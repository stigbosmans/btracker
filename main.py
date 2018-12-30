from price_data_collector import CoinTracker
from technical_analysis import Rsi, Macd
import matplotlib.pyplot as plt

btc = CoinTracker('BTC')
macd = Macd(btc)
macd.plot(100)
plt.show()
macd.get_advice(1930, 5)