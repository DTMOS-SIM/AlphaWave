import logging
from alpaca.data import StockLatestTradeRequest
from infrastructure.interface.IAdapter import GenericAdapter
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
from alpaca.common.exceptions import APIError
from alpaca.data.historical import StockHistoricalDataClient


class AlpacaAdapter(GenericAdapter, object):
    instance = None

    def __init__(self, api_key, api_secret):
        self._api_key = api_key
        self._secret_key = api_secret
        self._hedging_client = TradingClient(self._api_key, self._secret_key)
        self._hedging_market = StockHistoricalDataClient(self._api_key, self._secret_key)

    def get_credentials(self):
        return self._api_key, self._secret_key

    def get_account_info(self):
        response = self._hedging_client.get_account()
        return response

    def get_current_ticker_data(self, symbol: str):
        request_params = StockLatestTradeRequest(
            symbol_or_symbols=symbol
        )
        response = self._hedging_market.get_stock_latest_trade(request_params)[symbol].price
        return float(response)

    def get_asset_data(self, symbol):
        return self._hedging_client.get_asset(symbol_or_asset_id=symbol)

    def transact_assets(self, symbol: str, qty: float, side: str):
        try:
            # preparing orders
            market_order_data = MarketOrderRequest(
                symbol_or_symbols=symbol,
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
        except APIError as e:
            logging.error("Trade Execution Error: " + str(e.response))
            pass

    def get_all_orders(self, side: str):
        try:
            # params to filter orders by
            request_params = GetOrdersRequest(
                status=QueryOrderStatus.OPEN,
                side=OrderSide.SELL
            )

            # orders that satisfy params
            return self._hedging_client.get_orders(filter=request_params)
        except APIError as e:
            logging.error("Trade Execution Error: " + str(e.response))
            pass

    def cancel_all_orders(self):
        try:
            return self._hedging_client.cancel_orders()
        except APIError as e:
            logging.error("Trade Execution Error: " + str(e.response))
            pass

    def get_all_positions(self):
        try:
            return self._hedging_client.get_all_positions()
        except APIError as e:
            logging.error("Trade Execution Error: " + str(e.response))
            pass

    def close_all_positions(self):
        try:
            return self._hedging_client.close_all_positions(cancel_orders=True)
        except APIError as e:
            logging.error("Trade Execution Error: " + str(e.response))
            pass

    def __del__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance
