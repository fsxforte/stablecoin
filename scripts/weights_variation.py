#########################################
#### Variation in weights over time #####
#########################################

#Want to see how the weights have changed over time for a fixed basket of assets
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, date

from scripts import data_cleaning
from engine.generic_functions import resample

from engine.generic_functions import pairwise, generate_time_pairs
from engine.portfolio_functions import simulated_ef

#Weights: chosen to minimize variance of basket
#Constant parameters
start_date = dt.datetime(2019,7,1)
end_date = dt.datetime(2019,12,1)
num_assets = 5

#Find list of 10 largest symbols by period over period given by start_date and end_date
selected_symbols = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)
##For 5 assets chosen to have the most volume in September, list is:
#['CBM-4B2_BNB', 'MVL-7B0_BNB', 'RAVEN-F66_BNB', 'BKBT-3A6_BNB', 'NPXSXEM-89C_BNB']

#See how weights would change for everyday in September
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).months)):
        yield start_date + timedelta(n)

date_list = list(pairwise(daterange(start_date, end_date)))

#Make a dataframe containing all of the portfolio weights over September
weights_master = pd.DataFrame()
for day in date_list:
	close_prices = data_cleaning.df_make('close', selected_symbols, day[0], day[1])
	#Create returns matrix for hourly prices (resampling to hourly)
	close_prices = close_prices.resample('H').mean()
	#Calculate 
	returns = close_prices.pct_change()
	mean_returns = returns.mean()
	cov_matrix = returns.cov()
	num_portfolios = 1000
	risk_free_rate = 0.02
	min_vol_weights = simulated_ef(close_prices, num_assets, mean_returns, cov_matrix, num_portfolios, risk_free_rate)
	min_vol_weights = min_vol_weights.div(min_vol_weights.sum(axis=1), axis=0)
	min_vol_weights['date'] = day[0]
	weights_master = weights_master.append(min_vol_weights)

weights_master = weights_master.set_index('date')

fig, ax = plt.subplots()
weights_master.plot(ax=ax)
ax.set_ylabel('Weight in basket', fontsize = 16)
ax.tick_params(axis='both', which='major', labelsize=16)
plt.title('Volatility minimizing weights - daily', fontsize = 16)
plt.show()