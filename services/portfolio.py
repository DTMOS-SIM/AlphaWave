from infrastructure.interface.Binance.Iwallet import IWallet
from services.asset import Asset
from services.wallet import Wallet
from infrastructure.interface.Iportfolio import IPortfolio
from infrastructure.utility.Adapters.binance_adapter import BinanceAdapter
from infrastructure.utility.Indicators.ATR import ATR


class Portfolio(IPortfolio):

    def __init__(self, assets: [Asset], wallet: Wallet):
        self.combined_signals = []
        self.assets = assets
        self.wallet = wallet

    def get_notional(self):
        return self._notional

    def show_specs(self):
        print("Wallet Data: ")
        print(self.wallet)
        for asset in self.assets:
            name, weight, position, current_asset, ta = asset.asset_info()
            print("Asset Name: ", name)
            print("Asset Weight: ", weight)
            print("Asset Positions: ")
            print(position)
            print("Asset Current weight: ", current_asset)
            print("Asset Indicators: ")
            print(ta)

    def generate_signals(self):
        ATR().generate_signals()

    def set_notional(self, notional):
        self._notional = notional

    def compute_realized_allocation(self):
        # Get all the coins
        pass

    def sell_assets(self):
        latest_timestamp = self.combined_signals[:-1]
        for product in latest_timestamp:
            if product == -1:
                # Call binance API to sell off product
                # **Change BinanceAdapter to singleton call**
                BinanceAdapter().sell_assets(product)

    def filter_signals(self, indicators: []):
        pass

    def buy_assets(self):
        pass

    def __del__(self):
        pass