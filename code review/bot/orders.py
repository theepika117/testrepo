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
    order_params = {
        "category": "linear",
        "symbol": ticker,
        "side": side,
        "qty": quantity,
        "isLeverage": 0,
        "reduceOnly": False,
        "closeOnTrigger": False,
        "stopLoss": stop_loss
    }
    # Adjusting parameters according to order type
    if limit_order:  # Placing limit order
        order_params.update({
            "orderType": "Limit",
            "price": price,
            "timeInForce": "PostOnly"
        })
    else:  # Placing market order
        order_params.update({
            "orderType": "Market",
            "timeInForce": "GTC"
        })
    response = session_private.place_order(**order_params)

    return response


def order(ticker, direction, capital):
    """Collects all the necessary data and places order accordingly"""
    orderbook = session.get_orderbook(category="linear", symbol=ticker)

    if orderbook:
        mid_price, stop_loss, quantity = calc_trade_details(orderbook, direction, capital)                                  
        if quantity > 0:                                                                                                        #checking if there exists some quantity that the trader can buy or sell in market
            response = call_order(ticker, mid_price, quantity, direction, stop_loss)
            if "result" in response.keys() and "orderId" in response["result"]:
                return response["result"]["orderId"]
    return 0