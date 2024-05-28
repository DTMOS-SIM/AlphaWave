import logging

from infrastructure.utility.Adapters.yfinance_adapter import YfinanceAdapter
from services.position import Position
from infrastructure.interface.currencyWeightsEnum import CurrencyWeights
from services import asset
from infrastructure.utility.Adapters.binance_adapter import BinanceAdapter
from services.portfolio import Portfolio
from infrastructure.utility.Indicators import ATR, Bollinger_Bands, Fibonacci, MACD, RSI, Stochastic_Oscillator
from services.wallet import Wallet


def main():
    # logging configuration
    logging.basicConfig(format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
                        level=logging.INFO)

    # Declare right type of adapter to use
    api_adapter = YfinanceAdapter()

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
        response = api_adapter.get_initial_df(1, 5)

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
                'stochastic': Stochastic_Oscillator.StochasticOscillator().calculate_historical_readings(response[item].copy(), 5)
            }

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

            temp_asset = asset.Asset(item, CurrencyWeights[item].value, positions=temp_position_list, TAs=TAs)
            temp_assets_list.append(temp_asset)

        # Assign portfolio asset allocation
        portfolio = Portfolio(assets=temp_assets_list, wallet=wallet)

        # DEBUGGING PURPOSE
        # portfolio.show_specs()

        # Activate Monitoring
        portfolio.activate_monitoring()

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

            # Map current positions to system
            # for position in positions:
            #     if position['symbol'] == item:
            #         temp_position = Position(
            #             symbol=item,
            #             initialMargin=float(position['initialMargin']),
            #             maintMargin=float(position['maintMargin']),
            #             unrealizedProfit=float(position['unrealizedProfit']),
            #             positionInitialMargin=float(position['positionInitialMargin']),
            #             openOrderInitialMargin=float(position['openOrderInitialMargin']),
            #             leverage=float(position['leverage']),
            #             isolated=bool(position['isolated']),
            #             entryPrice=float(position['entryPrice']),
            #             maxNotional=float(position['maxNotional']),
            #             bidNotional=float(position['bidNotional']),
            #             askNotional=float(position['askNotional']),
            #             positionSide=str(position['positionSide']),
            #             positionAmt=float(position['positionAmt']),
            #             updateTime=float(position['updateTime'])
            #         )
            #         temp_position_list.append(temp_position)

            temp_asset = asset.Asset(item, CurrencyWeights[item].value, positions=[], TAs=TAs)
            temp_assets_list.append(temp_asset)

        # Assign portfolio asset allocation
        portfolio = Portfolio(assets=temp_assets_list, wallet=wallet)

        # DEBUGGING PURPOSE
        portfolio.show_specs()

        # Activate Monitoring
        portfolio.activate_monitoring()


if __name__ == '__main__':
    main()
