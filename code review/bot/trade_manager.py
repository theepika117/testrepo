from settings import session_private, instrument_1, instrument_2, trigger, capital, limit_order
from order_review import review_order
from price_calls import liquidity
from calc_stats import z_score
from orders import order

import time


def trade(switch):
    """Executes the trading strategy by analysing z-score, placing and managing trades dynamically."""
    signal_side = ""
    hot = False

    # Calculating the latest z-score data
    zscore, positive_signal = z_score()

    if abs(zscore) > trigger:

        # Activating hot trigger
        hot = True
        print("--Status: HOT--")
        print("--Placing and Monitoring Existing Trades--")

    # Placing and managing trades
    if hot and switch == 0:

        # Getting trading history to calculate liquidity
        liquidity_1, ltp_1 = liquidity(instrument_1)                                                        #returns avg liquidity and latest trading size of instrument 1
        liquidity_2, ltp_2 = liquidity(instrument_2)                                                        #returns avg liquidity and latest trading size of instrument 2

        # Deciding long and short tickers
        if positive_signal:
            long_ticker = instrument_1
            short_ticker = instrument_2
            liquidity_long = liquidity_1
            liquidity_short = liquidity_2
            ltp_long = ltp_1
            ltp_short = ltp_2
        else:
            long_ticker = instrument_2
            short_ticker = instrument_1
            liquidity_long = liquidity_2
            liquidity_short = liquidity_1
            ltp_long = ltp_2
            ltp_short = ltp_long

        # Filling targets
        capital_long = capital * 0.5                                                                      #50% of the capital is assigned to capital_long and remaining to capital_short
        capital_short = capital - capital_long
        target_long = liquidity_long * ltp_long                                                           #capital that could be invested in the long position on the basis of its liquidity and market price
        target_short = liquidity_short * ltp_short                                                        #capital that could be invested in the short position on the basis of its liquidity and market price
        initial_capital = min(target_long, target_short)

        # Making sure that initial capital does not exceed limits set in settings
        if limit_order:
            if initial_capital > capital_long:
                initial_capital = capital_long
        else:
            initial_capital = capital_long

        # Setting remaining capital
        balance_long = capital_long
        balance_short = capital_short

        # Trading until filled or signal is false
        status_long = ""
        status_short = ""
        counts_long = 0
        counts_short = 0

        while switch == 0:

            # Placing long order
            if counts_long == 0:
                order_long_id = order(long_ticker, "Long", initial_capital)
                counts_long = 1 if order_long_id else 0
                balance_long = balance_long - initial_capital

            # Placing shorting order
            if counts_short == 0:
                order_short_id = order(short_ticker, "Short", initial_capital)
                counts_short = 1 if order_short_id else 0
                balance_short = balance_short - initial_capital

            # Updating signal side
            if zscore > 0:
                signal_side = "Positive"
            else:
                signal_side = "Negative"

            # Handling switch for Market orders
            if not limit_order and counts_long and counts_short:
                switch = 1

            # Allowing some time for the API
            time.sleep(3)

            # Checking limit orders and making sure z_score is still within the range
            zscore_new, positive_signal_new = z_score()
            if switch == 0:
                if abs(zscore_new) > trigger * 0.9 and positive_signal_new == positive_signal:

                    # Checking long order status
                    if counts_long == 1:
                        status_long = review_order(long_ticker, balance_long)

                    # Checking short order status
                    if counts_short == 1:
                        status_short = review_order(short_ticker, balance_short)

                    print(f"{status_long}; {status_short}; z-score: {zscore_new}")

                    # If orders are still active, do nothing
                    if status_long in ["Created", "New"] or status_short in ["Created", "New"]:
                        continue

                    # If orders are partial fill, do nothing
                    if status_long == "PartiallyFilled" or status_short == "PartiallyFilled":
                        continue

                    # If orders trade complete, do nothing - stop opening trades
                    if status_long == "Trade Complete" and status_short == "Trade Complete":
                        switch = 1

                    # If position filled - place another trade
                    if status_long == "Filled" and status_short == "Filled":
                        counts_long = 0
                        counts_short = 0

                    # If order cancelled for long - try again
                    if status_long in ["Cancelled", "Rejected"]:
                        counts_long = 0

                    # If order cancelled for short - try again
                    if status_short in ["Cancelled", "Rejected"]:
                        counts_short = 0

                else:
                    # Canceling all active orders
                    session_private.cancel_all_active_orders(symbol=instrument_2)
                    session_private.cancel_all_active_orders(symbol=instrument_1)
                    switch = 1

    return switch, signal_side