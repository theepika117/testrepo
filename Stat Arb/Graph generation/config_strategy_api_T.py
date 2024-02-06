"""
test net API end point : https://api-testnet.bybit.com
main net api endpoint : https://api.bybit.com
API Documentation : https://bybit-exchange.github.io/docs/linear/#t-introduction




"""
 #for providing http requests. pybit is a module provided by bybit


from pybit.unified_trading import HTTP


#from pybit.unified_trading import WebSocket


# CONFIG

timeframe = 120                                 #60 min interval
kline_limit = 1000                               #max limit of kline. You can only get a max of 200 kline at a time acc to API
z_score_window = 60                            #z score for past 60 days




# TEST API
api_key_testnet = "m1SGFz4iwLbmIi9VZX"
api_secret_testnet = "JkoEAojdvRMuUQNVa2Bhn2GhIVtOePRPseO6"


# SELECTED API
api_key = api_key_testnet
api_secret = api_secret_testnet


# SELECTED URL
api_url = "https://api-testnet.bybit.com"


# SESSION Activation
# test = True
# session = HTTP(testnet=test)

session = HTTP(
    testnet=True,
    api_key="api_key_testnet",
    api_secret="api_secret_testnet",
)

symbols = session.get_instruments_info(category="linear")
if symbols["retMsg"] == "OK":
    symbols = symbols["result"]["list"]

#print(symbols)

# # Web Socket Connection
# subs = [
#     "candle.1.BTCUSDT"
# ]
# ws = WebSocket(
#     "wss://stream-testnet.bybit.com/realtime_public",
#     subscriptions=subs
# )


# while True:
#     data = ws.fetch(subs[0])
#     if data:
#         print(data)

