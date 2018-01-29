#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
from datetime import datetime

def xs(data):
    def helper(point):
        return datetime.fromtimestamp(point["date"])
    return list(map(helper, data))
def ys(data):
    def helper(point):
        return point["close"]
    return list(map(helper, data))

def save_chart(currency):
    plt.cla()
    with open("data/{}.json".format(currency)) as f:
        data = json.load(f)
    plt.plot(xs(data), ys(data))
    plt.savefig("charts/{}.png".format(currency))

with open("currencies.json") as f:
    currencies = json.load(f)

for currency in currencies:
    save_chart(currency)
