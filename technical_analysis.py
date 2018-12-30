from finta import TA
import matplotlib.pyplot as plt
import pandas as pd
from price_data_collector import CoinTracker
from util import in_notebook
if in_notebook():
    import plotly.graph_objs as go
    import plotly.offline as py
    from plotly.offline import init_notebook_mode
    init_notebook_mode(connected=True)


class Indicator:
    def __init__(self, coin_tracker: CoinTracker):
        self.coin_tracker = coin_tracker
        self.data = pd.DataFrame()

    def plot(self, limit):
        if in_notebook():
            data = go.Scatter(x=self.coin_tracker.get_dates().iloc[-limit:], y=self.data)
            py.iplot([data])
        else:
            plt.plot(range(limit), self.data.iloc[-limit:].values, 'r-')


class Macd(Indicator):
    def __init__(self, coin_tracker: CoinTracker):
        super().__init__(coin_tracker)
        self.data = TA.MACD(coin_tracker.get_ohlc())

    def plot(self, limit):
        if in_notebook():
            dates = self.coin_tracker.get_dates().iloc[-limit:]
            macd = go.Scatter(x=dates, y=self.data["MACD"].iloc[-limit:].values, name="MACD")
            signal = go.Scatter(x=dates, y=self.data["SIGNAL"].iloc[-limit:].values, name="SIGNAL")
            l = go.Layout(title=f"{self.coin_tracker.coin_name} MACD")
            py.iplot(go.Figure(data=[macd, signal], layout=l))
        else:
            plt.title("MACD")
            plt.plot(range(limit), self.data["MACD"].iloc[-limit:].values, label="MACD")
            plt.plot(range(limit), self.data["SIGNAL"].iloc[-limit:].values, label="SIGNAL")
            plt.legend()


class Rsi(Indicator):
    def __init__(self, coin_tracker: CoinTracker):
        super().__init__(coin_tracker)
        self.data = TA.RSI(coin_tracker.get_ohlc())

    def get_events(self):
        pass

    def plot(self, limit):
        if in_notebook():
            dates = self.coin_tracker.get_dates().iloc[-limit:]
            data = go.Scatter(x=dates, y=self.data, name="RSI")
            upper = go.Scatter(x=dates, y=[70 for i in range(len(dates))], name="Upper bound")
            lower = go.Scatter(x=dates, y=[30 for i in range(len(dates))], name="Lower bound")
            l = go.Layout(title=f"{self.coin_tracker.coin_name} RSI")
            py.iplot(go.Figure(data=[data, upper, lower], layout=l))
        else:
            plt.title("RSI")
            plt.plot(range(limit), [70 for i in range(limit)], 'b-')
            plt.plot(range(limit), [30 for i in range(limit)], 'b-')
            super().plot(limit)
