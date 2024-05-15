from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class BollingerBands(IIndicator):

    @staticmethod
    def calculate_historical_readings(dataframe: pd.DataFrame, window: int) -> pd.DataFrame:

        # Calculate the middle band (simple moving average)
        dataframe['Middle_Band'] = dataframe.iloc[:, 0].rolling(window=window).mean()

        # Calculate the standard deviation
        std = dataframe.iloc[:, 0].rolling(window=window).std()

        # Calculate the upper band
        dataframe['Upper_Band'] = dataframe['Middle_Band'] + (std * 2)

        # Calculate the lower band
        dataframe['Lower_Band'] = dataframe['Middle_Band'] - (std * 2)

        return dataframe

    @staticmethod
    def generate_signals(dataframe: pd.DataFrame, window: int) -> pd.Series:

        signals = pd.Series(index=dataframe.index, dtype=int)

        # Generate signals based on Bollinger Band conditions
        for index, row in dataframe.iterrows():
            if row[column] < row['Lower_Band']:
                signals.loc[index] = 1  # Buy signal
            elif row[column] > row['Upper_Band']:
                signals.loc[index] = -1  # Sell signal
            else:
                signals.loc[index] = 0  # Hold

        return signals

    @staticmethod
    def calculate(self):
        pass
