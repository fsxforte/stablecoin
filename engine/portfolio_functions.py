import numpy as np
import pandas as pd
import scipy.optimize as sco
import matplotlib.pyplot as plt

def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    '''
    Function to return portfolio annualized performance.
    :weights: portfolio weights, dimensionality is 1 x n, where n is number of assets in basket
    :mean_returns: mean returns over sample period
    :cov_matrix: covariance matrix of returns
    '''
    returns = np.sum(mean_returns * weights ) * 365.25
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(365.25)
   
    return std, returns
  
def random_portfolios(num_assets: int, num_portfolios: int, mean_returns: float, cov_matrix, risk_free_rate: float):
    '''
    Function to generate random portfilios.
    :num_assets: number of assets in basket. 
    :num_portfolios: number of portfolios to generate
    :mean_returns: variable for mean returns
    :cov_matrix: covariance matrix of returns
    :risk_free_rate: risk free rate on open market
    '''
    results = np.zeros((3,num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
   
    return results, weights_record

def simulated_ef(df, num_assets: int, mean_returns: float, cov_matrix, num_portfolios: int, risk_free_rate: float):
    '''
    Function to randomly generate portfolios by randomly generating weights. 
    :df: dataframe with column names
    :num_assets: number of assets in basket
    :mean_returns: variable for mean returns
    :cov_matrix: covariance matrix of returns
    :num_portfolios: number of portfolios to generate
    :risk_free_rate: rf rate to act as a comparator
    '''
    results, weights = random_portfolios(num_assets, num_portfolios, mean_returns, cov_matrix, risk_free_rate)
    
    #Find portfolio that maximizes sharpe ratio
    max_sharpe_idx = np.argmax(results[2])
    
    #Extract standard deviation and return of portfolio that maximizes sharpe
    portfolio_std_dev_max, rp = results[0,max_sharpe_idx], results[1,max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx],index=df.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    
    #Find minimum volatility
    min_vol_idx = np.argmin(results[0])
    portfolio_std_dev_min, rp_min = results[0,min_vol_idx], results[1,min_vol_idx]
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx],index=df.columns,columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    # print('Maximum Sharpe Ratio Portfolio Allocation\n')
    # print('Annualised Return:', round(rp,2)) 
    # print('Annualised Volatility:', round(portfolio_std_dev_max,2))
    # print('\n') 
    # print(max_sharpe_allocation)
    # print('Minimum Volatility Portfolio Allocation\n')
    # print('Annualised Return:', round(rp_min,2))
    # print('Annualised Volatility:', round(portfolio_std_dev_min,2))
    # print('\n')
    # print(min_vol_allocation)
    
    # plt.figure(figsize=(10, 7))
    # plt.scatter(results[0,:],results[1,:],c=results[2,:],cmap='BuGn', marker='o', s=10, alpha=0.3)
    # plt.colorbar()
    # plt.scatter(portfolio_std_dev_max,rp,marker='1',color='r',s=500, label='Maximum Sharpe ratio')
    # plt.scatter(portfolio_std_dev_min,rp_min,marker='1',color='g',s=500, label='Minimum volatility')
    # plt.title('Simulated Portfolio Optimization - Mean/Variance trade-off')
    # plt.xlabel('Annualised volatility')
    # plt.ylabel('Annualised returns')
    # plt.legend(labelspacing=0.8)
    # plt.show()

    return min_vol_allocation

def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

def find_min_variance_basket(mean_returns, cov_matrix):
    '''
    Compute minimum variance portfolio directly using SciPy Optimize.
    :mean_returns: mean returns for each asset over the period
    :cov_matrix: covariance matrix of returns
    '''
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    
    #Setup the dictionary of constraints
    #type ='eq' means that the constraint is an equality
    #fun defines the function defining the constraint
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    #Specify the bounds on the weights such that any weight must be between 0 and 1 (inclusive).
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))

    #SLSQP corresponds to Sequential Least SQuares Programming
    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints, options={'maxiter': '1000'})

    return result

