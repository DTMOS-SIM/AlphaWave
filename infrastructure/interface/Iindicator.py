from abc import ABC, abstractmethod


class IIndicator(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def calculate_historical_readings(self):
        raise NotImplementedError

    @abstractmethod
    def calculate(self):
        raise NotImplementedError

    @abstractmethod
    def __del__(self):
        raise NotImplementedError
