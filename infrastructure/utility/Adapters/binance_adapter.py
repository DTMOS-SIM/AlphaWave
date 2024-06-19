import logging
import time
import calendar
import pandas as pd
from datetime import datetime as dt

from binance.error import ClientError
from infrastructure.interface.currencyWeightsEnum import CurrencyWeights
from infrastructure.interface.IAdapter import GenericAdapter
from binance.um_futures import UMFutures


class BinanceAdapter(GenericAdapter, object):
    instance = None

    def __init__(self, api_key, api_secret):
        self._base_url = 'https://testnet.binancefuture.com'
        self._api_key = api_key
        self._secret_key = api_secret
        self._futures_client = UMFutures(key=self._api_key, secret=self._secret_key, base_url=self._base_url)

    def get_credentials(self):
        return self._base_url, self._api_key, self._secret_key

    def get_account_info(self):
        response = self._futures_client.account()
        return response, response['assets'], response['positions']

    def get_asset_data(self):
        pass

    def get_market_positions(self, symbol: str = None):
        try:
            response = self._futures_client.get_position_risk(symbol=symbol, recvWindow=6000)
            logging.info(response)
            return response
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def get_ticker_price(self, symbol: str):
        return float(self._futures_client.ticker_price(symbol=symbol)['price'])

    def get_market_data(self, interval: str):
        temp_dict = {}
        pairs = CurrencyWeights.list()

        temp_dict[pairs[0]] = self._futures_client.klines(pairs[0], interval)[-1][1:6]
        temp_dict[pairs[1]] = self._futures_client.klines(pairs[1], interval)[-1][1:6]
        temp_dict[pairs[2]] = self._futures_client.klines(pairs[2], interval)[-1][1:6]
        temp_dict[pairs[3]] = self._futures_client.klines(pairs[3], interval)[-1][1:6]
        temp_dict[pairs[4]] = self._futures_client.klines(pairs[4], interval)[-1][1:6]

        temp_dict = {key: list(map(float, value)) for key, value in temp_dict.items()}

        return temp_dict

    def get_specific_market_data(self, interval: str, pair_name: str):
        return list(map(float, self._futures_client.klines(symbol=pair_name, interval=interval)[-1][1:6]))

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

        # Completed
        logging.info(f'Finished getting initial data for T + {initial_interval}')
        return dict_temp

    def get_current_df_row(self, dict_temp: {}, pair) -> dict:
        final_table_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        response = self.get_specific_market_data("1h", pair)
        time_now = calendar.timegm((dt.utcnow()).utctimetuple())

        for x, y in dict_temp.items():
            dict_temp[x] = dict_temp[x].drop(index=dict_temp[x].index[0], axis=0)
            dict_temp[x] = dict_temp[x].drop(columns=[col for col in dict_temp[x] if col not in final_table_columns])
            dict_temp[x].loc[time_now] = response

        return dict_temp

    def __del__(self):
        pass

    def transact_assets(self, symbol: str, qty: float, side: str, position_side: str):

        try:
            response = self._futures_client.new_order(
                symbol=symbol,
                side=side,
                positionSide=position_side,
                type="MARKET",
                quantity=str(qty))
            logging.info('Sent Order: ', response)
            return response
        except Exception as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            return error.__str__()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance
