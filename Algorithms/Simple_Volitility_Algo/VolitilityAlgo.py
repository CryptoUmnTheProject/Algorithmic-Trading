#!/usr/bin/env python3
#you need this top line

'''
The variables are borrowed heavily from the momentum algo.

This is a simple algorithm that I wrote up over break. It doesn't work well
but I wanted to see what would happen if I created a volitility algo.

The logic is that it checks to see where the last entry falls on a range
from the lowest and highest values over a given period of time.
In this implementation, if the price is at or above 70% of the values range,
then we think the price will increase so buy.
If the moving price falls bellow 60% then sell because we think the price will
go down.
I'm submitting this so that we can see that not all ideas work well
in reality.
'''

#----------------- Opening and creating files
import json
from os import path
import datetime
print("Simple momentum algorithm")
print("Start")

currency = "DASH" #input what currency you want to test here if you've cloned the Data repo

jsonAddress = open('/Users/ericschneider/Documents/hft/Data/data/' + currency + '.json',"r") #give the whole address of the file
jsonFile = json.load(jsonAddress)

results = 'ResultsFor' + currency + "Volitility"#this is the name of the results file
nfile = open(results, 'w')

#----------------- This is where we declare the varibales we're going to use
variable = "weightedAverage"

movingAverageCalculation = 0

longDays = 12 #long moving average
longAverageValues = []

tracker = 0   #for use in checking which entry we're at

pastLongDays = False

cashMoneySwagYolo = 10000   #Let's start with $10,000 in investment
moneytemp = cashMoneySwagYolo #use this var so we keep track of our starting dollar amount
buyMargin = .7             #buy if the price is at least 70% of the range
sellMargin = .6         #sell if the price is less than 60% of the range
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

for entry in jsonFile:
    if tracker == 1:
        startTime = entry.get("date")
        startCurrency = entry.get(variable)
        lowestPrice = entry.get(variable)
    tracker += 1

    if lowestPrice > entry.get(variable):
        lowestPrice = entry.get(variable)
    if highestPrice < entry.get(variable):
        highestPrice = entry.get(variable)
    
    if tracker >= longDays:
        pastLongDays = True
    if not pastLongDays:
        longAverageValues.append(entry.get(variable))
    else:
        longAverageValues.append(entry.get(variable))

#this is where we calculate the range and the variable's proportions therein
        minn = min(longAverageValues)
        maxx = max(longAverageValues)
        calc = (maxx - minn)
        valu = (entry.get(variable)-minn)/calc
       
        if cashMoneySwagYolo > 0 and  valu > buyMargin:
            investmentPrice = entry.get(variable)
            numberOfCurrency = cashMoneySwagYolo/investmentPrice
            cashMoneySwagYolo = 0                                            #invest entire portfolio
            
            #write to the results file
            nfile.write("Time: " + str(datetime.datetime.fromtimestamp(entry.get("date")).strftime("%Y-%m-%d %H:%M:%S")) + "\n")            #the time will be in linux time so you might have to convert it
            nfile.write("Bought at " + str(investmentPrice) + "\n")
            nfile.write("Current number of "+ currency + " is " + str(int(numberOfCurrency)) + "\n")
            nfile.write("------------------------\n")
        elif cashMoneySwagYolo == 0 and valu < sellMargin:
            cashMoneySwagYolo = entry.get(variable) * numberOfCurrency          #if we sell then sell entire holdings
            numberOfCurrency = 0

            #write to the results file
            nfile.write("Time: " + str(datetime.datetime.fromtimestamp(entry.get("date")).strftime("%Y-%m-%d %H:%M:%S")) + "\n")
            nfile.write("Sold at " + str(investmentPrice) + "\n")
            nfile.write("Current US dollar balance: $" + str(int(cashMoneySwagYolo)) + "\n")            
            nfile.write("------------------------\n")
            
         #make room for each list so new data can be added
        del longAverageValues[0]
        endTime = entry.get('date')
        endCurrency = entry.get(variable)
        
#--------------------- If at the end of the analysis we only have crypto currency, sell it all and get the US dollar amount
if cashMoneySwagYolo == 0:
    cashMoneySwagYolo = entry.get(variable) * numberOfCurrency
    numberOfCurrency = 0
    
#--------------------- Calculate what the best market (non algo assisted) result would be
market = (moneytemp/lowestPrice)*highestPrice

#--------------------- Get overall market earnings from start to finish
marketOverall = (moneytemp/startCurrency) * endCurrency

#--------------------- Close files and report results
nfile.write("\nStart time was: " + str(datetime.datetime.fromtimestamp(startTime).strftime("%Y-%m-%d %H:%M:%S")) + "\n")
nfile.write("End time was: " + str(datetime.datetime.fromtimestamp(endTime).strftime("%Y-%m-%d %H:%M:%S")) + "\n\n")

nfile.write("The markets maximum earnings were: $" + str("{:,}".format(int(market))) + "\n")
nfile.write("The markets earnings from start to finish were: $" + str("{:,}".format(int(marketOverall))) + "\n")
nfile.write("Final account holdings in US dollars (algorithm results): $" + str("{:,}".format(int(cashMoneySwagYolo))) + "\n\n")

nfile.write("Buy Margin as a percent: " + str(buyMargin) + "\n")
nfile.write("Sell Margin as a percent: " + str(sellMargin))
print("Finished")
nfile.close()
jsonAddress.close()
