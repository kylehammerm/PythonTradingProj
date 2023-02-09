import Trader1
import yfinance as yf
import datetime as dt

def signal_generator(df):
    # Gets the open and close for today
    o = df.Open.iloc[-1]
    c = df.Close.iloc[-1]

    # Gets the open and close from yesterday
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]

    # Bearish Pattern
    if o > c and c < previous_open < previous_close <= o:
        return 1

    # Bullish Pattern
    elif o < c and c > previous_open > previous_close >= o:
        return 2

    # No clear Pattern
    else:
        return 0


interval = '1h'
# gets the dates we will use
start = dt.datetime(2021, 2, 9)
end = dt.datetime(2023, 2, 8)

Stock = yf.download('TSLA', start=start, end=end, interval=interval)

k = Trader1.Trader(10000, Stock['Open'][0])

for i in range(1, len(Stock)):
    # Gets last two days
    df = Stock[i - 1:i + 1]
    k.singalInterp(signal_generator(df), Stock['Open'][i])

k.report()
