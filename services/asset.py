import datetime
from infrastructure.interface.Iasset import IAsset
from services.position import Position
from infrastructure.interface.currencyweights import CurrencyWeights


class Asset(IAsset):

    def __init__(self, name: str, weight: CurrencyWeights, positions: [Position], TAs: {}):
        self._name = name
        self._weight = weight
        self._positions = positions
        self._current_asset_weights = 0.0
        self._date_created = datetime.datetime.now()
        self._date_modified = datetime.datetime.now()
        self._TAs = TAs

    def asset_info(self) -> [Position]:
        return self._name, self._weight, self._positions, self._current_asset_weights, self._TAs

    def set_weight(self, weight: CurrencyWeights) -> None:
        self._weight = weight

    def get_weight(self) -> CurrencyWeights:
        return self._weights

    def set_indicators(self, indicators: {}) -> None:
        self._TAs = indicators

    def get_indicators(self) -> dict:
        return self._TAs

    def set_current_asset_weightage(self, weight: float):
        self._current_asset_weights = weight

    def get_current_asset_weightage(self) -> float:
        return self._current_asset_weights

    def __del__(self):
        pass

