from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class RSI(IIndicator):

    @staticmethod
    def calculate_historical_readings(dataframe: pd.DataFrame, window: int) -> pd.DataFrame:
        # Assume the data is in the first column if not explicitly provided
        column_name = dataframe.columns[0]  # Automatically get the column name

        # Calculate price changes
        delta = dataframe[column_name].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0).fillna(0)
        loss = -delta.where(delta < 0, 0).fillna(0)

        # Calculate the exponential moving average of gains and losses
        avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
        avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()

        # Calculate the RS
        rs = avg_gain / avg_loss

        # Calculate the RSI
        rsi = 100 - (100 / (1 + rs))

        # Append the RSI to the DataFrame
        dataframe['RSI'] = rsi

        return dataframe

    @staticmethod
    def generate_signals(dataframe: pd.DataFrame, lower: int, upper: int) -> pd.Series:
        signals = pd.Series(index=dataframe.index, dtype=int)  # Initialize the signals Series

        # No need to convert to DataFrame, assuming df already includes an 'RSI' column
        for index, row in dataframe.iterrows():
            if row['RSI'] < lower:
                signals.loc[index] = 1  # Buy signal
            elif row['RSI'] > upper:
                signals.loc[index] = -1  # Sell signal
            else:
                signals.loc[index] = 0  # Hold

        return signals

    @staticmethod
    def calculate():
        pass
