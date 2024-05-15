class Position:

    def __init__(self, symbol: str, initialMargin: float, maintMargin: float, unrealizedProfit: float, positionInitialMargin: float, openOrderInitialMargin: float,
                 leverage: float, isolated: bool, entryPrice: float, maxNotional: float, bidNotional: float, askNotional: float, positionSide: str, positionAmt: float, updateTime: float):
        self.symbol = symbol
        self.initialMargin = initialMargin
        self.maintMargin = maintMargin
        self.unrealizedProfit = unrealizedProfit
        self.positionInitialMargin = positionInitialMargin
        self.openOrderInitialMargin = openOrderInitialMargin
        self.leverage = leverage
        self.isolated = isolated
        self.entryPrice = entryPrice
        self.maxNotional = maxNotional
        self.bidNotional = bidNotional
        self.askNotional = askNotional
        self.positionSide = positionSide
        self.positionAmt = positionAmt
        self.updateTime = updateTime

    def add_pos(self):
        raise NotImplementedError

    def get_assets(self):
        raise NotImplementedError

    def get_notional(self):
        raise NotImplementedError

    def __del__(self):
        raise NotImplementedError
