import pybit.exceptions
from settings import session, session_private, limit_order
from calc_trade_details import calc_trade_details


def leverage(ticker):
    """Sets leverage to 1"""
    try:
        session_private.set_leverage(                                                           #sets the leverage to 1x for the parsed instrument
            category="linear",
            symbol=ticker,
            buyLeverage="1",
            sellLeverage="1",
        )
    except pybit.exceptions.InvalidRequestError:                                                 #to avoid code termination
        pass


def call_order(ticker, price, quantity, direction, stop_loss):
    """Places Limit or Market order"""

    side = "Buy" if direction == "Long" else "Sell"

    # Common order parameters
    order_params = {                                                                            #dict to store order parameters
        "category": "linear",
        "symbol": ticker,               
        "side": side,                   
        "qty": quantity,                
        "isLeverage": 0,
        "reduceOnly": False,                                                                    #provides flexibility over either increasing or decreasing or establishing new positions
        "closeOnTrigger": False,                                                                #this is for the manual control over exiting the trade
        "stopLoss": stop_loss
    }
    # Adjusting parameters according to order type
    if limit_order:  # Placing limit order
        order_params.update({
            "orderType": "Limit",
            "price": price,
            "timeInForce": "PostOnly"                                                           #"PostOnly" ensures that the limit order is only added to the order book and not immedietely matched
        })
    else:  # Placing market order
        order_params.update({
            "orderType": "Market",
            "timeInForce": "GTC"                                                                #provides flexibility over order filling at different market prices   
        })
    response = session_private.place_order(**order_params)                                      #fetches orderID

    return response


def order(ticker, direction, capital):
    """Collects all the necessary data and places order accordingly"""
    orderbook = session.get_orderbook(category="linear", symbol=ticker)                                                         #fetches orderbook for the instrument

    if orderbook:
        mid_price, stop_loss, quantity = calc_trade_details(orderbook, direction, capital)                                  
        if quantity > 0:                                                                                                        #checking if there exists some quantity that the trader can buy or sell in market
            response = call_order(ticker, mid_price, quantity, direction, stop_loss)
            if "result" in response.keys() and "orderId" in response["result"]:
                return response["result"]["orderId"]                                                                            #returns the orderID only when the order is successfully placed
    return 0 