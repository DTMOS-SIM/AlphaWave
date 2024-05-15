from abc import ABC, abstractmethod
import pandas as pd


class IIndicator(ABC):

    @staticmethod
    @abstractmethod
    def calculate_historical_readings():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def calculate():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_signals():
        raise NotImplementedError
