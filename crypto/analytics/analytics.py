import pandas as pd
import numpy as np
import json
from datetime import date
from crypto.data.loader import cleaned_dataset


def getCoin(dataset, coin):
    return dataset[(dataset['Coin'] == coin)]


def getDates(dataset, startDate, endDate):
    return dataset[((dataset['Date'] >= startDate) & (dataset['Date'] <= endDate))]


def getDate(dataset, date):
    return dataset[(dataset['Date'] == date)]


def getSorted(data, column, asc = False):
    return data.sort_values(by=column, ascending=asc).dropna()


def getClose(data, coin, date):
    dataDate = getDate(data, date)
    dataCoin = getCoin(dataDate, coin)
    return float(dataCoin["Close"].values[0])


def top10_by_market_cap(top100):
    top10 = top100[top100['Date'] == '2017-12-18'].sort_values('Market-Cap', ascending=False)
    print(top10[['Coin', 'Market-Cap']][:10])
    top10[['Coin', 'Market-Cap']][:10].to_csv('top10_marketcap.csv')
    print(top10[['Coin', 'Market-Cap']][-10:])
    top10[['Coin', 'Market-Cap']][-10:].to_csv('bottom10_market_cap.csv')


def top_by_market_cap(dataset, date='2017-12-18'):
    dataset = dataset[top100['Date'] == date].sort_values('Market-Cap', ascending=False)
    return dataset


def get_historical_data(top100, ticker, start, end):
    return top100[
        (top100['Coin'] == ticker) &
        (top100['Date'] >= start) &
        (top100['Date'] <= end)][['Date', 'Volume', 'Close', 'Market-Cap']]


# get all from top 100 that are traded at the exchanges passed in as parameter
def filtered_data(top100, exchange_names):
    top100 = top100[top100['Coin'].isin(exchange_names)]
    top100 = top100[top100['Date'] == '2017-12-18']

    print(top100)


def under_20c_cost_analysis(dataset):
    current_values = dataset[dataset['Date'] == '2017-12-22']
    under_20c = current_values[current_values['Close'] < 0.2]

    print('Coins')
    print(under_20c[['Coin', 'Close']])
    print('Total: ' + str(under_20c['Close'].round(4).sum() * 100))


def under_200mil_market_cap(dataset):
    current_values = dataset[dataset['Date'] == '2017-12-22']
    under_200_market_cap = current_values[current_values['Market-Cap'] < 200000000]

    print('Under 200 mil market-cap')
    print(under_200_market_cap[['Coin', 'Market-Cap', 'Close']])


dataset = cleaned_dataset()
#top10_by_market_cap(dataset)
# current = get_historical_data(dataset, 'litecoin', '2017-12-16', '2017-12-18')

hist = get_historical_data(dataset, 'bitcoin', '2017-10-17', '2017-10-18')
print(hist)
# current['diff'] = (current['Close'] - hist['Close'].values[0]) / hist['Close'].values[0]
# print(current)

#filtered_data(dataset, per_exchange_currencies(['Poloniex', 'Bitfinex']))

# under_20c_cost_analysis(dataset)

# under_200mil_market_cap(dataset)
