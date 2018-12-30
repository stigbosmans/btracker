from price_data_collector import CoinTracker
from technical_analysis import Rsi, Macd
import matplotlib.pyplot as plt
from simulator import StrategySimulator

btc = CoinTracker('BTC')
macd = Macd(btc)
macd.plot(100)
plt.show()

sim = StrategySimulator()
sim.simulate(2000)