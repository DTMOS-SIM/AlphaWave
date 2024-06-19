import logging
import threading
import time
import os
from dotenv import load_dotenv
from pathlib import Path

from infrastructure.utility.Adapters.alpaca_adapter import AlpacaAdapter
from infrastructure.utility.Adapters.yfinance_adapter import YfinanceAdapter
from services.position import Position
from infrastructure.interface.currencyWeightsEnum import CurrencyWeights
from services.asset import Asset
from infrastructure.utility.Adapters.binance_adapter import BinanceAdapter
from services.portfolio import Portfolio
from infrastructure.utility.Indicators import ATR, Bollinger_Bands, Fibonacci, MACD, RSI, Stochastic_Oscillator
from services.wallet import Wallet

if __name__ == '__main__':
    load_dotenv()

    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_api_secret = os.getenv("ALPACA_API_SECRET")
    binance_api_key = os.getenv("BINANCE_API_KEY")
    binance_api_secret = os.getenv("BINANCE_API_SECRET")

    # logging configuration
    logging.basicConfig(format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
                        level=logging.INFO)

    # Declare right type of adapter to use
    api_adapter = BinanceAdapter(binance_api_key, binance_api_secret)
    hedging_adapter = AlpacaAdapter(alpaca_api_key, alpaca_api_secret)

    # Reflect platform
    if isinstance(api_adapter, BinanceAdapter):
        data, assets, positions = api_adapter.get_account_info()

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

        # Binance api to fetch and map into dataframe for consolidation of data
        response = api_adapter.get_initial_df(3600, 15)

        temp_assets_list = []

        # Loop through each key e.g. (BTCUSDT, BNBUSDT etc.) and create TA's Positions automatically.
        for item in response.keys():

            temp_position_list = []

            # Generate & add in TAs into each asset class
            TAs = {
                'atr': ATR.ATR().calculate_historical_readings(response[item].copy(), 5),
                'bollinger': Bollinger_Bands.BollingerBands().calculate_historical_readings(response[item].copy(), 5),
                'fibonacci': Fibonacci.FIBONACCI().calculate_historical_readings(response[item].copy(), 5),
                'macd': MACD.MACD().calculate_historical_readings(response[item].copy(), 5),
                'rsi': RSI.RSI().calculate_historical_readings(response[item].copy(), 5),
                'stochastic': Stochastic_Oscillator.StochasticOscillator().calculate_historical_readings(
                    response[item].copy(), 5)}

            # Map current positions to system
            for position in positions:
                if position['symbol'] == item:
                    temp_position = Position(
                        symbol=item,
                        initialMargin=float(position['initialMargin']),
                        maintMargin=float(position['maintMargin']),
                        unrealizedProfit=float(position['unrealizedProfit']),
                        positionInitialMargin=float(position['positionInitialMargin']),
                        openOrderInitialMargin=float(position['openOrderInitialMargin']),
                        leverage=float(position['leverage']),
                        isolated=bool(position['isolated']),
                        entryPrice=float(position['entryPrice']),
                        maxNotional=float(position['maxNotional']),
                        bidNotional=float(position['bidNotional']),
                        askNotional=float(position['askNotional']),
                        positionSide=str(position['positionSide']),
                        positionAmt=float(position['positionAmt']),
                        updateTime=float(position['updateTime'])
                    )
                    temp_position_list.append(temp_position)

            temp_asset = Asset(item, CurrencyWeights[item].value, positions=temp_position_list, TAs=TAs)
            temp_assets_list.append(temp_asset)

        # Assign portfolio asset allocation
        portfolio = Portfolio(assets=temp_assets_list, wallet=wallet)

        # DEBUGGING PURPOSE
        # portfolio.show_specs()

        while True:
            portfolio.activate_monitoring(api_adapter)
            time.sleep(60)

    elif isinstance(api_adapter, YfinanceAdapter):

        # data, assets, positions = api_adapter.get_account_info()

        # Create Wallet
        wallet = Wallet(
            0,
            1000000,
            0,
            0,
            0,
            1000000,
            1000000,
        )

        # Binance api to fetch and map into dataframe for consolidation of data
        response = api_adapter.get_asset_data()

        print(response)

        temp_assets_list = []

        # Loop through each key e.g. (BTCUSDT, BNBUSDT etc.) and create TA's Positions automatically.
        for item in response.keys():
            temp_position_list = []

            # Generate & add in TAs into each asset class
            TAs = {
                'atr': ATR.ATR().calculate_historical_readings(response[item].copy(), 5),
                'bollinger': Bollinger_Bands.BollingerBands().calculate_historical_readings(response[item].copy(), 5),
                'fibonacci': Fibonacci.FIBONACCI().calculate_historical_readings(response[item].copy(), 5),
                'macd': MACD.MACD().calculate_historical_readings(response[item].copy(), 5),
                'rsi': RSI.RSI().calculate_historical_readings(response[item].copy(), 5),
                'stochastic': Stochastic_Oscillator.StochasticOscillator().calculate_historical_readings(
                    response[item].copy(), 5)
            }

            temp_asset = Asset(item, CurrencyWeights[item].value, positions=[], TAs=TAs)
            temp_assets_list.append(temp_asset)

        # Assign portfolio asset allocation
        portfolio = Portfolio(assets=temp_assets_list, wallet=wallet)

        # DEBUGGING PURPOSE
        portfolio.show_specs()

        # Activate Monitoring
        threading.Timer(60, portfolio.activate_monitoring(api_adapter)).start()
