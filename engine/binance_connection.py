import requests
from pandas.io.json import json_normalize
import pandas as pd
import datetime as dt
from itertools import tee
from typing import Iterable, Tuple, TypeVar
import pickle

from engine.get_pairs_universe import basket_universe
from ratelimit import limits

#Get pairs universe
pairs_universe = basket_universe(10)
frequency = '1m'
startTime = dt.datetime.strptime("1/1/19 00:00", "%d/%m/%y %H:%M")
start= int(startTime.strftime("%s"))*1000
endTime = dt.datetime.now()
end = int(endTime.strftime("%s"))*1000

T = TypeVar('T')

def generate_time_pairs(start: dt.datetime, end: dt.datetime) -> Iterable[int]:
	"""
	Function to generate a list of timestamps such that requests are broken down into requests of 1000 datapoints. 
	Assuming that data is 1m.	
	"""
	start_unix = int(start.strftime("%s"))
	end_unix = int(end.strftime("%s"))
	#Generate difference between times in seconds
	difference = end_unix - start_unix
	if difference > 60000:
		bins = int(difference/60000 + 1)
		for i in range(bins):
			yield start_unix + 60000 * i
		yield end_unix

def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T,T]]:
	x, y = tee(iterable)
	next(y, None)
	return zip(x, y)

#Make exlusive timestamp categories
timestamp_list = list(pairwise(generate_time_pairs(dt.datetime(2019,1,1), dt.datetime(2019,10,22))))
ranges = []
for window in timestamp_list:
	couple = (window[0]*1000+1, window[1] * 1000)
	ranges.append(couple)

@limits(calls = 10, period = 1)
def dataset_extractor():
	"""
	Extracts all 1m kline data from the Binance API and stores it as a pickle file.
	"""
	df_master = pd.DataFrame()
	#Retrieve historical data from Binance for the pairs
	for pair in pairs_universe:
		for window in ranges:
			response = requests.get('https://api.binance.com/api/v1/klines?symbol=' + str(pair) + '&interval=' + str(frequency) + '&startTime='+str(window[0])+'&endTime='+str(window[1]))
			print(response.status_code)
			if response.status_code != 200:
				# This means something went wrong.
				print('Error ' + str(response.status_code) + ' returned from Binance.')
			else:
				df = pd.DataFrame.from_records(response.json(), columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
				df['pair']=pair
				df['Open time']=df['Open time'].astype(float)
				df['Open'] = df['Open'].astype(float)
				df['High'] = df['High'].astype(float)
				df['Low'] = df['Low'].astype(float)
				df['Close'] = df['Close'].astype(float)
				df['Volume'] = df['Volume'].astype(float)
				df['Close time'] = df['Quote asset volume'].astype(float)
				df['Number of trades'] = df['Taker buy base asset volume'].astype(float)
				df['Taker buy quote asset volume'] = df['Taker buy quote asset volume'].astype(float)
				df['Ignore'] = df['Ignore'].astype(float)
				df_master = df_master.append(df, ignore_index=True)
	df_master.to_pickle("./kline_data.pkl")


