from settings import session_private


def check_positions(ticker):
    """Checks for any open positions and returns true or false accordingly"""
    positions = session_private.get_positions(category="linear", symbol=ticker)
    if all(("retMsg" in positions.keys(), positions["retMsg"] == "OK",
            positions["result"]["list"] != [])):                                                                #checks for successful response. However the first two conditions are same. unneccessary extra condition check                                                   
        
        for item in positions["result"]["list"]:
            if float(item["size"]) > 0:                                                                         #considers only those coins in open positions
                price = float(item["avgPrice"]) if not len(item["avgPrice"]) == 0 else 0                        #converts the avgPrice to float value if it is present else it is made 0
                qty = float(item["size"])                                                                       #qty has amt of crypto currency in open positions
                return True, price, qty                                                                         #returns avg price and quantity for successful response
    
    return [False, 0, 0]                                                                                        #returns false is the response is unsuccessful or if the list is empty


def check_orders(ticker):
    """Checks for any active orders and returns true or false accordingly"""
    active_orders = session_private.get_open_orders(
        category="linear",
        symbol=ticker,
        openOnly=0,
        limit=50,
    )                                                                                                               #fetches open orders
    if all(("retMsg" in active_orders.keys(), active_orders["retMsg"] == "OK",
            active_orders["result"]["list"] != [])):
        for item in active_orders["result"]["list"]:
            if float(item["qty"]) > 0:
                price = float(item["avgPrice"]) if not len(item["avgPrice"]) == 0 else 0
                qty = float(item["qty"])                                                                            #fetches the quantity of coins in open trade
                status = item["orderStatus"]                                                                        #fetches current status of the coin
                return True, price, qty, status                                                                     #returns average price, quantity and status for successful response
    return [False, 0, 0, ""]