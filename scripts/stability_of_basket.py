
####################################
## Stability of basket of assets ###
####################################

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from scripts import data_cleaning
from engine.generic_functions import resample

##### 10 assets
num_assets = 10

#April
start_date = dt.datetime(2019,4,1)
end_date = dt.datetime(2019,5,1)
selected_symbols_april = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#May
start_date = dt.datetime(2019,5,1)
end_date = dt.datetime(2019,6,1)
selected_symbols_may = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#June
start_date = dt.datetime(2019,6,1)
end_date = dt.datetime(2019,7,1)
selected_symbols_jun = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#July
start_date = dt.datetime(2019,7,1)
end_date = dt.datetime(2019,8,1)
selected_symbols_jul = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#August
start_date = dt.datetime(2019,8,1)
end_date = dt.datetime(2019,9,1)
selected_symbols_aug = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#September
start_date = dt.datetime(2019,9,1)
end_date = dt.datetime(2019,10,1)
selected_symbols_sep = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#October
start_date = dt.datetime(2019,10,1)
end_date = dt.datetime(2019,11,1)
selected_symbols_oct = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#November
start_date = dt.datetime(2019,11,1)
end_date = dt.datetime(2019,12,1)
selected_symbols_nov = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#Compare lists
def symbols_diff(li1, li2): 
    li_dif = [i for i in li2 if i not in li1] 
    return li_dif 

#Jan-Mar have 0 symbols
#April has 2, May has 7, June and onwards have at least 10

diff = symbols_diff(selected_symbols_jun, selected_symbols_jul)
#In Jul new larger volume symbols are ['PVT-554_BNB', 'BKBT-3A6_BNB', 'ERD-D06_BNB', 'MEETONE-031_BNB', 'KAT-7BB_BNB', 'TOP-491_BNB', 'CHZ-ECD_BNB']

diff = symbols_diff(selected_symbols_jul, selected_symbols_aug)
#In Aug new larger volume symbols are ['CBM-4B2_BNB', 'MVL-7B0_BNB', 'QBX-38C_BNB', 'NEW-09E_BNB']

diff = symbols_diff(selected_symbols_aug, selected_symbols_sep)
#In Sept new larger volume symbols are ['NPXSXEM-89C_BNB', 'EQL-586_BNB', 'MTV-4C6_BNB']

diff = symbols_diff(selected_symbols_sep, selected_symbols_oct)
#In Oct new larger volume symbols are ['CNNS-E16_BNB', 'AXPR-777_BNB']

diff = symbols_diff(selected_symbols_oct, selected_symbols_nov)
#In Nov new larger volume symbols are ['PYN-C37_BNB', 'EVT-49B_BNB']


###### 5 assets
num_assets = 5

#April
start_date = dt.datetime(2019,4,1)
end_date = dt.datetime(2019,5,1)
selected_symbols_april = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#May
start_date = dt.datetime(2019,5,1)
end_date = dt.datetime(2019,6,1)
selected_symbols_may = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#June
start_date = dt.datetime(2019,6,1)
end_date = dt.datetime(2019,7,1)
selected_symbols_jun = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#July
start_date = dt.datetime(2019,7,1)
end_date = dt.datetime(2019,8,1)
selected_symbols_jul = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#August
start_date = dt.datetime(2019,8,1)
end_date = dt.datetime(2019,9,1)
selected_symbols_aug = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#September
start_date = dt.datetime(2019,9,1)
end_date = dt.datetime(2019,10,1)
selected_symbols_sep = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#October
start_date = dt.datetime(2019,10,1)
end_date = dt.datetime(2019,11,1)
selected_symbols_oct = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)

#November
start_date = dt.datetime(2019,11,1)
end_date = dt.datetime(2019,12,1)
selected_symbols_nov = data_cleaning.universe_selection_on_volume(num_assets, start_date, end_date)


#Jan-Mar have 0 symbols
#April has 2, May has 7, June and onwards have at least 10

diff = symbols_diff(selected_symbols_jun, selected_symbols_jul)
#In Jul new larger volume symbols are ['PVT-554_BNB', 'BKBT-3A6_BNB', 'ERD-D06_BNB', 'MEETONE-031_BNB']

diff = symbols_diff(selected_symbols_jul, selected_symbols_aug)
#In Aug new larger volume symbols are ['CBM-4B2_BNB', 'KAT-7BB_BNB']

diff = symbols_diff(selected_symbols_aug, selected_symbols_sep)
#In Sept new larger volume symbols are ['MVL-7B0_BNB', 'NPXSXEM-89C_BNB']

diff = symbols_diff(selected_symbols_sep, selected_symbols_oct)
#In Oct new larger volume symbols is ['KAT-7BB_BNB']

diff = symbols_diff(selected_symbols_oct, selected_symbols_nov)
#In Oct new larger volume symbols is ['MTV-4C6_BNB']