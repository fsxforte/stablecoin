import requests
from pandas.io.json import json_normalize
import pandas as pd
import datetime as dt
from itertools import tee
from typing import Iterable, Tuple, TypeVar
import pickle

from engine.get_pairs_universe import basket_universe

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

#Resample data
def resample(df, frequency: str):
	"""
	Resample data to a lower time resolution. 
	:df: input data, MUST be for a single pair only
	:frequency: frequency to resample to, e.g. 'H' for hourly
	"""
	ohlcv_dict = {
	'open': 'first',
	'high': 'max',
	'low': 'min',
	'close': 'last',
	'volume': 'sum',
	'quote_asset_volume': 'sum',
	'number_of_trades': 'sum'
	}
	df = df.resample(frequency, how = ohlcv_dict)
	return df