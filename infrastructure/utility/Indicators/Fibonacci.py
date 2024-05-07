from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class FIBONACCI(IIndicator):

    def __init__(self, dataframe: pd.DataFrame):
        super().__init__()
        self.dataframe = dataframe

    def calculate_historical_readings(self):

        # Get the single column name automatically assuming there's only one column
        column_name = self.dataframe.columns[0]

        # Find the maximum and minimum close price
        max_price = self.dataframe[column_name].max()
        min_price = self.dataframe[column_name].min()

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
            self.dataframe[level] = price

        return self.dataframe

    def __del__(self):
        pass
