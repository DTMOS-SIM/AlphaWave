import logging
import time
import calendar
import pandas as pd
from datetime import datetime as dt
from infrastructure.interface.currencyWeightsEnum import CurrencyWeights
from infrastructure.interface.IAdapter import GenericAdapter
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()


class YfinanceAdapter(GenericAdapter, object):

    def __init__(self):
        self._dataframes = {}
        self._df_names = CurrencyWeights.list()

        start = dt(2019, 3, 31)
        end = dt(2024, 3, 31)

        self._dataframes[self._df_names[0]] = pdr.get_data_yahoo("BTC-USD", start, end, progress=False)
        self._dataframes[self._df_names[1]] = pdr.get_data_yahoo("ETH-USD", start, end, progress=False)
        self._dataframes[self._df_names[2]] = pdr.get_data_yahoo("BNB-USD", start, end, progress=False)
        self._dataframes[self._df_names[3]] = pdr.get_data_yahoo("ZEC-USD", start, end, progress=False)
        self._dataframes[self._df_names[4]] = pdr.get_data_yahoo("LTC-USD", start, end, progress=False)

    def get_credentials(self):
        pass

    def get_account_info(self):
        pass

    def get_asset_data(self):
        return self._dataframes

    def transact_assets(self, symbol: str, qty: float, side: str, position_side: str):
        pass

    def __del__(self):
        pass
