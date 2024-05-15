import asyncio
import logging
from services.position import Position
from infrastructure.interface.currencyweights import CurrencyWeights
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
    api_adapter = BinanceAdapter()

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
        response = api_adapter.get_initial_df(1, 10)

        temp_assets_list = []

        # Loop through each key e.g. (BTCUSDT, BNBUSDT etc.) and create TA's Positions automatically.
        for item in response.keys():

            temp_position_list = []

            # Generate TAs for initial findings
            atr_df = ATR.ATR().calculate_historical_readings(response[item], 15)
            boll_df = Bollinger_Bands.BollingerBands().calculate_historical_readings(response[item], 15)
            fib_df = Fibonacci.FIBONACCI().calculate_historical_readings(response[item], 15)
            macd_df = MACD.MACD().calculate_historical_readings(response[item], 15)
            rsi_df = RSI.RSI().calculate_historical_readings(response[item], 15)
            stochastic_df = Stochastic_Oscillator.StochasticOscillator().calculate_historical_readings(response[item],
                                                                                                       15)
            # Add in TAs into each asset class
            TAs = {
                'atr': atr_df,
                'bollinger': boll_df,
                'fibonacci': fib_df,
                'macd': macd_df,
                'rsi': rsi_df,
                'stochastic': stochastic_df
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

        portfolio.show_specs()

        # # Generate new time stamp TAs
        # signals = portfolio.generate_signals()
        #
        # # Sell any negative signal indications
        # portfolio.sell_assets()
        #
        # # Update weightage and notional value
        # portfolio.compute_realized_allocation()
        #
        # # Buy any remaining buy signal indications
        # portfolio.buy_assets()


if __name__ == '__main__':
    main()
