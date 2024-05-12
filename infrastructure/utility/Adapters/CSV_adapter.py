import string
from infrastructure.interface.IAdapter import GenericAdapter
import time
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
from pandas_datareader import data as pdr
import yfinance as yf

class CSVadapter(GenericAdapter):

    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CSVadapter, cls).__new__(cls)
        return cls.instance


    def __init__(self, file_name: string, data_type: string, start: dt, end: dt):

        self.file_name = file_name
        self.data_type = data_type
        self.start = start
        self.end = end

        raise NotImplementedError

    
    def get_credentials(self):
        raise NotImplementedError
    

    def get_account_info(self):
        raise NotImplementedError
   

    def get_asset_data(self):
        # Read csv command
        if self.data_type == "CSV":
            df = pd.read_csv(self.file_name)

        # Read yahoo command
        elif self.data_type == "YAHOO":
            df = pdr.get_data_yahoo(self.file_name, self.start, self.end,progress = False)

        return df


    def send_market_order(self, symbol: str, quantity: float, side: bool):

        timestamp = int(time.time() * 1000)
        order_record = {
            "symbol": symbol,
            "side": "BUY" if side else "SELL",
            "type": "MARKET",
            "quantity": quantity,
            'timestamp': timestamp
        }

        return order_record

        # raise NotImplementedError

    def __del__(self):
        raise NotImplementedError


