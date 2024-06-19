from enum import Enum


class HedgingAssets(Enum):
    BTCUSDT = 'IWV'
    ETHUSDT = 'XLF'
    BNBUSDT = 'XLF'
    ZECUSDT = 'XTL'
    LTCUSDT = 'XTL'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))

