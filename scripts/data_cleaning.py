import pickle
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

from engine.generic_functions import resample

#Import data
file = open("./data/kline_data.pkl", 'rb')
df = pickle.load(file)

#Basic data processing
df = df.sort_values(['open_time'])
df['datetime']=pd.to_datetime(df['open_time'], unit='ms')

#Extract unique list of symbols
symbols = list(df['symbol'].unique())

#Select dataframe for a single symbol
subset = df.loc[df['symbol'] == symbols[0]]

#Set dataframe index and frequency
subset = subset.set_index('datetime')
subset = subset.asfreq('T')

#Resample data
resampled_subset = resample(subset, 'D')

#Exploratory plots
for symbol in symbols:
	subset = df.loc[df['symbol'] == symbol]
	#Set dataframe index and frequency
	subset = subset.set_index('datetime')
	subset = subset.asfreq('T')
	#Resample data
	resampled_subset = resample(subset, 'D')
	resampled_subset['number_of_trades'].plot()
