from enum import Enum
from infrastructure.utility.Indicators.ATR import ATR
from infrastructure.utility.Indicators.MACD import MACD
from infrastructure.utility.Indicators.RSI import RSI
from infrastructure.utility.Indicators.Fibonacci import FIBONACCI
from infrastructure.utility.Indicators.Bollinger_Bands import BollingerBands
from infrastructure.utility.Indicators.Stochastic_Oscillator import StochasticOscillator


class Indicators(Enum):
    ATR = ATR()
    RSI = RSI()
    Stochastic_Oscillator = StochasticOscillator()
    MACD = MACD()
    Bollinger_Bands = BollingerBands()
    Fibonacci = FIBONACCI()

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))