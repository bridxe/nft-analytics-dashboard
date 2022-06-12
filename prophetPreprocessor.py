from covalentReader import CovalentReader
from sklearn.preprocessing import MinMaxScaler

class ProphetPreprocessor(CovalentReader):
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
        df = self.normalize(df)
        return df
        