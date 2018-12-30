
class BuyOrder:
    def __init__(self, total_price:float, price_per_unit:float, coin:str):
        self.total_price = total_price
        self.price_per_unit = price_per_unit
        self.units = self.total_price / self.price_per_unit
        self.coin = coin

    def get_current_profit(self, current_price_per_unit:float):
        price_difference_per_unit = current_price_per_unit - self.price_per_unit
        profit = self.units * price_difference_per_unit
        return profit

    def get_profit_factor(self, current_price_per_unit:float):
        profit = self.get_current_profit(current_price_per_unit)
        return profit / self.total_price