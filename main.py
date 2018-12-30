from price_data_collector import CoinTracker
import matplotlib.pyplot as plt

btc = CoinTracker('BTC')
btc.plot()
plt.show()