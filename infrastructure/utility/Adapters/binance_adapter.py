import logging
import time
import hmac
import hashlib
import requests
import calendar
import pandas as pd
from datetime import datetime as dt, timezone
from urllib.parse import urlencode
from promisio import promisify
from infrastructure.interface.currencyweights import CurrencyWeights
from infrastructure.interface.IAdapter import GenericAdapter
from binance.um_futures import UMFutures


class BinanceAdapter(GenericAdapter, object):

    instance = None

    def __init__(self):
        self._base_url = 'https://testnet.binancefuture.com'
        self._api_key = 'b8e0a5bc6ccfe44e8458f633c9c7e12859f181a5cbc23db42d2a03bc851b63b7'
        self._secret_key = 'af61a6188b81f0038715e0ae5837333fa39772c8114641d5e013a15d8c26fa12'
        self._futures_client = UMFutures(key=self._api_key, secret=self._secret_key, base_url=self._base_url)

    def get_credentials(self):
        return self._base_url, self._api_key, self._secret_key

    def get_account_info(self):
        response = self._futures_client.account()
        return response, response['assets'], response['positions']

    def get_asset_data(self):
        pass

    def get_market_data(self, interval: str):
        temp_dict = {}
        pairs = CurrencyWeights.list()

        temp_dict[pairs[0]] = self._futures_client.klines(symbol=pairs[0], interval=interval)[-1][1:6]
        temp_dict[pairs[1]] = self._futures_client.klines(pairs[1], interval)[-1][1:6]
        temp_dict[pairs[2]] = self._futures_client.klines(pairs[2], interval)[-1][1:6]
        temp_dict[pairs[3]] = self._futures_client.klines(pairs[3], interval)[-1][1:6]
        temp_dict[pairs[4]] = self._futures_client.klines(pairs[4], interval)[-1][1:6]

        temp_dict = {key: list(map(float, value)) for key, value in temp_dict.items()}

        return temp_dict

    def get_initial_df(self, seconds, interval):
        dict_temp = {}

        # Generate a list of dataframes for manipulation
        for pair in CurrencyWeights.list():
            dict_temp[pair] = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

        initial_interval = interval

        while interval:
            try:
                logging.info(f'Getting initial data for T + {initial_interval - interval}')

                response = self.get_market_data("1h")
                time_now = calendar.timegm((dt.utcnow()).utctimetuple())

                for pair in CurrencyWeights.list():
                    dict_temp[pair].loc[time_now] = response.get(pair)

                interval -= 1
            except Exception as e:
                raise e
            time.sleep(seconds)
            logging.info(f'Sleeping for {seconds} seconds')
        # Completed
        logging.info(f'Finished getting initial data for T + {initial_interval}')
        return dict_temp

    def __del__(self):
        pass

    # send market order
    def send_market_order(self, key: str, secret: str, symbol: str, quantity: float, side: bool):
        # order parameters
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "side": "BUY" if side else "SELL",
            "type": "MARKET",
            "quantity": quantity,
            'timestamp': timestamp
        }

        # create query string
        query_string = urlencode(params)
        logging.info('Query string: {}'.format(query_string))

        # signature
        signature = hmac.new(secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

        # url
        url = self._base_url + '/fapi/v1/order' + "?" + query_string + "&signature=" + signature

        # post request
        session = requests.Session()
        session.headers.update(
            {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": key}
        )
        response = session.post(url=url, params={})

        # get order id
        response_map = response.json()
        order_id = response_map.get('orderId')

        return order_id

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance



'''
Used for testing purposes only
'''
# if __name__ == '__main__':
#     binance_api = BinanceAdapter()
#     response = binance_api.get_market_data()
#     response = binance_api.get_account_info()
#     print(response)
