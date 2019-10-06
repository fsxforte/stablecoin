import requests
from pandas.io.json import json_normalize
import pandas as pd

#Retrieve data on all markets supported by the CryptoCompare API
response = requests.get('https://min-api.cryptocompare.com/data/top/mktcapfull?limit=20&tsym=USD')
if response.status_code != 200:
	# This means something went wrong.
	print('Error ' + str(response.status_code) + ' returned from CryptoCompare.')
elif response.status_code == 200:
	print('Payload successfully retrieved.')

#Convert the payload to a DataFrame
df=json_normalize(response.json()['Data'])

