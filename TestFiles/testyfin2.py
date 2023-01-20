
import pandas as pd

import yfinance as yf
from yahoofinancials import YahooFinancials

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


curr_date = '2023-01-01'
start_date = '2022-12-01'
interval = '2m'

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
data_df['Signal'] = signal

print(data_df.Signal.value_counts())

stock_total = 0
stock = 0
wallet = 1000
for i in range(len(data_df['Signal'])):
    match data_df['Signal'][i]:
        case 0:
            print(f"[UNCLEAR] Holding: {data_df['Close'][i]}")
        case 1:
            print(f"[BEARISH] Selling: {data_df['Close'][i]}")
            wallet += stock * data_df['Close'][i]
            stock = 0
        case 2:
            print(f"[BULLISH] Buying: {data_df['Close'][i]}")
            newStock = wallet // data_df['Close'][i]
            wallet -= data_df['Close'][i] * newStock
            stock += newStock
            stock_total += stock


wallet += stock * data_df['Close'][len(data_df['Close'])-1]
print(wallet, stock_total)
