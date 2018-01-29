# Historical Data
## Second by second and every four hours

The data in the ‘data’ folder consists of data points from every four hours of the specified currency.  If you want to remote to the SQL database that contains the second by second data, then use this link:
http://home.remexre.xyz:8001/snapshot-1505512821-57e9cd8?sql=select+*+from+ticker+where+currencyBase+%3D+%22BCH%22+and+currencyQuote+%3D+%22ZUSD%22+limit+1000

Right now the link only supports commands that take up to 1 second to process so keep sample sizes 1000 or less.  Props to Nathan Ringo for putting the database together!

If the link above is down, you can download the 6 gig chunk of data here: https://acm.umn.edu/~nathan/snapshot-1505512821.db

# historical-data

Scripts to download and plot historical data of various currencies.

## Usage

To fetch updated data, run

```bash
$ rm -r data
$ python3 get_historical_data.py
Got BTC vs. AMP data
Got BTC vs. ARDR data
Got BTC vs. BCN data
...
Got BTC vs. XRP data
Got BTC vs. XVC data
Got BTC vs. ZEC data
$ # done!
```

To plot data, run

```bash
$ rm -r charts
$ python3 make_charts.py
$ # done!
```
