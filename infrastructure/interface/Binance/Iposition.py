class IPosition:

    def __init__(self):
        self.symbol = "BTCUSDT"
        self.initialMargin = 0
        self.maintMargin = 0
        self.unrealizedProfit = 0.00000000
        self.positionInitialMargin = 0
        self.openOrderInitialMargin = 0
        self.leverage = 100
        self.isolated = True
        self.entryPrice = 0.00000
        self.maxNotional = 250000
        self.bidNotional = 0
        self.askNotional = 0
        self.positionSide = "BOTH"
        self.positionAmt = 0
        self.updateTime = 0

    def add_pos(self):
        raise NotImplementedError

    def get_assets(self):
        raise NotImplementedError

    def get_notional(self):
        raise NotImplementedError

    def __del__(self):
        raise NotImplementedError
