######################################################
#### Stablecoin with minimum volatility weightings ###
######################################################

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from engine import data_cleaning
from engine.generic_functions import resample

from engine.portfolio_functions import simulated_ef
from engine import portfolio_functions

#Constant parameters
start_date = dt.datetime(2019,7,1)
end_date = dt.datetime(2019,12,1)
num_assets = 5
num_portfolios = 1000
risk_free_rate = 0.02

#Find list of 10 largest symbols by period over period given by start_date and end_date
selected_symbols = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#Create dataframe of close prices
close_prices = data_cleaning.df_make('close', selected_symbols, start_date, end_date)

#Create returns matrix
close_prices = close_prices.resample('D').mean()
returns = close_prices.pct_change()
mean_returns = returns.mean()
cov_matrix = returns.cov()


#Get weights that minimize variance
simulated_ef(close_prices, num_assets, mean_returns, cov_matrix, num_portfolios, risk_free_rate)
min_vol_allocation = simulated_ef(close_prices, num_assets, mean_returns, cov_matrix, num_portfolios, risk_free_rate)
min_vol_allocation = min_vol_allocation.div(min_vol_allocation.sum(axis=1), axis=0)

#Confirm with scipy computation
result = portfolio_functions.find_min_variance_basket(mean_returns, cov_matrix)
#Extract array of weights
analytical_weights = list(result['x'])
analytical_weights_df = pd.DataFrame([analytical_weights], columns=selected_symbols)

#Compute stablecoin and plot for weights defined through simulation
stablecoin_random_weights = pd.DataFrame()
for symbol in selected_symbols:
	weight = min_vol_allocation[[symbol]].values[0][0]
	print(weight)
	weighted_col = returns[[symbol]]*weight
	print(weighted_col)
	stablecoin_random_weights = pd.concat([stablecoin_random_weights, weighted_col], axis=1, sort=False)

stablecoin_random_weights_volatility = stablecoin_random_weights.sum(axis=1)

#Plot for equal weights
equal_weighted_returns_volatility = returns.mean(axis=1)

#Plot for analytical weights 
stablecoin_analytical_weights = pd.DataFrame()
for symbol in selected_symbols:
	weight = analytical_weights_df[[symbol]].values[0][0]
	print(weight)
	weighted_col = returns[[symbol]]*weight
	print(weighted_col)
	stablecoin_analytical_weights = pd.concat([stablecoin_analytical_weights, weighted_col], axis=1, sort=False)

stablecoin_analytical_weights_volatility = stablecoin_analytical_weights.sum(axis=1)

fig, ax = plt.subplots()
master_df = pd.concat([equal_weighted_returns_volatility, stablecoin_random_weights_volatility, stablecoin_analytical_weights_volatility], axis = 1, sort = False)
master_df = master_df.rename(columns={0: 'equal_weights', 1:'random_weights', 2: 'analytical_weights'})
master_df.plot(ax=ax)
ax.set_ylabel('Volatility', fontsize = 16)
ax.tick_params(axis='both', which='major', labelsize=16)
plt.title('Comparing different weights on a currency basket ', fontsize = 16)
ax.legend()
plt.show()