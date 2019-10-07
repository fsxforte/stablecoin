import requests
from pandas.io.json import json_normalize
import pandas as pd
from collections import Counter 


def basket_universe(size):
	'''
	This function retrieves the basket of pairs to look at, based on the last 24 hours of data
	:param: size - define the basket size to return
	;forced_pair: - specify the twin pair, if necessary
	'''
	#Retrieve data on all markets supported by the CryptoCompare API
	response = requests.get('https://min-api.cryptocompare.com/data/top/mktcapfull?limit=20&tsym=USD')
	if response.status_code != 200:
		# This means something went wrong.
		print('Error ' + str(response.status_code) + ' returned from CryptoCompare.')

	#Convert the payload to a DataFrame
	df=json_normalize(response.json()['Data'])

	#Create list of coins with the largest marketcap
	largest_pairs = list(df['CoinInfo.Name'])

	#For the coins with the largest marketcap, find the largest traded pairs
	df_master=pd.DataFrame()
	for pair in largest_pairs:
		query_string = 'https://min-api.cryptocompare.com/data/top/pairs?fsym=' + str(pair)
		response = requests.get(query_string)
		if response.status_code != 200:
			# This means something went wrong.
			print('Error ' + str(response.status_code) + ' returned from CryptoCompare.')
		df = json_normalize(response.json()['Data'])
		df_master = df_master.append(df, ignore_index=True)

	#Overall, what is the msot common currency for each of these large market cap pairs to be paired with?
	tosymbols = list(df_master['toSymbol'])
	def most_frequent(list): 
		occurence_count = Counter(list) 
		return occurence_count.most_common(1)[0][0]

	most_frequent(tosymbols)

	#Return list of the pairs for the basket
	basket_pairs = []
	for pair in largest_pairs:
		if pair!=most_frequent(tosymbols):
			basket_pairs.append(str(pair) + str(most_frequent(tosymbols)))
			
	print('Largest ' + str(size) + ' coins by market cap, twinned with the most common other currency, ' + str(most_frequent(tosymbols))+  ', are ' + str(basket_pairs[:size]))

