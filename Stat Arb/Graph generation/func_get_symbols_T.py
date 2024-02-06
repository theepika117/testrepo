from config_strategy_api_T import symbols

print("function initiated")
# Get symbols that are tradeable
def get_tradeable_symbols():

    #creating an empty dictionary to append symbols 
    symbol_list = list()
    f = open("generatedSymbol.txt","w")
    for symbol in symbols :
        if symbol["status"] == "Trading" and symbol["quoteCoin"] == "USDT" :
            symbolString = symbol['symbol'] #+ symbol['priceFilter']
            symbol_list.append(symbolString)
            f.write(str(symbolString))
            f.write("\n")
    
    
    f.close()
    with open("generatedSymbol.txt", "r") as file:
        file_contents = file.read()
    #print("Contents of generatedSymbol.txt:")
    #print(file_contents)

    return symbol_list
