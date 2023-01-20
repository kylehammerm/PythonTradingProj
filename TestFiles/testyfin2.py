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

stock_symbol = 'NVDA'

data_df = yf.download(stock_symbol, start=start_date, end=curr_date, interval=interval)
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

def mock_bot(wallet: int, time: str, verbose: bool):
    stock = 0
    history = []
    for i in range(len(data_df['Signal'])):
        f = i + (0 if time == 'Close' else 1)
        try:
            match data_df['Signal'][f]:
                case 0:
                    print(f"[UNCLEAR] Holding: {data_df[time][f]}")
                case 1:
                    print(f"[BEARISH] Selling: {data_df[time][f]}")
                    wallet += stock * data_df[time][f]
                    stock = 0
                case 2:
                    print(f"[BULLISH] Buying: {data_df[time][f]}")
                    newStock = wallet // data_df[time][f]
                    wallet -= data_df[time][f] * newStock
                    stock += newStock
        except IndexError:
            pass
        history.append({'wallet': wallet, 'stock': stock});

    wallet += stock * data_df[time][len(data_df[time])-1]
    if verbose:
        print(history)
    return wallet


initial = 1000
w1 = mock_bot(initial, 'Open', 0)
w2 = mock_bot(initial, 'Close', 0)

print(w1, w2, w1-w2)
print((w1-initial)/initial*100, (w2-initial)/initial*100, (w1-w2)/initial*100)
