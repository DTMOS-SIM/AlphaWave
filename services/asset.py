import datetime

from infrastructure.interface import Iasset
from infrastructure.interface.Binance.Iposition import IPosition


class Asset(Iasset):

    def __init__(self, name: str, weight: float, positions: [IPosition], date_created: datetime.datetime, date_modified: datetime.datetime):
        self.name = name
        self.weight = weight
        self.positions = positions
        self.date_created = date_created
        self.date_modified = date_modified

    def __del__(self):
        del self

