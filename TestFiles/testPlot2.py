import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import style
import yfinance as yf


def signal_generator(dataframe):
    # Gets the open and close of the last day
    open = dataframe.Open.iloc[-1]
    close = dataframe.Close[-1]

    # Gets the open and close of the day before last
    prevOpen = dataframe.Open.iloc[-2]
    prevClose = dataframe.Close[-2]

    # looks for a bearish pattern
    if open > close and prevOpen < prevClose and close < prevOpen and open >= prevClose:
        return 1
    # looks for bullish pattern
    elif open < close and prevOpen > prevClose and close > prevOpen and open <= prevClose:
        return 2
    # no clear pattern
    else:
        return 0


interval = '1d'
# gets the dates we will use
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2022, 2, 2)

Stock = yf.download('GE', start=start, end=end, interval=interval)
style.use('ggplot')

signal = [0]
for i in range(1, len(Stock)):
    # Gets last two days
    df = Stock[i - 1:i + 1]
    # Generates the signal for the two days
    signal.append(signal_generator(df))

color = "g"
for i in range(1, len(signal)):

    # decides the color based on whether we are holding the stock or not
    if signal[i] == 1:
        color = "r"
    elif signal[i] == 2:
        color = "g"
    else:
        color = color
    # red means don't have the stock green means we own it
    plt.plot([i - 1, i], [Stock['Close'][i - 1], Stock['Close'][i]], color=color)
plt.show()
