from datetime import datetime
import pandas as pd
import requests
from sklearn.preprocessing import MinMaxScaler


class CovalentReader():
    def __init__(self, api_key):
        self.api_key = api_key

    def get_ts(self, contract):
        # call Covalent API, return response in JSON
        url = f'https://api.covalenthq.com/v1/1/nft_market/collection/{contract}/?page-size=2000&key={self.api_key}'
        headers = {'Authorization': 'application/json'}
        response = requests.get(url, headers=headers) 
        ts = response.json()
        return ts

    def format_ts(self, ts):
        d = {}
        cols = ['collection_name', 'floor_price_quote_7d', 'average_volume_quote_day', 'volume_quote_day', 
            'unique_token_ids_sold_count_day', 'floor_price_wei_7d', 'average_volume_wei_day', 
            'volume_wei_day', 'gas_quote_rate_day']
        for item in ts['data']['items']:
            # key is date, value is array of cols
            op_date = item['opening_date']
            op_date = datetime.strptime(op_date, "%Y-%m-%d")
            row = []
            for col in cols:
                row.append(item[col])
            d[op_date] = row
        return d

    def dict_to_df(self, d):
        cols = ['name', 'floor_7d', 'avg_volume_1d', 'volume_1d', 'sold_1d', 'floor_wei_7d', 
            'avg_volume_wei_1d', 'volume_wei_1d', 'gas_1d']
        df = pd.DataFrame.from_dict(d, orient='index', columns=cols)
        return df

    def get_df(self, address):
        ts = self.get_ts(address)
        d = self.format_ts(ts)
        self.df = self.dict_to_df(d)
        return self.df

    def format_columns(self, df, target):
        df2 = df.reset_index()
        df2 = df2[['index', target]]
        df2.columns = ['ds', 'y']
        return df2

    def normalize(self, df):
        arr = df['y'].to_numpy().reshape(-1, 1)
        scaled = MinMaxScaler().fit_transform(arr)
        df['y'] = scaled.flatten()
        return df

    def load_data(self, address, target):
        df = self.get_df(address)
        df = self.format_columns(df, target)
        self.df_norm = self.normalize(df)
        return self.df_norm
