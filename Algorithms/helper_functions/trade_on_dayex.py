import datetime

import sys
sys.path.insert(0, '/Users/ericschneider/Desktop/Algorithmic-Trading/Algorithms/helper_functions/')
import helper

coin= "DASH"
info = helper.getInfo(coin)
results_file = open("results_for_happy.txt",'w')

dollars = 1000
amount_of_coin = 0
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

    if "Mon" in date and btc > 0:
        amount_of_coin = btc/price
        btc = 0

        helper.recordBuy(results_file, coin, date, price, amount_of_coin)

    elif "Sat" in date and amount_of_coin > 0:
        btc = amount_of_coin * price
        amount_of_coin = 0

        helper.recordSell(results_file, coin, date, price, btc)

if btc > 0:
    helper.converToDollars(results_file, btc, date)
else:
    btc = amount_of_coin * price
    amount_of_coin = 0
    helper.converToDollars(results_file, btc, date)

print("Done!")
results_file.close()
