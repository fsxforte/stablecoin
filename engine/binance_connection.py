import requests
from pandas.io.json import json_normalize

from engine.get_pairs_universe import basket_universe

#Get pairs universe
pairs_universe = basket_universe(10)

#Retrieve historical data from Binance for the pairs
for pair in pairs_universe:
	response = requests.get('https://api.binance.com/api/v1/klines?symbol=' + str(pair) + '&interval=1h')
	print(response.status_code)
	if response.status_code != 200:
		# This means something went wrong.
		print('Error ' + str(response.status_code) + ' returned from Binance.')