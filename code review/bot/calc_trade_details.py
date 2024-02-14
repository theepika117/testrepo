from settings import instrument_1, stop_loss, rounding_1, rounding_2, qty1_rounding, qty2_rounding


def close_prices(prices):
    closing_prices = [(float(candle[4])) for candle in prices["list"]
                      if not str(candle[4]).lower() == 'nan']                                           #only valid prices are returned
    return closing_prices


def calc_trade_details(orderbook, direction="Long", capital=0):
    """Returns prices, stop loss / fail-safe and quantity"""
    mid_price, quantity, fail_safe = 0, 0, 0

    if orderbook:
        # Rounding the prices and quantities
        price_round = rounding_1 if orderbook["result"]["s"] == instrument_1 else rounding_2                            #rounding value(no of decimal points in min price according to the symbol
        quantity_round = qty1_rounding if orderbook["result"]["s"] == instrument_1 else qty2_rounding                   #rounding value(no of decimal points in min orderqty according to the symbol

        # Organising prices
        bid_prices = [float(level[0]) for level in orderbook["result"]["b"]]                                            #stores bit order price
        ask_prices = [float(level[0]) for level in orderbook["result"]["a"]]                                            #stores ask order price

        # Calculating price, size, stop loss and average liquidity
        if bid_prices and ask_prices:
            bid_prices.sort(reverse=True)                                                                                #sorts the bit price in descending order
            ask_prices.sort()                                                                                            #sorts the ask price in ascending order these sortings helps in finding nearest bit and ask                                                                                      
            nearest_ask = ask_prices[0]  # Getting the nearest ask
            nearest_bid = bid_prices[0]  # Getting the nearest bid

            if direction == "Long":
                mid_price = nearest_bid                                                                                  #price at which trading happens
                fail_safe = round(mid_price * (1 - stop_loss), price_round)                                              #fail safe placed below mid price
            else:
                mid_price = nearest_ask
                fail_safe = round(mid_price * (1 + stop_loss), price_round)                                               #fail safe placed above mid price

            quantity = round(capital / mid_price, quantity_round)                                                         #number of units or quantity of the asset that the trader can buy or sell in the market.

    return mid_price, fail_safe, quantity