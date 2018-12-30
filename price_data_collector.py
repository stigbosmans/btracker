from cryptocompy import coin, price
from util import in_notebook
import pandas as pd
import numpy as np
if in_notebook():
    import plotly.graph_objs as go
    import plotly.offline as py
    from plotly.offline import init_notebook_mode
    init_notebook_mode(connected=True)
else:
    import matplotlib.pyplot as plt


def get_price_data(coin='BTC', frequency='hour', limit=2000):
    """
    :param coin: BTC | ETH | ..
    :param frequency: hour | minute | day
    :param limit:
    :return:
    """
    res = price.get_historical_data(coin, "USD", frequency, limit=limit)
    res = pd.DataFrame(res)
    return res


class CoinTracker:
    def __init__(self, coin_name, frequency='hour'):
        self.coin_name = coin_name
        self.history = get_price_data(coin_name, frequency)
        self.raw_data = np.array(self.history[["close"]])

    def get_size(self):
        return len(self.raw_data)

    def get_ohlc(self):
        return self.history[["open", "high", "low", "close"]]

    def get_dates(self):
        return self.history["time"]

    def plot(self, limit=200):
        if in_notebook():
            trace = go.Ohlc(x=self.history['time'].iloc[-limit:],
                            open=self.history['open'].iloc[-limit:],
                            high=self.history['high'].iloc[-limit:],
                            low=self.history['low'].iloc[-limit:],
                            close=self.history['close'].iloc[-limit:])
            py.iplot([trace])
        else:
            plt.title(f"{self.coin_name} Price Data")
            plt.plot(range(limit), self.get_ohlc().iloc[-limit:])
