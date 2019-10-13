import requests
import pandas as pd
import datetime as dt


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

def get_klines(frequency: str, startTime: dt.datetime, endTime: dt.datetime):
	"""
	Function to retrieve historical price data from the Binance chain. 
	:param frequency: specify the frequency of the data. Allowed values from:
	[1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M]
	:param startTime: set the start time of the period to retrieve the data from
	:param endTime: set the end time of the period to retrieve the data from
	"""
	#Get list of symbols
	df = get_markets()
	base_asset_symbols = list(df['base_asset_symbol'])
	#Select pairs where quote symbol is BNB
	base_asset_symbols_excluding_BNB = []
	df_master=pd.DataFrame()
	for item in base_asset_symbols:
		if item!='BNB':
			base_asset_symbols_excluding_BNB.append(str(item)+'_BNB')
	startTime=int(startTime.strftime('%s'))*1000
	endTime=int(endTime.strftime('%s'))*1000
	for symbol in base_asset_symbols_excluding_BNB:
		response = requests.get('https://dex.binance.org/api/v1/klines?symbol=' + str(symbol) + '&interval=' + str(frequency) + '&startTime=' + str(startTime)+'&endTime=' +str(endTime) +'&limit=1000')
		if response.status_code == 200:
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
		else:
			print('Error retrieving kline data.')
	return df_master