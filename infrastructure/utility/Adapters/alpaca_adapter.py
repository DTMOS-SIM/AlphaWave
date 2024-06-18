from infrastructure.interface.IAdapter import GenericAdapter
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


class AlpacaAdapter(GenericAdapter, object):

    instance = None

    def __init__(self):
        self._api_key = 'PKIRI9RL2ZS8I1ZXPWNG'
        self._secret_key = 'VJz9mVeshTea2VzvZPWAXKRh3sWZp7yyZEGNmPVL'
        self._hedging_client = TradingClient(self._api_key, self._secret_key)

    def get_credentials(self):
        return self._api_key, self._secret_key

    def get_account_info(self):
        response = self._hedging_client.get_account()
        return response

    def get_asset_data(self, symbol):
        return self._hedging_client.get_asset(symbol_or_asset_id=symbol)

    def transact_assets(self, symbol: str, qty: float, side: str, position_side: str):
        # preparing orders
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            type='MARKET',
            side=OrderSide.BUY if side == 'BUY' else OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )

        # Market order
        market_order = self._hedging_client.submit_order(
            order_data=market_order_data
        )

        return market_order

    def __del__(self):
        pass