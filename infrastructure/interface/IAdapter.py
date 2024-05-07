import threading
from abc import ABC, abstractmethod


class GenericAdapter(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def get_credentials(self):
        raise NotImplementedError

    @abstractmethod
    def get_account_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_asset_data(self):
        raise NotImplementedError

    @abstractmethod
    def send_market_order(self, key: str, secret: str, symbol: str, quantity: float, side: bool):
        raise NotImplementedError

    @abstractmethod
    def __del__(self):
        raise NotImplementedError