import datetime
import logging
import time, threading

from infrastructure.interface.currencyWeightsEnum import CurrencyWeights
from infrastructure.utility.Indicators.MACD import MACD
from infrastructure.utility.Indicators.RSI import RSI
from infrastructure.utility.Indicators.Fibonacci import FIBONACCI
from infrastructure.utility.Indicators.Bollinger_Bands import BollingerBands
from infrastructure.utility.Indicators.Stochastic_Oscillator import StochasticOscillator
from services.asset import Asset
from services.wallet import Wallet
from infrastructure.interface.Iportfolio import IPortfolio
from infrastructure.utility.Adapters.binance_adapter import BinanceAdapter
from infrastructure.utility.Indicators.ATR import ATR


class Portfolio(IPortfolio):

    def __init__(self, assets: [Asset], wallet: Wallet):
        self.combined_signals = []
        self.assets = assets
        self.wallet = wallet

    def get_notional(self):
        return self._notional

    def show_specs(self):
        print("Wallet Data: ")
        print(self.wallet)
        for asset in self.assets:
            name, weight, position, current_asset, ta = asset.asset_info()
            print("Asset Name: ", name)
            print("Asset Weight: ", weight)
            print("Asset Positions: ")
            print(position)
            print("Asset Current weight: ", current_asset)
            print("Asset Indicators: ")
            for name, df in ta.items():
                print('TA Name: ', name)
                print('TA Value: ')
                print(df)

    def generate_signals(self):
        overall_signals = {}
        for asset in self.assets:

            indicators = asset.get_indicators()
            name = asset.get_name()

            # Consolidate values in list
            temp = [
                ATR().generate_signals(indicators['atr']).iloc[-1],
                RSI().generate_signals(indicators['rsi'], 30, 70).iloc[-1],
                MACD().generate_signals(indicators['macd']).iloc[-1],
                FIBONACCI().generate_signals(indicators['fibonacci'], 'Close').iloc[-1],
                BollingerBands().generate_signals(indicators['bollinger'], 'Close').iloc[-1],
                StochasticOscillator().generate_signals(indicators['stochastic']).iloc[-1]
            ]

            print(temp)

            # Compute buy/sell/hold for particular asset
            if max(temp, key=temp.count) == 1:
                overall_signals[name] = 1
            elif max(temp, key=temp.count) == -1:
                overall_signals[name] = -1
            else:
                overall_signals[name] = 0

        return overall_signals

    def activate_monitoring(self):

        logging.info(f'Monitoring for hourly data starting: {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')

        # DEBUGGING PURPOSE
        # print(time.ctime())

        # Generate new time stamp TAs
        signals = self.generate_signals()

        print(signals)

        # Update weightage and notional value based on hold and buy
        self.compute_realized_allocation(signals)

        for name, signal in signals.items():

            # Check if asset position is available
            for asset in self.assets:

                temp_positions = []

                # Assign temporary positions
                if asset.get_name() == name:
                    temp_positions = asset.get_positions()

                # Check for sell signals
                if signal == -1:

                    # Short if positions not available
                    if len(temp_positions) <= 0:
                        response = self.transact_assets(symbol=name, qty=asset.get_current_asset_weightage(), side='BUY', position_side='SHORT')
                        logging.info(response)

                    for position in temp_positions:
                        # Sell if positions are available
                        response = self.transact_assets(symbol=name, qty=position.positionAmt, side='SELL', position_side='SHORT')
                        logging.info(response)

                # Check for buy signals
                elif signal == 1:

                    # Sell all purchased assets
                    for position in temp_positions:
                        # Sell if positions are available
                        response = self.transact_assets(symbol=name, qty=position.positionAmt, side='SELL', position_side='LONG')
                        logging.info(response)

                    # Buy back new set of assets with correct weightages
                    response = self.transact_assets(symbol=name, qty=asset.get_current_asset_weightage(), side='BUY', position_side='LONG')
                    logging.info(response)

                else:
                    pass

        threading.Timer(5, self.activate_monitoring).start()

    def set_notional(self, notional):
        self._notional = notional

    def compute_realized_allocation(self, signals: {}):

        total_current_weights = 0.0

        # Compute total amount of weights required for denominator
        for key, value in signals.items():
            if value == 1 or value == 0:
                total_current_weights += CurrencyWeights[key].value

        # Compute each nominal individual
        for asset in self.assets:
            asset.set_current_asset_weightage(float(asset.get_weight() / total_current_weights) * float(self.wallet.total_wallet_balance))

    def transact_assets(self, symbol: str, qty: int, side: str, position_side: str):
        return BinanceAdapter().transact_assets(symbol=symbol, qty=qty, side=side, position_side=position_side)

    def filter_signals(self, indicators: []):
        pass

    def __del__(self):
        pass