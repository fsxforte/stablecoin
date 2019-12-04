**BEP-2 Stablecoin**

The aim of this project is to examine BEP2 tokens on the Binance Blockchain.
In particular, the liquidity and volatility of these assets, and whether combinations of these assets may afford lower volatility. 

# **Section 1: project structure **

## **/data**

Folder that stores the data, in pickle file format.

## **/engine**

Folder that stores the main functions that are used for the analysis. In particular:

### binance_chain.py

This file contains functions that retrieve all the tokens from the Binance-Chain, get all the markets on the Binance Chain.
Most importantly the file contains the function **get_all_1m_klines()**, a file which extracts all of the data from the Binance Chain at 1-minute frequency. 

## generic_functions.py

This file contains generic functions that are used to support the analysis elsewhere. 

## portfolio_functions.py

This file contains a variety of functions that compute the performance of different baskets of BEP-2 cryptoassets.

## **/scripts**

### data_cleaning.py

This file contains functions for (i) loading in the pickled data file, (ii) selecting a basket of assets based on volume (as a proxy for liquidity), (iii) plotting of variables of interest within the imported data - and other functions too. 

### stability_of_basket.py

This purpose of the analysis in this file is to understand how much variability there is in the composition of the stablecoin basket.
For instance, if the 5 largest assets by volume are selected in one month, how many of these assets would be selected using data from the next month?
**There appears to be significant volatility in terms of the membership of assets to the basket, with many pairs joining and leaving the top 10. Therefore the analysis mainly focusses on the top 5 assets by volume to keep the basket composition stable **

In July, new larger volume symbols are ['PVT-554_BNB', 'BKBT-3A6_BNB', 'ERD-D06_BNB', 'MEETONE-031_BNB']

In Aug, new larger volume symbols are ['CBM-4B2_BNB', 'KAT-7BB_BNB']

In Sept new larger volume symbols are ['MVL-7B0_BNB', 'NPXSXEM-89C_BNB']

In Oct new larger volume symbols is ['KAT-7BB_BNB']

**The basket for September (used in the analysis) is [CBM-4B2_BNB. MVL-7B0_BNB, RAVEN-F66_BNB, BKBT-3A6_BNB, NPSXEM-89C_BNB]**

### weights_variation.py

This file demonstrates how much the weights would change if the weights are optimized to minimize variance every day (gives a sense of how volatile the assets are intra-day).
These weights are derives my minimizing the variance through simulation, as shown in the following figure. 

![Minimizing variance on MV portfolio simulations](figs/Figure_1.png)

Resulting in weights with the following variability over the course of 1-month.

![Optimum weights through time for 5 largest assets](figs/Figure_2.png)

### stablecoin.py

This is the main file, which shows how the volatility (returns) can be dampened / smoothed by selecting a basket of assets that minimize the variance. 

Three methods are compared: (i) equal weighting (a naive portfolio); (ii) using weights from random sampling and (iii) minimizing the weights using SciPy. 
See the following figure. 

![Improvement in volatility through variance minimization](figs/Figure_3.png)

