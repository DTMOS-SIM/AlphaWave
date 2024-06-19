import datetime
import logging
import threading

from infrastructure.interface.currencyWeightsEnum import CurrencyWeights
from infrastructure.interface.hedgingAssetsEnum import HedgingAssets
from infrastructure.utility.Adapters.alpaca_adapter import AlpacaAdapter
from infrastructure.utility.Adapters.yfinance_adapter import YfinanceAdapter
from infrastructure.utility.Indicators import Bollinger_Bands, Fibonacci, Stochastic_Oscillator
from infrastructure.utility.Indicators.ATR import ATR
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

    def get_asset(self):
        return self.assets

    def get_wallet(self):
        return self.wallet

    def set_wallet(self, wallet: Wallet):
        self.wallet = wallet

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
            temp = list(map(int, [
                ATR().generate_signals(indicators['atr']).iloc[-1],
                RSI().generate_signals(indicators['rsi'], 30, 70).iloc[-1],
                MACD().generate_signals(indicators['macd']).iloc[-1],
                FIBONACCI().generate_signals(indicators['fibonacci'], 'Close').iloc[-1],
                BollingerBands().generate_signals(indicators['bollinger'], 'Close').iloc[-1],
                StochasticOscillator().generate_signals(indicators['stochastic']).iloc[-1]
            ]))

            print("Asset Name: " + name)
            print(temp)

            # Compute buy/sell/hold for particular asset
            if temp.count(1) > temp.count(-1) and temp.count(1) >= 2:
                overall_signals[name] = 1
            elif temp.count(1) < temp.count(-1) and temp.count(-1) >= 2:
                overall_signals[name] = -1
            else:
                overall_signals[name] = 0

        return overall_signals

    def activate_monitoring(self, adapter: BinanceAdapter | YfinanceAdapter):

        logging.info(f'Monitoring for hourly data starting: {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')

        data, assets, positions = adapter.get_account_info()

        # Create Wallet
        wallet = Wallet(
            data['feeTier'],
            data['totalWalletBalance'],
            data['totalUnrealizedProfit'],
            data['totalMarginBalance'],
            data['totalCrossWalletBalance'],
            data['availableBalance'],
            data['maxWithdrawAmount'],
        )

        self.set_wallet(wallet)

        # Call updated rows of data
        for asset in self.assets:
            updated_df_response = adapter.get_current_df_row(asset.get_indicators(), asset.get_name())

            for x, y in updated_df_response.items():
                match x:
                    case 'atr':
                        updated_df_response[x] = ATR().calculate_historical_readings(updated_df_response[x].copy(), 5)
                    case 'bollinger':
                        updated_df_response[x] = Bollinger_Bands.BollingerBands().calculate_historical_readings(updated_df_response[x].copy(), 5)
                    case 'fibonacci':
                        updated_df_response[x] = Fibonacci.FIBONACCI().calculate_historical_readings(updated_df_response[x].copy(), 5)
                    case 'macd':
                        updated_df_response[x] = MACD().calculate_historical_readings(updated_df_response[x].copy(), 5)
                    case 'rsi':
                        updated_df_response[x] = RSI().calculate_historical_readings(updated_df_response[x].copy(), 5)
                    case 'stochastic':
                        updated_df_response[x] = Stochastic_Oscillator.StochasticOscillator().calculate_historical_readings(updated_df_response[x].copy(), 5)

            asset.set_indicators(updated_df_response)

        # Generate new time stamp TAs
        signals = self.generate_signals()

        print(signals)

        # Update weightage and notional value based on hold and buy
        self.compute_realized_allocation(signals)

        self.execute_trade(signals)

    def compute_realized_allocation(self, signals: {}):

        total_current_weights = 0.0

        # Compute total amount of weights required for denominator
        for key, value in signals.items():
            if value == 1 or value == -1:
                total_current_weights += CurrencyWeights[key].value

        # Compute each nominal individual
        for key, value in signals.items():
            for asset in self.assets:
                if asset.get_name() == key and value == 1 or value == -1:
                    new_weights = float(asset.get_weight() / total_current_weights) * float(self.wallet.total_wallet_balance)
                    asset.set_current_asset_weightage(new_weights)
                    print("Current asset weights for " + asset.get_name() + ": ", asset.get_current_asset_weightage())
                    break

    def execute_trade(self, signals: dict):
        for name, signal in signals.items():

            hedging_option = HedgingAssets.__getitem__(name).value

            # Check if asset position is available
            for asset in self.assets:

                temp_positions = []
                is_empty_array: bool
                is_long_empty_position: bool
                is_short_empty_position: bool

                # Assign temporary positions
                if asset.get_name() == name:
                    temp_positions = BinanceAdapter().get_market_positions(symbol=name)
                    is_empty_array = True if len(temp_positions) > 0 else False
                    is_long_empty_position = True if float(temp_positions[0]['positionAmt']) == 0 else False
                    is_short_empty_position = True if float(temp_positions[0]['positionAmt']) == 0 else False

                # Check for sell signals
                if signal == -1:

                    # Short if positions not available
                    if is_empty_array or is_long_empty_position and is_short_empty_position:
                        new_qty = round(asset.get_current_asset_weightage()/BinanceAdapter().get_ticker_price(name), 3)
                        new_hedge_qty = round(asset.get_current_asset_weightage()/AlpacaAdapter().get_current_ticker_data(name), 3)
                        response = self.transact_assets(symbol=name, qty=new_qty, side='SELL', position_side='SHORT')
                        hedge_response = self.transact_hedge_assets(symbol=hedging_option, qty=new_hedge_qty, side='BUY', position_side='LONG')
                        logging.info(f'Sell new short position placed for {name}')
                        logging.info(f'Buy new long hedge position placed for {hedging_option}')
                        break

                    # Check if existing short position exist
                    elif not is_short_empty_position:
                        # Skip short
                        break

                    elif not is_long_empty_position and not is_short_empty_position:
                        # If long previously, sell short positions
                        new_hedge_qty = round(temp_positions[0]['positionAmt'] / AlpacaAdapter().get_current_ticker_data(name), 3)
                        response = self.transact_assets(symbol=name, qty=temp_positions[0]['positionAmt'], side='BUY',position_side=temp_positions[0]['positionSide'])
                        hedge_response = self.transact_hedge_assets(symbol=hedging_option, qty=new_hedge_qty,side='BUY', position_side='SHORT')
                        logging.info(f'Sell SHORT position placed for {name}')
                        logging.info(f'Buy LONG hedge position placed for {hedging_option}')
                        break

                # Check for buy signals
                elif signal == 1:

                    # Sell if positions are available
                    if not is_empty_array or not is_long_empty_position and not is_short_empty_position:
                        response = self.transact_assets(symbol=name, qty=temp_positions[0]['positionAmt'], side='SELL',position_side='LONG')
                        hedge_response = self.transact_hedge_assets(symbol=hedging_option, qty=new_hedge_qty,side='BUY', position_side='SHORT')
                        logging.info(f'Sell LONG position placed for {name}')
                        logging.info(f'Buy SHORT hedge position placed for {hedging_option}')

                    # Buy back new set of assets with correct weightages
                    new_qty = round(asset.get_current_asset_weightage() / BinanceAdapter().get_ticker_price(name), 3)
                    new_hedge_qty = round(asset.get_current_asset_weightage() / AlpacaAdapter().get_current_ticker_data(name), 3)
                    response = self.transact_assets(symbol=name, qty=new_qty, side='BUY', position_side='LONG')
                    hedge_response = self.transact_hedge_assets(symbol=hedging_option, qty=new_hedge_qty, side='SELL',position_side='SHORT')
                    logging.info(f'Buy LONG position placed for {name}')
                    logging.info(f'Sell SHORT hedge position placed for {hedging_option}')
                    break

                # Hold position do not touch
                else:
                    break

    def transact_assets(self, symbol: str, qty: int, side: str, position_side: str):
        return BinanceAdapter().transact_assets(symbol=symbol, qty=qty, side=side, position_side=position_side)

    def transact_hedge_assets(self, symbol: str, qty: int, side: str):
        return AlpacaAdapter().transact_assets(symbol=symbol, qty=qty, side=side)
      
    def filter_signals(self, indicators: []):
        pass

    def __del__(self):
        pass