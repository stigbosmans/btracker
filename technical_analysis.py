from finta import TA
import matplotlib.pyplot as plt
import pandas as pd
from price_data_collector import CoinTracker
from util import in_notebook, find_intersection
import numpy as np
if in_notebook():
    import plotly.graph_objs as go
    import plotly.offline as py
    from plotly.offline import init_notebook_mode
    init_notebook_mode(connected=True)


class Advice:
    def __init__(self, advice: int, indicator_type:str):
        """

        :param advice: >0=buy, 0=hold, <0=sell
        """
        self.advice = advice
        self.indicator_type = indicator_type

    def __repr__(self):
        if self.advice > 0:
            return f"{self.indicator_type} advice: Buy"
        elif self.advice < 0:
            return f"{self.indicator_type} advice: Sell"
        else:
            return f"{self.indicator_type} advice: Hold"


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

    def get_advice(self, from_step, duration=2):
        macd = np.array(self.data["MACD"])[from_step: from_step + duration]
        signal = np.array(self.data["SIGNAL"])[from_step: from_step + duration]
        id, is_type = find_intersection(macd, signal)
        if is_type == 0:
            return Advice(0, 'MACD')
        elif is_type == 1:
            return Advice(1, 'MACD')
        elif is_type == -1:
            return Advice(-1, 'MACD')


class Rsi(Indicator):
    def __init__(self, coin_tracker: CoinTracker):
        super().__init__(coin_tracker)
        self.data = TA.RSI(coin_tracker.get_ohlc())

    def get_advice(self, from_step, duration=2):
        dat = np.array(self.data)[from_step: from_step + duration]
        if len(dat[dat >= 70]) > 0:
            return Advice(-1, 'RSI')
        elif len(dat[dat <= 30]) > 0:
            return Advice(1, 'RSI')
        else:
            return Advice(0, 'RSI')

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
