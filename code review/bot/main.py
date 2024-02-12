from orders_positions_check import check_positions, check_orders
from settings import instrument_1, instrument_2
from manage_positions import exit_all_positions
from trade_manager import trade
from calc_stats import z_score
from orders import leverage

import json
import time

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)                                          #to avoid unwanted warnings


def save_status(status):
    with open("status.json", "w") as fp:
        json.dump(status, fp, indent=4)


if __name__ == "__main__":
    print("StatBot Initiated")

    # Initialising variables
    status_dict = {"message": "starting..."}
    order_long = {}
    order_short = {}
    positive_signal = False
    signal_side = ""
    switch = 0

    save_status(status_dict)

    # Setting leverage to 1
    print("Setting leverage...")
    leverage(instrument_1)
    leverage(instrument_2)
    print("Leverage set to 1x")

    print("Looking for trades...")
    while True:

        # To manage API limits
        time.sleep(3)

        # Checking if there's any open trades
        
        #to find average price and num of coins in open positions
        isPTickerOpen = check_positions(instrument_1)                                   
        isNTickerOpen = check_positions(instrument_2)
        
        #to fetch order status and quantity of the coin
        isPTickerActive = check_orders(instrument_1)
        isNTickerActive = check_orders(instrument_2)
        
        checks_all = [isPTickerOpen[0], isNTickerOpen[0], isPTickerActive[0], isNTickerActive[0]]                                   #could have avoided this variable
        isNewTrades = not any(checks_all)

        # Saving status
        status_dict["message"] = "Initial checks made..."
        status_dict["checks"] = checks_all
        save_status(status_dict)

        # Checking for signal and place new trades
        if isNewTrades and switch == 0:
            status_dict["message"] = "Managing new trades..."
            save_status(status_dict)
            switch, signal_side = trade(switch)

        if switch == 1:
            # Calculating the latest z-score
            zscore, positive_signal = z_score()

            # Closing positions
            if signal_side == "Positive" and zscore < 0:
                switch = 2
            if signal_side == "Negative" and zscore >= 0:
                switch = 2

            # Putting back to zero if trades are closed
            if isNewTrades and switch != 2:
                switch = 0

        # Closing all active orders and open positions
        if switch == 2:
            print("Closing all positions...")
            status_dict["message"] = "Closing existing trades..."
            save_status(status_dict)
            switch = exit_all_positions(switch)

            time.sleep(5)