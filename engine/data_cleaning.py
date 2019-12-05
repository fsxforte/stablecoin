import pickle
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import seaborn as sns

from engine.generic_functions import resample

def load_from_pickle():
	'''
	Function to load cached data from pickle file. 
	'''
	#Import raw data
	file = open("./data/kline_data_new.pkl", 'rb')
	df = pickle.load(file)

	#Basic data processing
	df = df.sort_values(['close_time'])
	df['datetime']=pd.to_datetime(df['close_time'], unit='ms')

	return df

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

def universe_selection_on_volume(num_assets: int, start_date: dt.datetime, end_date: dt.datetime):
	'''
	Function to return a dataframe for pairs with the most liquidity, measured by 'vol'.
	'''
	df = load_from_pickle()
	volumes = pd.pivot_table(df, values='volume', index=['close_time'], columns=['symbol'])
	volumes['date']=pd.to_datetime(volumes.index, unit = 'ms')
	volumes = volumes.set_index('date')
	#Filter dataframe based on time window
	avg = volumes[start_date:end_date].mean().dropna()
	selected_symbols = list(avg.nlargest(num_assets).index)

	return selected_symbols

def data_explorer(variable_of_interest: str, selected_symbols, start_date: dt.datetime, end_date: dt.datetime):
	'''
	Function to explore the data. 
	:variable: variable to plot, e.g. 'close'
	:start_date: date at which to begin plots, in format dt.datetime(2019,1,1)
	:end_date: date at which to end plots, in format dt.datetime(2019,1,1)
	:frequency: frequency to resample data at, e.g. 'H' for hourly
	:number_symbols: the number of symbols to look at at a glance, starting with 
	'''
	df = load_from_pickle()
	df_var = pd.pivot_table(df, values=variable_of_interest, index=['close_time'], columns=['symbol'])
	df_var['date'] = pd.to_datetime(df_var.index, unit = 'ms')
	df_var = df_var.set_index('date')
	df_var = df_var[start_date:end_date]
	#Exploratory plots
	fig, ax = plt.subplots()
	df_var[selected_symbols].plot(ax = ax)
	ax.set_ylabel(str(variable_of_interest), fontsize = 16)
	ax.tick_params(axis='both', which='major', labelsize=16)
	plt.title('Exploratory plot of ' + str(variable_of_interest), fontsize = 16)
	ax.legend()	
	plt.show()

def df_make(variable_of_interest: str, selected_symbols, start_date: dt.datetime, end_date: dt.datetime):
	'''
	Function to explore the data. 
	:variable: variable to plot, e.g. 'close'
	:start_date: date at which to begin plots, in format dt.datetime(2019,1,1)
	:end_date: date at which to end plots, in format dt.datetime(2019,1,1)
	:frequency: frequency to resample data at, e.g. 'H' for hourly
	:number_symbols: the number of symbols to look at at a glance, starting with 
	'''
	df = load_from_pickle()
	df_var = pd.pivot_table(df, values=variable_of_interest, index=['close_time'], columns=['symbol'])
	df_var['date'] = pd.to_datetime(df_var.index, unit = 'ms')
	df_var = df_var.set_index('date')
	df_var = df_var[selected_symbols]
	df_var = df_var[start_date:end_date]

	return df_var

def visualize_heatmap(df, n_largest: int, start_date: dt.datetime, end_date: dt.datetime):
	'''
	Visualize a heatmap of the correlations between assets.
	:df: input dataframe, created using load_from_pickle function
	:n_largest: select the n_largest pairs to focus on, in terms of average daily volume
	:start_date: start date for the period, in dt.datetime format
	:end_date: end date for the period, in dt.datetime format
	'''
	volumes = variable_extractor('volume', df, 'D')
	avg = volumes[start_date:end_date].mean().dropna()
	n = n_largest
	selected_symbols = list(avg.nlargest(n).index)
	close_prices = variable_extractor('close', df, 'D')
	data = close_prices[[column for column in close_prices.columns if column in selected_symbols]]
	returns = data.pct_change()
	sns.heatmap(returns.corr())
	plt.show()


