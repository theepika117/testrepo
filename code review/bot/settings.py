from pybit.unified_trading import HTTP
import pandas as pd
import os

test = 1
testnet = [os.environ.get("bybit_key"), os.environ.get("bybit_private")]
mainnet = [os.environ.get("key_bybit"), os.environ.get("private_bybit")]

key, private = testnet if test else mainnet

limit = 1000  # Number of candles
interval = 120  # Length of a candle's data in minutes
window = 60  # To calculate Z-Score

session = HTTP(testnet=test)
session_private = HTTP(testnet=test, api_key=key, api_secret=private)

pairs_data = pd.read_csv("../data_collection/co-integrated_pairs.csv")                                                  #fetching data from the file containing cointegrates pairs detail
index = 0  # index of the pair to be traded                                                                             #first pair has highest num of zero crossings

instrument_1 = pairs_data.iloc[index]['Instrument-1']                                                                   #.iloc selects particular [row,column] from the dataFrame
instrument_2 = pairs_data.iloc[index]['Instrument-2']

# Getting the price and quantity roundings for the instruments
responses = (session.get_instruments_info(category="linear", symbol=instrument_1),
             session.get_instruments_info(category="linear", symbol=instrument_2))                                      #tuple of informations regarding instrument 1 and 2

if all("retMsg" in response.keys() and response["retMsg"] == "OK" for response in responses):
    minPrices = [response["result"]["list"][0]["priceFilter"]["minPrice"] for response in responses]                    #fetching minimum price of the instrument
    minOrderQty = [response["result"]["list"][0]["lotSizeFilter"]["minOrderQty"] for response in responses]             #fetching minimum order quantity of the instrument
    rounding_values = [[len(price.split(".")[1]) if "." in price else 0 for price in minPrices],
                       [len(qty.split(".")[1]) if "." in qty else 0 for qty in minOrderQty]]                            #stores the num of digits after decimal point if "." is present else zero is stored

    rounding_1, rounding_2 = rounding_values[0]                                                                         #num of decimal points in price
    qty1_rounding, qty2_rounding = rounding_values[1]                                                                   #num of decimal points in orderqty

limit_order = True
capital = 1000  # total capital allocated to be split between both pairs in USD
stop_loss = 0.20                                                                                                        #predetermined exit point to avoid loss
trigger = 1.1  # z-score value at which order is placed








'''
{
    "retCode": 0,
    "retMsg": "OK",
    "result": {
        "category": "linear",
        "list": [
            {
                "symbol": "BTCUSDT",
                "contractType": "LinearPerpetual",
                "status": "Trading",
                "baseCoin": "BTC",
                "quoteCoin": "USDT",
                "launchTime": "1585526400000",
                "deliveryTime": "0",
                "deliveryFeeRate": "",
                "priceScale": "2",
                "leverageFilter": {
                    "minLeverage": "1",
                    "maxLeverage": "100.00",
                    "leverageStep": "0.01"
                },
                "priceFilter": {
                    "minPrice": "0.10",
                    "maxPrice": "199999.80",
                    "tickSize": "0.10"
                },
                "lotSizeFilter": {
                    "maxOrderQty": "100.000",
                    "minOrderQty": "0.001",
                    "qtyStep": "0.001",
                    "postOnlyMaxOrderQty": "1000.000"
                },
                "unifiedMarginTrade": true,
                "fundingInterval": 480,
                "settleCoin": "USDT",
                "copyTrading": "both",
                "upperFundingRate": "0.00375",
                "lowerFundingRate": "-0.00375"
            }
        ],
        "nextPageCursor": ""
    },
    "retExtInfo": {},
    "time": 1707186451514
}
'''

