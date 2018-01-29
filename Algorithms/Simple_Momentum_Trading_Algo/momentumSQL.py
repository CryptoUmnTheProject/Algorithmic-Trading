#!/usr/bin/env python3
#you need this top line
import time
import datetime
print("Simple SQL momentum algorithm")
print("Start")
#todo add logic
currency = "DASH" #input what currency you want to test here if you've cloned the Data repo

import sqlite3
con = sqlite3.connect("/media/schn0921/778CF8814992BA37/snapshot-1505512821.db") #this part is just accessing the database, mine is stored on a flashdrive but yours will be differnet
c = con.cursor()
c.execute('''SELECT "askPrice" FROM ticker WHERE currencyBase = "DASH" \
AND currencyQuote = "XXBT"''') #get the dash information from the database

results = 'ResultsFor' + currency + "SQL.txt"#this is the name of the results file
nfile = open(results, 'w')        #makes the new file

smallAverageValues = []
smallAveragePrice = 0
longAverageValues = []
longAveragePrice = 0
#the entries are 3 seconds apart so 3 entries = 9 seconds of real-world time
smallEntries = 3 #small moving average
longEntries = 50 #long moving average

cashMoneySwagYolo = 10000   #Let's start with $10,000 in investment
buyMargin = .014             #buy if the moveing average is going up 2%
sellMargin = -0.0179         #sell if the moveing average is going down .5%
investmentPrice = 0         #what we bought at
numberOfCurrency = 0        #the amount of the currency we have
startTime = 0               #when we started the algo
endTime = 0                 #the last entry the algo looked at
lowestPrice = 0             #for calculating the minimum of all average prices
highestPrice = 0            #for calculating the maximum of all average prices
market = 0                  #for using lowestPrice and highestPrice to find best scenario
startCurrency = 0           #finding first entry price
lastCurrency = 0            #finding last entry price
marketOverall = 0           #finding the profit from absolute start to absolute finish

pastSmallDays = False
pastLongDays = False

tracker = 0
t0 = time.time()

for entry in c:
    
    if tracker == 0: #we do this to make sure we have at least one entry to look at
        smallAverageValues.append(entry[0])
        longAverageValues.append(entry[0])

    if tracker > 0: #needed to add this because the there are a few data points that were bad so this throws them out
        if entry[0]-10 > sum(smallAverageValues)/len(smallAverageValues):
            print(entry[0])
            continue
    tracker+=1
    #here we make sure we have the data we want
    if entry[0] != smallAverageValues[-1]:
        smallAverageValues.append(entry[0])
        if len(smallAverageValues) > smallEntries:
            del smallAverageValues[0]
    if entry[0] != longAverageValues[-1]:
        longAverageValues.append(entry[0])
        if len(longAverageValues) > longEntries:
            del longAverageValues[0]

    if len(longAverageValues) == longEntries and len(smallAverageValues) == smallEntries:
        #start algo
        smallAveragePrice = sum(smallAverageValues)/len(smallAverageValues)  #find the average price over the small period of time
        longAveragePrice = sum(longAverageValues)/len(longAverageValues)     #find the average price over the long period of time
        movingAverageCalculation = smallAveragePrice/longAveragePrice - 1    #calculate the percentage change
        #print(movingAverageCalculation)    #lets us see what our moving average is

        if cashMoneySwagYolo > 0 and movingAverageCalculation >= buyMargin:  #this is where we decide to invest
            investmentPrice = entry[0]
            numberOfCurrency = cashMoneySwagYolo/investmentPrice
            cashMoneySwagYolo = 0                                            #invest entire portfolio

            #write to the results file
            nfile.write("Bought at " + str(investmentPrice) + "\n")
            nfile.write("Current number of "+ currency + " is " + str(int(numberOfCurrency)) + "\n")
            nfile.write("------------------------\n")

        elif cashMoneySwagYolo == 0 and entry[0] > investmentPrice and movingAverageCalculation <= sellMargin: #
            cashMoneySwagYolo = entry[0] * numberOfCurrency          #if we sell then sell entire holdings
            numberOfCurrency = 0

            #write to the results file
            nfile.write("Sold at " + str(entry[0]) + "\n")
            nfile.write("Current US dollar balance: $" + str(int(cashMoneySwagYolo)) + "\n")
            nfile.write("------------------------\n")

#--------------------- If at the end of the analysis we only have crypto currency, sell it all and get the US dollar amount
if cashMoneySwagYolo == 0:
    cashMoneySwagYolo = entry[0] * numberOfCurrency
    numberOfCurrency = 0

nfile.write("Final account holdings in US dollars (algorithm results): $" + str("{:,}".format(int(cashMoneySwagYolo))) + "\n\n")
print("Finished")
t1 = time.time()
total = t1-t0
print(total)    #this allows us to see how long the algo took, this algo should take 7 minutes or less to run
nfile.close()
