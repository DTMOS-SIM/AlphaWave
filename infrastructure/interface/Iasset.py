from abc import ABC, abstractmethod
from infrastructure.interface.currencyWeightsEnum import CurrencyWeights
from services.position import Position


class IAsset(ABC):

    @abstractmethod
    def __init__(self, name: str, weight: CurrencyWeights, positions: [Position], TAs: {}):
        raise NotImplementedError

    @abstractmethod
    def asset_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_positions(self):
        raise NotImplementedError

    @abstractmethod
    def set_weight(self, weight: float):
        raise NotImplementedError

    @abstractmethod
    def get_weight(self):
        raise NotImplementedError

    @abstractmethod
    def set_current_asset_weightage(self, weight: float):
        raise NotImplementedError

    def get_current_asset_weightage(self):
        raise NotImplementedError

    @abstractmethod
    def __del__(self):
        raise NotImplementedError
