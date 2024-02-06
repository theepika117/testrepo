from config_strategy_api_T import z_score_window
from func_get_symbols_T import get_tradeable_symbols
from func_price_klines_T import store_price_history

generated_sym = get_tradeable_symbols()



print("Hello")

# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)
# from func_get_symbols_T import get_tradeable_symbols


sym_response = get_tradeable_symbols()

#print(sym_response)

# print("Constructing and saving price data to JSON...")
# if len(sym_response) > 0:
store_price_history(sym_response)

# for sym in sym_response:
#     print(sym,end=" ")
#     store_price_history(sym)
#     print()