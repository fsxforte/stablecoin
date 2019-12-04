import requests
import pandas as pd
import datetime as dt
from ratelimit import limits
import pickle

from engine.generic_functions import pairwise, generate_time_pairs

def get_tokens():
	"""
	Function returns a list of tokens on the Binance Chain. 
	:Return: dataframe of tokens, and additional information.
	"""
	response = requests.get('https://dex.binance.org/api/v1/tokens')
	if response.status_code == 200:
		df = pd.DataFrame.from_records(response.json())
	elif response.status_code == 400:
		print('Bad request.')
	elif response.status_code == 404:
		print('Not found.')
	return df


def get_markets():
	"""
	Function returns a list of tokens on the Binance Chain. 
	:Return: dataframe of tokens, and additional information.
	"""
	response = requests.get('https://dex.binance.org/api/v1/markets')
	if response.status_code == 200:
		df = pd.DataFrame.from_records(response.json())
	elif response.status_code == 400:
		print('Bad request.')
	elif response.status_code == 404:
		print('Not found.')
	return df


@limits(calls = 10, period = 1)
def get_all_1m_klines():
	"""
	Function to retrieve historical price data from the Binance chain. 
	:param frequency: specify the frequency of the data. Allowed values from:
	[1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M]
	:param startTime: set the start time of the period to retrieve the data from
	:param endTime: set the end time of the period to retrieve the data from
	"""

	#Make exlusive timestamp categories
	timestamp_list = list(pairwise(generate_time_pairs(dt.datetime(2019,1,1), dt.datetime(2019,12,1))))
	ranges = []
	for window in timestamp_list:
		couple = (window[0]*1000+1, window[1] * 1000)
		ranges.append(couple)

	#Get list of symbols
	df = get_markets()
	base_asset_symbols = list(df['base_asset_symbol'])

	#Select pairs where quote symbol is BNB
	base_asset_symbols_excluding_BNB = []
	df_master=pd.DataFrame()
	for item in base_asset_symbols:
		if item!='BNB':
			base_asset_symbols_excluding_BNB.append(str(item)+'_BNB')

	for symbol in base_asset_symbols_excluding_BNB:
		for window in ranges:
			response = requests.get('https://dex.binance.org/api/v1/klines?symbol=' + str(symbol) + '&interval=1m' + '&startTime=' + str(window[0])+'&endTime=' +str(window[1]) +'&limit=1000')
			if response.status_code != 200:
				print('Error code ' + str(response.status_code) + 'received')
			elif response.status_code == 200:
				df = pd.DataFrame.from_records(response.json(), columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades'])
				df['symbol']=str(symbol)
				df['open_time']=pd.to_numeric(df['open_time'])
				df['open']=pd.to_numeric(df['open'])
				df['high']=pd.to_numeric(df['high'])
				df['low']=pd.to_numeric(df['low'])
				df['close']=pd.to_numeric(df['close'])
				df['volume']=pd.to_numeric(df['volume'])
				df['close_time']=pd.to_numeric(df['close_time'])
				df['quote_asset_volume']=pd.to_numeric(df['quote_asset_volume'])
				df['number_of_trades']=pd.to_numeric(df['number_of_trades'])
				df_master=df_master.append(df)
				print(df_master)

	pickle_out = open("./data/kline_data_new.pkl","wb")
	pickle.dump(df_master, pickle_out)
	pickle_out.close()


# def dataset_extractor():
# 	"""
# 	Extracts all 1m kline data from the Binance API and stores it as a pickle file.
# 	"""
# 	df_master = pd.DataFrame()
# 	#Retrieve historical data from Binance for the pairs
# 	for pair in pairs_universe:
# 		for window in ranges:
# 			response = requests.get('https://api.binance.com/api/v1/klines?symbol=' + str(pair) + '&interval=' + str(frequency) + '&startTime='+str(window[0])+'&endTime='+str(window[1]))
# 			print(response.status_code)
# 			if response.status_code != 200:
# 				# This means something went wrong.
# 				print('Error ' + str(response.status_code) + ' returned from Binance.')
# 			else:
# 				df = pd.DataFrame.from_records(response.json(), columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
# 				df['pair']=pair
# 				df['Open time']=df['Open time'].astype(float)
# 				df['Open'] = df['Open'].astype(float)
# 				df['High'] = df['High'].astype(float)
# 				df['Low'] = df['Low'].astype(float)
# 				df['Close'] = df['Close'].astype(float)
# 				df['Volume'] = df['Volume'].astype(float)
# 				df['Close time'] = df['Quote asset volume'].astype(float)
# 				df['Number of trades'] = df['Taker buy base asset volume'].astype(float)
# 				df['Taker buy quote asset volume'] = df['Taker buy quote asset volume'].astype(float)
# 				df['Ignore'] = df['Ignore'].astype(float)
# 				df_master = df_master.append(df, ignore_index=True)
# 	df_master.to_pickle("./kline_data.pkl")