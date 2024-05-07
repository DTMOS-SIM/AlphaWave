from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class RSI(IIndicator):

    def __init__(self, dataframe: pd.DataFrame, window: int = 14):
        super().__init__()
        self.dataframe = dataframe
        self.window = window

    def calculate_historical_readings(self):
        # Assume the data is in the first column if not explicitly provided
        column_name = self.dataframe.columns[0]  # Automatically get the column name

        # Calculate price changes
        delta = self.dataframe[column_name].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0).fillna(0)
        loss = -delta.where(delta < 0, 0).fillna(0)

        # Calculate the exponential moving average of gains and losses
        avg_gain = gain.ewm(com=self.window - 1, min_periods=self.window).mean()
        avg_loss = loss.ewm(com=self.window - 1, min_periods=self.window).mean()

        # Calculate the RS
        rs = avg_gain / avg_loss

        # Calculate the RSI
        rsi = 100 - (100 / (1 + rs))

        # Append the RSI to the DataFrame
        self.dataframe['RSI'] = rsi

        return self.dataframe

    def __del__(self):
        pass
