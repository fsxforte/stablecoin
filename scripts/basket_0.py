import datetime as dt
import pandas as pd

from engine.binance_chain import get_klines

#Import data
df = get_klines('1h', dt.datetime(2019,9,1), dt.datetime(2019,9,30))

#Create returns matrix
close_prices = pd.pivot_table(df, values='close', index=['close_time'], columns=['symbol'])
returns = close_prices.pct_change()
