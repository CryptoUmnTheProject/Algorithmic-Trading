#!/usr/bin/env python3
#you need this top line

'''
This algo works by taking in some file (you have to give the entire
file address i.e. /Users/..).
It will only work with the json files from the Data repo because it
parses out the average price for that day from the other data.
The method I used was to download the json file and run this code on the
downloaded file.

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

results = 'ResultsFor' + currency + "Keller"#this is the name of the results file
nfile = open(results, 'w')        #makes the new file

#----------------- This is where we declare the varibales we're going to use
variable = "weightedAverage"

smallAverageValues = []
smallAveragePrice = 0
longAverageValues = []
longAveragePrice = 0

movingAverageCalculation = 0

smallDays = 3 #small moving average
longDays = 10 #long moving average

tracker = 0   #for use in checking which entry we're at

pastSmallDays = False
pastLongDays = False

cashMoneySwagYolo = 10000   #Let's start with $10,000 in investment
moneytemp = cashMoneySwagYolo #use this var so we keep track of our starting dollar amount
buyMargin = .02             #buy if the moveing average is going up 2%
sellMargin = -0.005         #sell if the moveing average is going down .5%
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


#------------------ This is where the actual logic starts to work
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
    
    if tracker >= smallDays:
        pastSmallDays = True
    if tracker >= longDays:
        pastLongDays = True
        
    #the if and elif determine if we've passed the minimum short and long moving averages respectivly
    if not pastSmallDays and not pastLongDays:
        smallAverageValues.append(entry.get(variable))
        longAverageValues.append(entry.get(variable))
        
    elif pastSmallDays and not pastLongDays:
        smallAverageValues.append(entry.get(variable))
        longAverageValues.append(entry.get(variable))
        del smallAverageValues[0]
    
    else:
        # This is the really important part of the program
        smallAverageValues.append(entry.get(variable))
        longAverageValues.append(entry.get(variable))
        
        smallAveragePrice = sum(smallAverageValues)/len(smallAverageValues)  #find the average price over the small period of time
        longAveragePrice = sum(longAverageValues)/len(longAverageValues)     #find the average price over the long period of time
        movingAverageCalculation = smallAveragePrice/longAveragePrice - 1    #calculate the percentage change

        if cashMoneySwagYolo > 0 and movingAverageCalculation >= buyMargin:  #this is where we decide to invest
            investmentPrice = entry.get(variable)
            numberOfCurrency = cashMoneySwagYolo/investmentPrice
            cashMoneySwagYolo = 0                                            #invest entire portfolio
            
            #write to the results file
            nfile.write("Time: " + str(datetime.datetime.fromtimestamp(entry.get("date")).strftime("%Y-%m-%d %H:%M:%S")) + "\n")            #the time will be in linux time so you might have to convert it
            nfile.write("Bought at " + str(investmentPrice) + "\n")
            nfile.write("Current number of "+ currency + " is " + str(int(numberOfCurrency)) + "\n")
            nfile.write("------------------------\n")
            
        elif cashMoneySwagYolo == 0 and movingAverageCalculation <= sellMargin:  #and investmentPrice < entry.get(variable): #this ensures we never lose money
            cashMoneySwagYolo = entry.get(variable) * numberOfCurrency          #if we sell then sell entire holdings
            numberOfCurrency = 0

            #write to the results file
            nfile.write("Time: " + str(datetime.datetime.fromtimestamp(entry.get("date")).strftime("%Y-%m-%d %H:%M:%S")) + "\n")
            nfile.write("Sold at " + str(entry.get(variable)) + "\n")
            nfile.write("Current US dollar balance: $" + str(int(cashMoneySwagYolo)) + "\n")            
            nfile.write("------------------------\n")
            
        del smallAverageValues[0]  #make room for each list so new data can be added
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

nfile.write("Small moving average, number of days: " + str(smallDays) + "\n")
nfile.write("Long moving average, number of days: " + str(longDays) + "\n")
nfile.write("Buy Margin as a percent: " + str(buyMargin) + "\n")
nfile.write("Sell Margin as a percent: " + str(sellMargin))
print("Finished")
nfile.close()
jsonAddress.close()
