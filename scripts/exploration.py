import datetime as dt

from scripts import data_cleaning

start_date = dt.datetime(2019,9,1)
end_date = dt.datetime(2019,9,30)

selected_symbols = data_cleaning.universe_selection_on_volume(10, start_date, end_date)

#Things to look at: open, high, low, close, volume, quote_asset_volume, number_of_trades
data_cleaning.data_explorer('number_of_trades', selected_symbols, start_date, end_date)
