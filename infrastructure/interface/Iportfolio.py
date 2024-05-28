from abc import ABC, abstractmethod


class IPortfolio(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def filter_signals(self, indicators: []):
        raise NotImplementedError

    @abstractmethod
    def show_specs(self):
        raise NotImplementedError

    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError

    @abstractmethod
    def compute_realized_allocation(self, signals: {}):
        raise NotImplementedError

    @abstractmethod
    def transact_assets(self, symbol: str, qty: int, side: str, position_side: str):
        raise NotImplementedError

    @abstractmethod
    def __del__(self):
        raise NotImplementedError
