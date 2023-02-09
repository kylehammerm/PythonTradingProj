import datetime as dt
from matplotlib import pyplot as plt
import yfinance as yf


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


curr_date = '2023-01-19'
start_date = '2022-12-10'
interval = '2m'

stock_symbol = 'PLTR'

data_df = yf.download(stock_symbol, start=start_date, end=curr_date, interval=interval)
print(type(data_df))

signal = [0]
for i in range(1, len(data_df)):
    # Gets last two days
    df = data_df[i - 1:i + 1]

    # Generates the signal for the two days
    signal.append(signal_generator(df))

# Adds the signals to the data frame
data_df['Signal'] = signal

print(data_df.Signal.value_counts())


def mock_bot(wallet: int, time: str, verbose: bool):
    stock = 0
    total_stock = 0
    history = []
    for i in range(len(data_df['Signal'])):
        f = i + (0 if time == 'Close' else 1)
        try:
            match data_df['Signal'][f]:
                case 0:
                    if verbose:
                        print(f"[UNCLEAR] Holding: {data_df[time][f]}")
                case 1:
                    if verbose:
                        print(f"[BEARISH] Selling: {data_df[time][f]}")
                    wallet += stock * data_df[time][f]
                    stock = 0
                case 2:
                    if verbose:
                        print(f"[BULLISH] Buying: {data_df[time][f]}")
                    newStock = wallet / data_df[time][f]
                    wallet -= data_df[time][f] * newStock
                    stock += newStock
                    total_stock += newStock
        except IndexError:
            pass
        history.append({'wallet': wallet, 'stock': stock})

    wallet += stock * data_df[time][len(data_df[time]) - 1]
    if verbose:
        print(history)
    return wallet, total_stock, history


initial = 1000
w1, t1, h1 = mock_bot(initial, 'Open', False)
w2, t2, h2 = mock_bot(initial, 'Close', False)

print(f"Open Strategy: ${w1}", f"Close Strategy: ${w2}", f"Difference: ${w1 - w2}")
print(f"Open Strategy Gain: {(w1 - initial) / initial * 100}%",
      f"Close Strategy Gain: {(w2 - initial) / initial * 100}%", f"Difference: {(w1 - w2) / initial * 100}%")
print(f"Total Stock Open Strategy: {t1}", f"Total Stock Close Strategy: {t2}", f"Difference: {t1 - t2}")
color = "g"
for i in range(1, len(signal)):

    # decides the color based on whether we are holding the stock or not
    if h1[i]["stock"] > 0:
        color = "g"
    elif h1[i]["stock"] == 0:
        color = "r"
    else:
        color = color
    # red means don't have the stock green means we own it
    plt.plot([i - 1, i], [data_df['Close'][i - 1], data_df['Close'][i]], color=color)
plt.show()
