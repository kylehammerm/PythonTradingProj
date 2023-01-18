import yfinance as yf
import pandas as pd

# define some variables we are using
curDate = "2023-1-18"
startDate = "2023-1-1"
interval = '1d'
# Ticker we are using
stock = "TSLA"


# says whether to buy or sell
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


# gets the data for our interval
dataF = yf.download(stock, start=startDate, end=curDate, interval=interval)
print(type(dataF))

sig = []
sig.append(0)

for i in range(1, len(dataF)):
    # gets last two days
    df = dataF[i - 1:i + 1]
    # generates signal for the last two days
    sig.append(signal_generator(df))

# adds our sig to our pandas data
dataF["signal"] = sig
print(dataF.signal.value_counts())
