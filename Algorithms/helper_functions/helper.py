import json
from os import path
import datetime
import sqlite3
import time
import urllib.request
'''
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("www.blahinc.com",80))
'''
#will need to be changed so we can connect to server
def getUrlforBTC(time):#time should come in form yyyymmdd so feb 7 2014 would be 20140207
    '''
    time = str(time)
    url = 'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1391803200&end=1391803200&period=300'
    #url = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="+time+"&end="+time
    openUrl = urllib.request.urlopen(url)
    r = openUrl.read()
    openUrl.close()
    d = json.loads(r.decode())
    '''
    return 712.40
#todo
def getUrlforDollars(time):
    return 2173.40
#todo

def getInfo(altCoin):#takes a string
    jsonAddress = open('/Users/ericschneider/Desktop/Algorithmic-Trading/Data/data/' + altCoin + '.json',"r") #give the whole address of the file
    jsonFile = json.load(jsonAddress)
    jsonAddress.close()
    return jsonFile

def convertToBTC(results_file, dollars, time):
    time = str(time)
    results_file.write("Time: "+time+"\n")
    
    btc = getUrlforBTC(time)
    results_file.write("Bought BTC at: "+str(btc)+"\n")
    
    number_of_btc = dollars/btc
    results_file.write("Number of BTC: "+str(number_of_btc)+"\n")
    results_file.write("----------------\n")
    return number_of_btc

def converToDollars(results_file, btc, time):
    time = str(time)
    results_file.write("Time: "+str(time)+"\n")
    
    dollars = getUrlforDollars(time)
    results_file.write("Sold BTC at: "+str(dollars)+"\n")
    
    number_of_dollars = btc*dollars
    results_file.write("Number of US Dollars: "+str(number_of_dollars)+"\n")
    return number_of_dollars

def recordBuy(results_file, coin, time, price, number_of_coin):    
    results_file.write("Time: "+str(time)+"\n")
    results_file.write("Bought at "+str(price)+"\n")
    results_file.write("Current number of "+str(coin)+" is "+str(number_of_coin)+"\n")

def recordSell(results_file, coin, time, price, number_of_btc):
    results_file.write("------------------\n")
    results_file.write("Time: "+str(time)+"\n")
    results_file.write("Sold at "+str(price)+"\n")
    results_file.write("Current number of BTC is "+str(number_of_btc)+"\n")
    results_file.write("------------------\n")
    
def getInfoSQL(fromCurr, toCurr, price, limit):
    '''fromCurr - which currency we're going from
       toCurr - which currency we want to get
       price - what kind of price like asking price of buy price
       limit - max size
       
       ex: if I was the price from btc to dash at a given time then call:
           getInfo(XXBT, DASH, askPrice,100)

       IMPORTANT:
          If no LIMIT is wanted, then pass 0 into the limit option
    '''
    fromCurr = str(fromCurr)
    toCurr = str(toCurr)
    price = str(price)
    limit = str(limit)

    con = sqlite3.connect("/Volumes/Untitled/snapshot-1505512821.db") #this part is just accessing the database, mine is stored on a flashdrive but yours will be different
    c = con.cursor()

    if limit == 0:
        command = "SELECT "+ price+' FROM ticker WHERE currencyBase = "' +toCurr+ '" AND currencyQuote = "'+fromCurr+'"'
    else:
        command = "SELECT "+ price+' FROM ticker WHERE currencyBase = "' +toCurr+ '" AND currencyQuote = "'+fromCurr+'" LIMIT '+limit
    c.execute(command) #get the dash information from the database
    con.close()
    return c
#THIS FUNCTION NEEDS TESTING
def convert_to_altcoin(dollars, altcoin, time):#time in unix
    con = sqlite3.connect("/Volumes/Untitled/snapshot-1505512821.db") #this part is just accessing the database, mine is stored on a flashdrive but yours will be different
    c = con.cursor()

    altcoin = str(altcoin)
    command = 'SELECT "askPrice" FROM ticker WHERE currencyBase = "' + altcoin+ '" AND currencyQuote = "ZUSD" LIMIT 10'
    print(command)
    conversion_value = 1
    for i in c:
        print(i)
        conversion_value = i[0]
    c.execute(command) #get the dash information from the database
    con.close()
    return dollars/conversion_value

