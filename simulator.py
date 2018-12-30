from price_data_collector import CoinTracker
from technical_analysis import Rsi, Macd
from orders import BuyOrder


class SimulationStrategy:
    def __init__(self):
        self.btc = CoinTracker('BTC', 'hour')
        self.macd = Macd(self.btc)
        self.rsi = Rsi(self.btc)

        self.current_macd_advice = 0
        self.current_rsi_advice = 0
        self.duration_threshold = 24 * 5 #5 days wait before placing next buy order

        self.current_step = 30
        self.last_buy_order_step = 0
        self.last_sell_order_step = 0

    def collect_advise(self, step_size):
        madvice = self.macd.get_advice(self.current_step, step_size)
        radvice = self.rsi.get_advice(self.current_step, step_size)

        if madvice.advice > 0:
            self.current_macd_advice = 'BUY'
        elif madvice.advice < 0:
            self.current_macd_advice = 'SELL'

        if radvice.advice > 0:
            self.current_rsi_advice = 'BUY'
        elif radvice.advice < 0:
            self.current_rsi_advice = 'SELL'

    def step(self, buy_budget, past_buy_orders, step_size=2):
        self.collect_advise(step_size)
        duration_threshold_passed = self.current_step - self.last_buy_order_step > self.duration_threshold

        self.current_step += step_size
        if self.current_macd_advice == 'BUY' and self.current_rsi_advice == 'BUY' \
                and duration_threshold_passed and buy_budget > 50:
            current_price = self.btc.raw_data[self.current_step]
            self.last_buy_order_step = self.current_step
            return BuyOrder(50, current_price, 'BTC')


class StrategySimulator:
    def __init__(self):
        self.budget = 700
        self.s = SimulationStrategy()
        self.buy_orders = []
        self.btc = CoinTracker('BTC', 'hour')

    def get_buy_order_profit(self, step):
        profit = 0
        current_price = self.btc.raw_data[step]
        for o in self.buy_orders:
            profit += o.get_current_profit(current_price)
        return profit

    def simulate(self, num_steps):
        step = 0
        step_size = 2
        while step < num_steps:
            order = self.s.step(self.budget, self.buy_orders, step_size) #Each step consists of 2 hours
            if type(order) == BuyOrder:
                self.buy_orders.append(order)
                self.budget -= order.total_price

            if step % 24 == 0: #Daily profit
                profit = self.get_buy_order_profit(step)
                print(f"Step {step}, BuyOrders: {len(self.buy_orders)}, Budget: {self.budget}, Profit: {profit}")

            step += step_size