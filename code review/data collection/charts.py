import pandas as pd
import matplotlib.pyplot as plt

from settings import window
from cointegration import close_prices, calc_spread, calc_zscore, cointegrate


def plot_charts(symbol_1, symbol_2, price_data):

    # Extracting prices to plot the trends
    prices_1 = close_prices(price_data[symbol_1])
    prices_2 = close_prices(price_data[symbol_2])

    # Getting spread and z-score
    coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossing = cointegrate(prices_1, prices_2)
    spread = calc_spread(prices_1, prices_2, hedge_ratio)
    zscore = calc_zscore(spread, window_size=window)

    # Calculating percentage changes
    df = pd.DataFrame(columns=[symbol_1, symbol_2])
    df[symbol_1] = prices_1
    df[symbol_2] = prices_2
    df[f"{symbol_1}_pct"] = df[symbol_1] / prices_1[0]
    df[f"{symbol_2}_pct"] = df[symbol_2] / prices_2[0]
    series_1 = df[f"{symbol_1}_pct"].astype(float).values
    series_2 = df[f"{symbol_2}_pct"].astype(float).values

    # Saving results for Backtesting
    df_2 = pd.DataFrame()
    df_2[symbol_1] = prices_1
    df_2[symbol_2] = prices_2
    df_2["Spread"] = spread
    df_2["Z-Score"] = zscore

    df_2.to_csv("Backtest.csv")
    print("Backtesting data has been saved.")

    # Plotting charts
    fig, axs = plt.subplots(3, figsize=(16, 8))
    fig.suptitle(f"Price Movement")
    axs[1].set_title("Spread")
    axs[2].set_title("Z-Score")

    # Plotting price movements
    axs[0].plot(series_1, label=symbol_1)
    axs[0].plot(series_2, label=symbol_2)
    axs[0].legend()

    # Plotting spread
    axs[1].plot(spread, label='Spread')
    axs[1].legend()

    # Plotting z-scores
    axs[2].plot(zscore, label='Z-Score')
    axs[2].legend()

    plt.get_current_fig_manager().set_window_title(f"Price, Spread and Z-Score - {symbol_1} & {symbol_2}")
    plt.tight_layout()  # To adjust subplot layout
    plt.show()