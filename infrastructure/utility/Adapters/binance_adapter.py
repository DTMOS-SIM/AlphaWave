import logging
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from infrastructure.interface.IAdapter import GenericAdapter
from binance.cm_futures import CMFutures


class BinanceAdapter(GenericAdapter):

    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BinanceAdapter, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._base_url = 'https://testnet.binancefuture.com'
        self._api_key = 'b8e0a5bc6ccfe44e8458f633c9c7e12859f181a5cbc23db42d2a03bc851b63b7'
        self._secret_key = 'af61a6188b81f0038715e0ae5837333fa39772c8114641d5e013a15d8c26fa12'
        self._futures_client = CMFutures(key=self._api_key, secret=self._secret_key, base_url=self._base_url)

    def get_credentials(self):
        return self._base_url, self._api_key, self._secret_key

    def get_account_info(self):
        return self._futures_client.account()

    def get_asset_data(self):
        return (self._futures_client.account())['assets']

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



'''
Used for testing purposes only
'''
# if __name__ == '__main__':
#     binance_api = BinanceAdapter()
#     response = binance_api.get_account_info()
#     for currency in response['assets']:
#         print(currency['asset']),
#         print(currency['walletBalance']),
#         print(currency['marginBalance']),
#         print(currency['availableBalance']),
#         print(currency['maxWithdrawAmount'])
