######################################
##### Plots of Liquidity #############
######################################

import datetime as dt

from engine import data_cleaning

start_date = dt.datetime(2019,7,1)
end_date = dt.datetime(2019,12,1)

selected_symbols = data_cleaning.universe_selection_on_volume(5, start_date, end_date)

#Things to look at: open, high, low, close, volume, quote_asset_volume, number_of_trades
data_cleaning.data_explorer('close', selected_symbols, start_date, end_date)
