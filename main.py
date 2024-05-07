import logging

from infrastructure.utility.Assets import ETH, BNB, WETH, LIC, BTC
from infrastructure.utility.Adapters.binance_adapter import BinanceAdapter
from services.portfolio import Portfolio
from infrastructure.utility.Indicators import ATR, Bollinger_Bands, Fibonacci, MACD, RSI, Stochastic_Oscillator
from services.wallet import Wallet


def main():
    # logging configuration
    logging.basicConfig(format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
                        level=logging.INFO)

    # Declare right type of adapter to use
    binance_adapter = BinanceAdapter()
    data = binance_adapter.get_account_info()

    # Pipe down csv or binance collected dataframe
    #Binance
    df = binance_adapter.get_asset_data()

    #CSV

    # Create Wallet
    wallet = Wallet(
        data['feeTier'],
        data['totalWalletBalance'],
        data['totalUnrealizedProfit'],
        data['totalMarginalBalance'],
        data['totalCrossWalletBalance'],
        data['availableBalance'],
        data['maxWithdrawalAmount'],
    )

    # Create TAs
    indicators = [
        ATR.ATR(dataframe=df, window=15),
        RSI.RSI(dataframe=df, window=15),
        MACD.MACD(dataframe=df, window=15),
        Bollinger_Bands.BollingerBands(dataframe=df, window=15),
        Fibonacci.FIBONACCI(dataframe=df),
        Stochastic_Oscillator.StochasticOscillator(dataframe=df, window=15)
    ]

    # Create Assets
    assets = [
        ETH.ETH(),
        BNB.BNB(),
        BTC.BTC(),
        WETH.WETH(),
        LIC.LIC()
    ]

    # Assign/Check/Filter/Compute/Update portfolio asset allocation
    portfolio = Portfolio(indicators=indicators, assets=assets, wallet=wallet)

    # Generate new time stamp TAs
    signals = portfolio.generate_signals()

    # Filter signals that are within a certain range
    portfolio.filter_signals(signals)

    # Sell any negative signal indications
    portfolio.sell_assets()

    # Update weightage and notional value
    portfolio.compute_realized_allocation()

    # Buy any remaining buy signal indications
    portfolio.buy_assets()


if __name__ == '__main__':
    main()
