import math

import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import coint
import statsmodels.api as sm


# Calculating Z-Score
def calc_zscore(series, window_size):
    mean = series.rolling(window=window_size).mean()
    std = series.rolling(window=window_size).std()
    zscore = (series - mean) / std
    return zscore


# Calculating Spread
def calc_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - (pd.Series(series_2) * hedge_ratio)
    return spread


# Calculating Co-integration
def cointegrate(series_1, series_2):
    coint_test = 0
    t_value, p_value, critical_value = coint(series_1, series_2)
    model = sm.OLS(series_1, series_2).fit()  # To calculate the hedge ratio
    hedge_ratio = model.params[0]
    spread = calc_spread(series_1, series_2, hedge_ratio)
    zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])                                             #calculating number of zero crossings by counting where the sign changes
    if p_value < 0.5 and t_value < critical_value[1]:
        coint_test = 1                                                                                      #flag is made true when the condition is met
    return (coint_test, round(p_value, 2), round(t_value, 2),
            round(critical_value[1], 2), round(hedge_ratio, 2), zero_crossings)


# Extracting closing prices from the data
def close_prices(prices):
    closing_prices = [candle[4] for candle in prices["list"] if not math.isnan(candle[4])]
    return closing_prices


# Finding Cointegrated Pairs
def cointegrated_pairs(prices):
    pairs = []
    included_pairs = []

    for symbol_1 in list(prices.keys()):                                                            #loops to iterate over the price dict
        for symbol_2 in list(prices.keys()):
            if symbol_2 != symbol_1:
                sorted_characters = sorted(symbol_1 + symbol_2)
                unique = "".join(sorted_characters)                                                 #2 diff symb are concatinated and sorted 
                if unique in included_pairs:                                                        #if similar pair is aldready found then this iteration will be broken
                    break

                #closing prices are calculated
                series_1 = close_prices(prices[symbol_1])
                series_2 = close_prices(prices[symbol_2])

                #checking for cointegrated pairs
                coint_test, p_value, t_value, c_value, hedge_ratio, zero_crossings = cointegrate(series_1, series_2)
                
                if coint_test:                                                      
                    included_pairs.append(unique)                                                           #appending the unique name of symbols created to included_pairs list only when the symbols are cointegrated
                    pairs.append({
                        "Instrument-1": symbol_1,
                        "Instrument-2": symbol_2,
                        "p-value": p_value,
                        "t-value": t_value,
                        "critical value": c_value,
                        "hedge_ratio": hedge_ratio,
                        "Zero_crossings": zero_crossings
                    })
    if not pairs:
        print("No cointegrated pairs found; Try adjusting the candle limit and interval")
        return None
    coint_df = pd.DataFrame(pairs).sort_values(by="Zero_crossings", ascending=False)                        #pairs are sorted in descending order 
    coint_df.to_csv("co-integrated_pairs.csv", index=False)
    print("Calculations completed; Report has been saved in co-integrated_pairs.csv")
    return coint_df