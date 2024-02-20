from settings import instrument_1, instrument_2, session_private


def position_info(ticker):
    """Returns information on positions, if present, of the specified ticker"""
    side = 0
    size = ""
    position = session_private.get_positions(category="linear", symbol=ticker)                      #fetches data through API
    if "retMsg" in position.keys() and position["retMsg"] == "OK":
        if int(position["result"]["list"][0]["size"]) > 0:
            size = int(position["result"]["list"][0]["size"])
            side = position["result"]["list"][0]["side"]
        else:
            size = int(position["result"]["list"][0]["size"])
            side = "Sell"

    return side, size                                                                               #returns side and quantity


def close_position(ticker, side, size):
    """Closes a position immediately by placing a market order"""

    session_private.place_order(
        category="linear",
        symbol=ticker,
        side=side,
        orderType="Market",
        qty=size,
        reduceOnly=True,                                            #indicates close position
    )
    return


def exit_all_positions(switch):
    """Closes all the existing positions and cancels any pending orders"""
    session_private.cancel_all_orders(category="linear", symbol=instrument_1, settleCoin="USDT")
    session_private.cancel_all_orders(category="linear", symbol=instrument_2, settleCoin="USDT")

    side_1, size_1 = position_info(instrument_1)
    side_2, size_2 = position_info(instrument_2)

    if size_1 > 0:
        close_position(instrument_1, side_2, size_1)

    if size_2 > 0:
        close_position(instrument_2, side_1, size_2)

    switch = 0
    return switch
