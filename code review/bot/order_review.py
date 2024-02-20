from settings import session
from calc_trade_details import calc_trade_details
from orders_positions_check import check_positions, check_orders


def review_order(ticker, remaining_capital):
    """Takes a ticker, checks for any open orders """
    # Getting latest orderbook data
    orderbook = session.get_orderbook(category="linear", symbol=ticker)                                     #fetches orderbook

    # To get the last traded price
    mid_price, _, _ = calc_trade_details(orderbook)                                                         #storing mindprice

    # Getting details of the trade
    _, order_price, order_qty, order_status = check_orders(ticker)                                          #fetches order price, quantity and status for the selected instrument

    # Getting open positions
    _, position_price, position_quantity = check_positions(ticker)                                          #fetches avg price and quantity
    if position_price >= remaining_capital and position_quantity > 0:
        print(f"position_quantity {position_quantity}; remaining_capital {remaining_capital}")
        return "Trade Complete"                                                                             
                                                                                                            #this function returns the order status, which could be either complete or new or created or partially filled or filled or cancelled or rejected
    return order_status                                                                                     