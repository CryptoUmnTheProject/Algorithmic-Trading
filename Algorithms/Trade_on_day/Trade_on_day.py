import time
import datetime

import sys
sys.path.insert(0, '/Users/ericschneider/Desktop/Algorithmic-Trading/Algorithms/helper_functions/')
import helper

altcoin = "DASH"
info = helper.getInfo(altcoin)
results_file = open("dayTest_results.txt",'w')

dollars = 10000
amount_of_altcoin = 0
btc = 0

for entry in info:
    """
    {'close': 0.002681, 'date': 1397073600, 'open': 0.001, 'quoteVolume': 6313.01079809,
    'high': 0.002681, 'weightedAverage': 0.00247511, 'volume': 15.62544098, 'low': 0.001}
    """
    date = datetime.datetime.fromtimestamp(entry.get('date')).strftime("%c")
    """
    Wed Apr  9 15:00:00 2014
    Thu Apr 10 19:00:00 2014
    """
    price = entry.get('weightedAverage')
    
    if btc == 0 and dollars > 0:
        btc = helper.convertToBTC(results_file, dollars, entry.get('date'))
        dollars = 0
        hodl_buy = btc/price
        
    if 'Mon' in date and btc > 0:        
        amount_of_altcoin = btc/price
        btc = 0

        helper.recordBuy(results_file, altcoin, date, price, amount_of_altcoin)
    
    elif 'Sat' in date and amount_of_altcoin > 0:
        btc = amount_of_altcoin*price
        amount_of_altcoin = 0

        helper.recordSell(results_file, altcoin, date, price, btc)
        
    hodl_sell = hodl_buy*price

if btc > 0 :
    helper.converToDollars(results_file, btc, date)
else:
    btc = amount_of_altcoin*price
    amount_of_altcoin = 0
    helper.converToDollars(results_file, btc, date)
    
hodl_sell = hodl_sell * 2173.40
results_file.write("HODL ideology "+ str(hodl_sell))
print("Done!")
results_file.close()
