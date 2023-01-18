
import pandas as pd

import yfinance as yf
from yahoofinancials import YahooFinancials

def signal_generator(df):
    # Gets the open and close for today
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]

    # Gets the open and close from yesterday
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]

    # Bearish Pattern
    if open > close and close < previous_open < previous_close <= open:
        return 1

    # Bullish Pattern
    elif open < close and close > previous_open > previous_close >= open:
        return 2

    # No clear Pattern
    else:
        return 0


curr_date = '2023-01-17'
start_date = '2023-01-01'
interval = '15m'

stock = 'TSLA'

data_df = yf.download(stock, start=start_date, end=curr_date, interval=interval)
print(type(data_df))

signal = [0]
for i in range(1, len(data_df)):
    # Gets last two days
    df = data_df[i-1:i+1]

    # Generates the signal for the two days
    signal.append(signal_generator(df))

# Adds the signals to the data frame
data_df['signal'] = signal

print(data_df.signal.value_counts())
