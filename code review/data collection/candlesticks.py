from settings import session, interval, limit
import datetime
import time

# Getting start times
start_date = 0
if isinstance(interval, int):
    start_date = datetime.datetime.now() - datetime.timedelta(hours=limit)                                  #if the interval is in hours, it subtracts limit no of hrs frm the current date

if interval == "D":
    start_date = datetime.datetime.now() - datetime.timedelta(days=limit)                                   #if the interval is in days, it subtracts limit  no of days from the current date

start_seconds = int(start_date.timestamp())                                                                 #time converted into seconds


def get_candles(symbol):
    # Getting price candles
    candles = session.get_mark_price_kline(                                                                 #fetches price details of candlesticks
        symbol=symbol, category="linear", interval=interval, limit=limit, start=start_seconds
    )

    # In order to manage API call limit issues
    time.sleep(0.1)
    candles = candles["result"]
    candles["list"] = [[float(price) for price in candle] for candle in candles["list"]]                    #it stores the API response data of string datatype in float datatype for future computation


    return candles if len(candles["list"]) == limit else {}                                                 #returns only those candles with price details









'''

    {
    "retCode": 0,
    "retMsg": "OK",
    "result": {
        "symbol": "BTCUSDT",
        "category": "linear",
        "list": [
            [
            "1670608800000",
            "17164.16",
            "17164.16",
            "17121.5",
            "17131.64"
            ]
        ]
    },
    "retExtInfo": {},
    "time": 1672026361839
}

candles = {
        "symbol": "BTCUSDT",
        "category": "linear",
        "list": [
            [
            "1670608800000",        #price in string
            "17164.16",             #price in string
            "17164.16",             #price in string
            "17121.5",              #price in string
            "17131.64"              #price in string
            ]
        ]
    }

candle = [
            "1670608800000",
            "17164.16",
            "17164.16",
            "17121.5",
            "17131.64"
            ]
'''
