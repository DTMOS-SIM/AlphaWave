from infrastructure.interface.Binance.Iwallet import IWallet
from infrastructure.utility.Adapters.binance_adapter import BinanceAdapter


class Wallet(IWallet):

    def __init__(self, fee_tier: float, total_wallet_balance: float, total_unrealized_profit: float,
                 total_marginal_balance: float, total_cross_wallet_balance: float, available_balance: float,
                 max_withdrawal_amount: float):
        self.fee_tier = fee_tier
        self.total_wallet_balance = total_wallet_balance
        self.total_unrealized_profit = total_unrealized_profit
        self.total_marginal_balance = total_marginal_balance
        self.total_cross_wallet_balance = total_cross_wallet_balance
        self.available_balance = available_balance
        self.max_withdrawal_amount = max_withdrawal_amount

    def update_account(self) -> None:
        binance_client = BinanceAdapter()
        response = binance_client.get_account_info()
        self.fee_tier = response['feeTier']
        self.total_wallet_balance = response['totalWalletBalance']
        self.total_unrealized_profit = response['totalUnrealizedProfit']
        self.total_marginal_balance = response['totalMarginalBalance']
        self.total_cross_wallet_balance = response['totalCrossWalletBalance']
        self.available_balance = response['availableBalance']
        self.max_withdrawal_amount = response['maxWithdrawalAmount']

    def get_notional(self) -> float:
        return self.total_wallet_balance

    def __del__(self):
        pass

