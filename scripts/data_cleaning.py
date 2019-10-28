import pickle
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import seaborn as sns

from engine.generic_functions import resample

#Import raw data
file = open("./data/kline_data.pkl", 'rb')
df = pickle.load(file)

#Basic data processing
df = df.sort_values(['open_time'])
df['datetime']=pd.to_datetime(df['open_time'], unit='ms')


def variable_extractor(variable: str, df, frequency: str):
	"""
	Creates dataframe of values of key variable, rows are time and columns are symbols.
	:variable: specify the variable of interest, for example, 'open' or 'volume'
	:df: data input
	:frequency: frequency of resampled data, e.g. 'D' for daily

	"""
	#Extract list of unique symbols from dataset
	symbols = list(df['symbol'].unique())
	df_master=pd.DataFrame()
	for symbol in symbols:
		print(symbol)
		subset = df.loc[df['symbol'] == symbol]
		#Drop random duplicates in data
		subset.drop_duplicates(inplace=True)
		#Set dataframe index and frequency
		subset = subset.set_index('datetime')
		subset = subset.asfreq('T')
		#Resample data
		resampled_subset = resample(subset, frequency)
		col_of_interest = pd.DataFrame(resampled_subset[variable])
		col_of_interest = col_of_interest.rename(columns = {variable: str(symbol)})
		df_master = pd.concat([df_master, col_of_interest], axis = 1)
	return df_master

def data_explorer(start_date: dt.datetime, end_date: dt.datetime):
	#Compute MA volumes
	volumes = variable_extractor('volume', df, 'D')
	avg = volumes[start_date:end_date].mean().dropna()
	n = 10
	selected_symbols = list(avg.nlargest(n).index)
	#Exploratory plots
	for symbol in selected_symbols:
		subset = df.loc[df['symbol'] == symbol]
		#Drop random duplicates in data
		subset.drop_duplicates(inplace=True)
		#Set dataframe index and frequency
		subset = subset.set_index('datetime')
		subset = subset.asfreq('T')
		#Resample data
		resampled_subset = resample(subset, frequency)
		resampled_subset['symbol']=symbol
		resampled_subset['close'].plot()

def visualize_heatmap(n_largest: int, variable: str, start_date: dt.datetime, end_date: dt.datetime):
	volumes = variable_extractor(variable, df, 'D')
	avg = volumes[start_date:end_date].mean().dropna()
	n = n_largest
	selected_symbols = list(avg.nlargest(n).index)
	close_prices = variable_extractor('close', df, 'D')
	data = close_prices[[column for column in close_prices.columns if column in selected_symbols]]
	returns = data.pct_change()
	sns.heatmap(returns.corr())
	plt.show()


