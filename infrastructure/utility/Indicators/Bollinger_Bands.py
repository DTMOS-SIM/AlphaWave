from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class BollingerBands(IIndicator):

    def __init__(self, dataframe: pd.DataFrame, window: int = 14):
        super().__init__()
        self.df = dataframe
        self.window = window

    def calculate_historical_readings(self):

        # Ensure df is a DataFrame with the correct structure
        if isinstance(self.df, pd.Series):
            self.df = self.df.to_frame()  # Convert Series to DataFrame if necessary

        # Calculate the middle band (simple moving average)
        self.df['Middle_Band'] = self.df.iloc[:, 0].rolling(window=self.window).mean()

        # Calculate the standard deviation
        std = self.df.iloc[:, 0].rolling(window=self.window).std()

        # Calculate the upper band
        self.df['Upper_Band'] = self.df['Middle_Band'] + (std * 2)

        # Calculate the lower band
        self.df['Lower_Band'] = self.df['Middle_Band'] - (std * 2)

        return self.df

    def calculate(self):
        pass


    def __del__(self):
        pass
