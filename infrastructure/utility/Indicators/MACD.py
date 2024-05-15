from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class MACD(IIndicator):

    @staticmethod
    def calculate_historical_readings(dataframe: pd.DataFrame, window: int) -> pd.DataFrame:

        # Assume that the DataFrame contains only one column
        column_name = dataframe.columns[0]  # Dynamically get the name of the column

        # Calculate the short-term exponential moving average (EMA)
        short_ema = dataframe[column_name].ewm(span=window * (12 / 26), adjust=False).mean()

        # Calculate the long-term exponential moving average (EMA)
        long_ema = dataframe[column_name].ewm(span=window, adjust=False).mean()

        # Calculate the MACD line
        dataframe['MACD'] = short_ema - long_ema  # Name change to not use column_name in output

        # Calculate the signal line
        dataframe['Signal'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()

        return dataframe

    @staticmethod
    def generate_signals(dataframe: pd.DataFrame) -> pd.Series:
        signals = pd.Series(index=dataframe.index, dtype=int)  # Initialize the signals Series

        # Iterate through the DataFrame to generate signals
        for index, row in dataframe.iterrows():
            if row['MACD'] > row['Signal']:
                signals.loc[index] = 1  # Buy signal if MACD crosses above the signal line
            elif row['MACD'] < row['Signal']:
                signals.loc[index] = -1  # Sell signal if MACD crosses below the signal line
            else:
                signals.loc[index] = 0  # Hold if there's no crossover

        return signals

    @staticmethod
    def calculate():
        pass