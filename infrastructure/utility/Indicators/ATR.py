from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class ATR(IIndicator):

    def __init__(self, dataframe: pd.DataFrame, window: int = 14):
        super().__init__()
        self.dataframe = dataframe
        self.window = window

    def calculate_historical_readings(self):

        self.dataframe["Previous Close"] = self.dataframe["Close"].shift(1)
        true_range = self.dataframe.apply(lambda row: max(row["High"] - row["Low"], abs(row["High"] - row["Previous Close"]),
                                                     abs(row["Low"] - row["Previous Close"])), axis=1)

        rolling_true_range = true_range.rolling(window=self.window).sum()
        average_volatility = rolling_true_range * (1 / self.window)
        self.dataframe["Price_Diff"] = self.dataframe["Close"] - self.dataframe["Open"]
        self.dataframe["Next_Avg_Volatility"] = average_volatility.shift(-1)

        return self.dataframe

    def calculate(self):
        pass

    def __del__(self):
        pass
