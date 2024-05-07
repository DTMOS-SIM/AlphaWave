from abc import ABC, abstractmethod


class IWallet(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def update_account(self):
        raise NotImplementedError

    @abstractmethod
    def get_assets(self):
        raise NotImplementedError

    @abstractmethod
    def get_notional(self):
        raise NotImplementedError

    @abstractmethod
    def __del__(self):
        raise NotImplementedError
