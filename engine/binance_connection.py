import requests
from pandas.io.json import json_normalize
import pandas as pd
import datetime

from engine.get_pairs_universe import basket_universe

#Get pairs universe
pairs_universe = basket_universe(10)
frequency = '1h'
startTime = datetime.datetime.strptime("1/1/19 00:00", "%d/%m/%y %H:%M")
start= int(startTime.strftime("%s"))*1000
endTime = datetime.datetime.now()
end = int(endTime.strftime("%s"))*1000

df_master = pd.DataFrame()
#Retrieve historical data from Binance for the pairs
for pair in pairs_universe[:2]:
	response = requests.get('https://api.binance.com/api/v1/klines?symbol=' + str(pair) + '&interval=' + str(frequency) + '&startTime='+str(start)+'&endTime='+str(end))
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