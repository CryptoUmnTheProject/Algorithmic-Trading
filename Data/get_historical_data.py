#!/usr/bin/env python3

import json
from os import mkdir
from os.path import isdir
from requests import get
from time import sleep

def get_rates(_from, _to):
    r = get("https://poloniex.com/public?command=returnChartData&currencyPair={}_{}&start=0&end=9999999999&period=14400".format(_from, _to))
    assert r.status_code is 200
    return r.json()

with open("currencies.json") as f:
    currencies = json.load(f)

if not isdir("data"):
    mkdir("data")

for c in currencies:
    sleep(1/4)
    with open("data/" + c + ".json", "w") as f:
        json.dump(get_rates("BTC", c), f)
    print("Got BTC vs. {} data".format(c))
