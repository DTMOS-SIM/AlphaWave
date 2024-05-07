from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class MACD(IIndicator):

    def __init__(self, dataframe: pd.DataFrame, window: int = 14):
        super().__init__()
        self.dataframe = dataframe
        self.window = window

    def calculate_historical_readings(self):

        # Assume that the DataFrame contains only one column
        column_name = self.dataframe.columns[0]  # Dynamically get the name of the column

        # Calculate the short-term exponential moving average (EMA)
        short_ema = self.dataframe[column_name].ewm(span=self.window * (12 / 26), adjust=False).mean()

        # Calculate the long-term exponential moving average (EMA)
        long_ema = self.dataframe[column_name].ewm(span=self.window, adjust=False).mean()

        # Calculate the MACD line
        self.dataframe['MACD'] = short_ema - long_ema  # Name change to not use column_name in output

        # Calculate the signal line
        self.dataframe['Signal'] = self.dataframe['MACD'].ewm(span=9, adjust=False).mean()

        return self.dataframe

    def __del__(self):
        pass
