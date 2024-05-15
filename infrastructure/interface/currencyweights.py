from enum import Enum


class CurrencyWeights(Enum):
    BTCUSDT = 0.23
    ETHUSDT = 2.37
    BNBUSDT = 22.06
    ZECUSDT = 3.26
    LTCUSDT = 71.78

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))

