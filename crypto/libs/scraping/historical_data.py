import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def get_historical_data(crypto, mode='a', include_header=False):
    try:

        crypto = crypto.split(":")
        symbol = crypto[1]
        crypto = crypto[0]

        url = 'https://coinmarketcap.com/currencies/{crypto}/historical-data/?start=20000428&end={end}'
        url = url.format(crypto=crypto, end=datetime.today().strftime('%Y%m%d'))

        page = requests.get(url)
        contents = page.content

        soup = BeautifulSoup(contents, 'html.parser')
        table = soup.find("table", { "class" : "table" })
        table_rows = table.find_all('tr')

        columns = [elem.text.replace(' ', '-') for elem in table_rows[0].find_all('th')]
        columns.insert(0, 'Coin')
        columns.insert(0, 'Symbol')

        rows = []

        for i in range(1, len(table_rows)):
            row = [data.text.replace(',', '.') for data in table_rows[i].find_all('td')]
            row.insert(0, crypto)
            row.insert(0, symbol)

            rows.append(row)


        df = pd.DataFrame(rows)
        if include_header:
            df.columns = columns

        with open('crypto/data/coin_data.csv', mode) as f:
            df.to_csv(f, index=False, header=include_header)
    except:
        print('Currency ', crypto)
