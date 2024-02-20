from settings import session_private


def check_positions(ticker):
    """Checks for any open positions and returns true or false accordingly"""
    positions = session_private.get_positions(category="linear", symbol=ticker)                     #fetches trading position data
    if all(("retMsg" in positions.keys(), positions["retMsg"] == "OK",
            positions["result"]["list"] != [])):                                                    #checking for successful response        
        for item in positions["result"]["list"]:
            if float(item["size"]) > 0:
                price = float(item["avgPrice"]) if not len(item["avgPrice"]) == 0 else 0
                qty = float(item["size"])
                return True, price, qty                                                             #returns avg price and quantity for successful response
    return [False, 0, 0]


def check_orders(ticker):
    """Checks for any active orders and returns true or false accordingly"""
    active_orders = session_private.get_open_orders(
        category="linear",
        symbol=ticker,
        openOnly=0,
        limit=50,
    )                                                                                               #fetches open orders
    if all(("retMsg" in active_orders.keys(), active_orders["retMsg"] == "OK",
            active_orders["result"]["list"] != [])):                                                #checking for successful response
        for item in active_orders["result"]["list"]:
            if float(item["qty"]) > 0:
                price = float(item["avgPrice"]) if not len(item["avgPrice"]) == 0 else 0
                qty = float(item["qty"])
                status = item["orderStatus"]
                return True, price, qty, status                                                     #returns average price, quantity and status for successful response
    return [False, 0, 0, ""]