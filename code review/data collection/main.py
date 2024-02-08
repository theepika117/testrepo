from pick_instruments import instruments
from store_data import store_data
from cointegration import cointegrated_pairs
from charts import plot_charts

import pandas as pd
import json

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == "__main__":

    # Getting all available symbols
    print("Fetching available instruments...")
    response = instruments()

    # Saving price history data
    print(f"Successfully fetched {len(response)} total symbols")
    print("Constructing and saving price data in JSON...")
    if len(response) > 0:
        store_data(response.values())

    # Getting Co-integrated pairs
    print("Calculating co-integration...")
    with open("data.json") as file:
        price_data = json.load(file)
        if len(price_data) > 0:
            pairs = cointegrated_pairs(price_data)

    # Plotting charts and saving for backtesting
        if len(price_data) > 0 and pairs is not None:
            pairs_data = pd.read_csv("co-integrated_pairs.csv")
            index = 0  # Index of the pair to be plotted
            instrument_1 = pairs_data.iloc[index]['Instrument-1']
            instrument_2 = pairs_data.iloc[index]['Instrument-2']
            print("Plotting charts...")
            plot_charts(instrument_1, instrument_2, price_data)