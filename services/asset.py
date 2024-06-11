import datetime
from infrastructure.interface.Iasset import IAsset
from services.position import Position
from infrastructure.interface.currencyWeightsEnum import CurrencyWeights


class Asset(IAsset, object):

    def __init__(self, name: str, weight: CurrencyWeights, positions: [Position], TAs: dict):
        self._name = name
        self._weight = weight
        self._positions = positions
        self.__current_asset_weights = 0.0
        self._date_created = datetime.datetime.now()
        self._date_modified = datetime.datetime.now()
        self.TAs = TAs

    def asset_info(self):
        return self._name, self._weight, self._positions, self._current_asset_weights, self._TAs

    def get_positions(self):
        return self._positions

    def get_name(self):
        return self._name

    def set_weight(self, weight: CurrencyWeights) -> None:
        self._weight = weight

    def get_weight(self) -> CurrencyWeights:
        return self._weight

    def set_indicators(self, indicators: {}) -> None:
        self.TAs = indicators

    def get_indicators(self) -> dict:
        return self.TAs

    def set_current_asset_weightage(self, weight: float):
        self.__current_asset_weights = weight

    def get_current_asset_weightage(self) -> float:
        return self.__current_asset_weights

    def __del__(self):
        pass

