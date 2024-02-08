from settings import symbols                    #list of instruments that we got through API


def instruments():
    trade_list = dict()                         #dictionary to store available symbols
    
    file = open("Available Instruments.txt", "w")               
    for symbol in symbols:

        #we are intrested in only those coins which is in trading state and the currency value is USDT
        
        conditions = [symbol["status"] == "Trading", symbol["quoteCoin"] == "USDT"]                 #conditions variable is not stricly neccessary. could have directly used it in the nxt line or could have used and condition                         
        if all(conditions):                                                                 
            trade_list[symbol["symbol"]] = symbol
            file.write(symbol["symbol"] + "\n")                                                #file will contain only the symbol names
    file.close()
    return trade_list