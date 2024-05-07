from infrastructure.interface.Iindicator import IIndicator
from statsmodels.tsa.stattools import pacf
import pandas as pd

class Optimal_Rolling_Window(IIndicator):

    def __init__(self, dataframe: pd.dataframe, significance_level: float = 0.05):
        super().__init__()
        self.dataframe = dataframe
        self.significance_level = significance_level

    def calculate_optimal_rolling_window(self):
        max_lags = min(40, len(self.dataframe) // 3)  # Adjust the denominator as needed
        pacf_values = pacf(self.dataframe, nlags=max_lags, alpha=self.significance_level)
        
        # The pacf function returns both the pacf values and the confidence intervals
        pacf_vals, confint = pacf_values
        
        # Find the last significant lag where PACF is outside the confidence bounds
        significant_lags = [i for i in range(len(pacf_vals)) if abs(pacf_vals[i]) > confint[i][1] - pacf_vals[i]]
        
        if significant_lags:
            optimal_lag = max(significant_lags)
        else:
            optimal_lag = 1  # Default to 1 if no significant lags are found
    
        return optimal_lag
    
    def __del__(self):
        # return super().__del__()
        pass


