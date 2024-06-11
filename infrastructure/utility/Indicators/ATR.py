from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class ATR(IIndicator):

    @staticmethod
    def calculate_historical_readings(dataframe: pd.DataFrame, window: int) -> pd.DataFrame:

        dataframe["Previous Close"] = dataframe["Close"].shift(1)
        true_range = dataframe.apply(lambda row: max(row["High"] - row["Low"], abs(row["High"] - row["Previous Close"]),
                                                     abs(row["Low"] - row["Previous Close"])), axis=1)

        rolling_true_range = true_range.rolling(window=window).sum()
        average_volatility = rolling_true_range * (1 / window)
        dataframe["Price_Diff"] = dataframe["Close"] - dataframe["Open"]
        dataframe["Next_Avg_Volatility"] = average_volatility.shift(-1)

        return dataframe

    @staticmethod
    def generate_signals(dataframe: pd.DataFrame) -> pd.Series:

        # Initialize signals
        signals = pd.Series(0, index=dataframe.index, dtype='int')

        # Generate signals using vectorized operations
        signals[(dataframe["Price_Diff"] > dataframe['Next_Avg_Volatility'])] = 1.0
        signals[(dataframe["Price_Diff"] < dataframe['Next_Avg_Volatility'])] = -1.0

        return signals

    @staticmethod
    def calculate(dataframe: pd.DataFrame, window: int):
        pass