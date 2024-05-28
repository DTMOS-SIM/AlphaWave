from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class FIBONACCI(IIndicator):
    @staticmethod
    def calculate_historical_readings(dataframe: pd.DataFrame, window: int) -> pd.DataFrame:

        # Get the single column name automatically assuming there's only one column
        column_name = dataframe.columns[0]

        # Find the maximum and minimum close price
        max_price = dataframe[column_name].max()
        min_price = dataframe[column_name].min()

        # Calculate Fibonacci Levels considering the maximum and minimum price
        diff = max_price - min_price
        levels = {
            'Level_23.6%': max_price - diff * 0.236,
            'Level_38.2%': max_price - diff * 0.382,
            'Level_50%': max_price - diff * 0.5,
            'Level_61.8%': max_price - diff * 0.618,
        }

        # Append Fibonacci retracement levels to the DataFrame
        for level, price in levels.items():
            dataframe[level] = price

        return dataframe

    @staticmethod
    def generate_signals(dataframe: pd.DataFrame, column_name: str) -> pd.Series:
        signals = pd.Series(index=dataframe.index, dtype=int)  # Initialize the signals Series

        # Calculate the maximum and minimum to re-establish the Fibonacci levels
        max_price = dataframe[column_name].max()
        min_price = dataframe[column_name].min()
        diff = max_price - min_price
        levels = {
            'Level_23.6%': max_price - diff * 0.236,
            'Level_38.2%': max_price - diff * 0.382,
            'Level_50%': max_price - diff * 0.5,
            'Level_61.8%': max_price - diff * 0.618,
        }

        # Determine if prices rebound from levels (simplified logic)
        for i in range(1, len(dataframe)):
            previous_price = dataframe[column_name].iloc[i - 1]
            current_price = dataframe[column_name].iloc[i]
            for level, price in levels.items():
                if previous_price < price <= current_price:  # Crossing up a level
                    signals.iloc[i] = 1  # Potential buy signal
                elif previous_price > price >= current_price:  # Crossing down a level
                    signals.iloc[i] = -1  # Potential sell signal
                else:
                    signals.iloc[i] = 0

        return signals

    @staticmethod
    def calculate():
        pass