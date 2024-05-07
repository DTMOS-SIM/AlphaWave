from infrastructure.interface.Binance.Iwallet import IWallet
from infrastructure.interface.Iasset import IAsset
from infrastructure.interface.Iindicator import IIndicator
from infrastructure.interface.Iportfolio import IPortfolio
from infrastructure.utility.Adapters.binance_adapter import BinanceAdapter


class Portfolio(IPortfolio):

    def __init__(self, indicators: [IIndicator], assets: [IAsset], wallet: IWallet):
        self.combined_signals = []
        self.indicators = indicators
        self.assets = assets
        self.wallet = wallet

    def get_notional(self):
        return self._notional

    def set_notional(self, notional):
        self._notional = notional

    def generate_signals(self):

        try:
            new_timestamp = []
            for asset in self.assets:
                temp_indicator = 0
                for indicator in self.indicators:
                    signal = indicator.calculate()
                    temp_indicator += signal
                # Finalise intended signal base on TAs
                new_timestamp.append(temp_indicator)
            return new_timestamp

        except TypeError:
            raise TypeError

    def filter_signals(self, indicators: []):

        for i in range(len(indicators)):
            if indicators[i] > 0:
                indicators[i] = 1
            elif indicators[i] < 0:
                indicators[i] = -1
            else:
                indicators[i] = 0

        self.combined_signals.append(indicators)

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

    def buy_assets(self):
        pass

    def __del__(self):
        pass