import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import style
import yfinance as yf

interval = '1d'
# gets the dates we will use
start = dt.datetime(2022, 1, 1)
end = dt.datetime(2022, 2, 2)

# gets the data
Stock = yf.download('TSLA', start=start, end=end, interval=interval)

style.use('ggplot')
Stock['Close'].plot(figsize=(8, 8), label='Tesla')
plt.show()
