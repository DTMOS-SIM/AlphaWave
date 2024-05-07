from datetime import datetime as dt
from infrastructure.interface.currencyweights import CurrencyWeights
from infrastructure.interface.Iasset import IAsset


class BTC(IAsset):

    def __init__(self):
        self._name = "BTC"
        self._weights = CurrencyWeights.BTC
        self._current_asset_weights = 0.0
        self._date_created = dt.now()
        self._date_modified = dt.now()

    def set_weight(self, weight: CurrencyWeights) -> None:
        self._weights = weight

    def get_weight(self) -> CurrencyWeights:
        return self._weights

    def set_current_asset_weightage(self, weight: float) -> None:
        self._current_asset_weights = weight

    def get_current_asset_weightage(self) -> float:
        return self._current_asset_weights

    def __del__(self):
        pass