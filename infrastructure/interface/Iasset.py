from abc import ABC, abstractmethod


class IAsset(ABC):

    @abstractmethod
    def __init__(self):
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
