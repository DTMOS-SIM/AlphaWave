from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class StochasticOscillator(IIndicator):

    def __init__(self, dataframe: pd.DataFrame, window: int = 14):
        super().__init__()
        self.dataframe = dataframe
        self.window = window

    def calculate_historical_readings(self):
        self.dataframe["Lowest_Low"] = self.dataframe["Low"].rolling(window=self.window).min()
        self.dataframe["Highest_High"] = self.dataframe["High"].rolling(window=self.window).max()
        self.dataframe["Stochastic_Osc"] = (self.dataframe["Close"].shift(1) - self.dataframe["Lowest_Low"]) / (
                    self.dataframe["Highest_High"] - self.dataframe["Lowest_Low"])

        return self.dataframe

    def __del__(self):
        pass
