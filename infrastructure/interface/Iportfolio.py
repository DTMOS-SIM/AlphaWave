from abc import ABC, abstractmethod


class IPortfolio(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError

    @abstractmethod
    def filter_signals(self, indicators: []):
        raise NotImplementedError

    @abstractmethod
    def compute_realized_allocation(self):
        raise NotImplementedError

    @abstractmethod
    def sell_assets(self):
        raise NotImplementedError

    @abstractmethod
    def buy_assets(self):
        raise NotImplementedError

    @abstractmethod
    def __del__(self):
        raise NotImplementedError
