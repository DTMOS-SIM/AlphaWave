from infrastructure.interface.Iindicator import IIndicator
import pandas as pd


class StochasticOscillator(IIndicator):
    @staticmethod
    def calculate_historical_readings(dataframe: pd.DataFrame, window: int) -> pd.DataFrame:
        dataframe["Lowest_Low"] = dataframe["Low"].rolling(window=window).min()
        dataframe["Highest_High"] = dataframe["High"].rolling(window=window).max()
        dataframe["Stochastic_Osc"] = (dataframe["Close"].shift(1) - dataframe["Lowest_Low"]) / (
                    dataframe["Highest_High"] - dataframe["Lowest_Low"])

        return dataframe

    @staticmethod
    def generate_signals(dataframe: pd.DataFrame, column_name: str) -> pd.Series:
        # Convert Series to DataFrame if necessary
        if isinstance(dataframe, pd.Series):
            dataframe = dataframe.to_frame(name='Stochastic_Osc')  # Assuming the series contains Stochastic Oscillator values

        # Initialize signals with 0 indicating no action
        signals = pd.Series(0, index=dataframe.index, dtype='int')

        # Assign buy signals where the stochastic oscillator is below 0.2
        signals[dataframe["Stochastic_Osc"] < 0.2] = 1  # Indicates a buy signal

        # Assign sell signals where the stochastic oscillator is above 0.8
        signals[dataframe["Stochastic_Osc"] > 0.8] = -1  # Indicates a sell signal

        return signals

    @staticmethod
    def calculate():
        pass
