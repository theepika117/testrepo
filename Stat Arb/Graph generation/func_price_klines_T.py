from config_strategy_api_T import session
from config_strategy_api_T import timeframe
from config_strategy_api_T import kline_limit
from pybit.unified_trading import HTTP
import datetime
import time
import json

# Get start times
time_start_date = 0
if timeframe == 120:
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == "D":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)

time_start_seconds = int(time_start_date.timestamp())


# Get historical prices (klines)
def get_price_klines(symbol):

    # Get prices
    # prices = session.query_mark_price_kline(
    #     symbol = symbol,
    #     interval = timeframe,
    #     limit = kline_limit,
    #     from_time = time_start_seconds
    # )
    session = HTTP(testnet=True)
    prices = session.get_mark_price_kline(
        category="linear",
        symbol="BTCUSDT",
        interval=15,
        start=1670601600000,
        end=1670608800000,
        limit=1,
        )

    # Manage API calls
    time.sleep(0.1)

    # Return output
    if len(prices["result"]) != kline_limit:
        return []
    return prices["result"]



# Store price histry for all available pairs
def store_price_history(symbols):

    # Get prices and store in DataFrame
    counts = 0
    price_history_dict = {}
    for sym in symbols:
        symbol_name = sym
        price_history = get_price_klines(symbol_name)
        if len(price_history) > 0:
            price_history_dict[symbol_name] = price_history
            counts += 1
            print(f"{counts} items stored")
        else:
            print(f"{counts} items not stored")

    # Output prices to JSON
    if len(price_history_dict) > 0:
        with open("1_price_list.json", "w") as fp:
            json.dump(price_history_dict, fp, indent=4)
        print("Prices saved successfully.")

    # Return output
    return

# #main code
# symbol_1 = "CROUSDT"
# store_price_history(symbol_1)
