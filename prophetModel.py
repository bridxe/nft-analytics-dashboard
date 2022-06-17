from fbprophet import Prophet
import pandas as pd


class ProphetModel():
    def __init__(self, df, daily, yearly):
        self.df = df
        self.prophet = Prophet(daily_seasonality=daily, yearly_seasonality=yearly)

    def train_test_split(self, size):
        self.forecast = size < 1
        if not self.forecast:
            self.test, self.train = self.df[:size], self.df[size:]
    
    def train(self):
        self.prophet.fit(self.df) if self.forecast else self.prophet.fit(self.train)

    def test(self):
        test_dates = pd.DataFrame(self.test['ds'].values)
        test_dates.columns = ['ds']
        self.res = self.prophet.predict(test_dates)
        return self.res

    def forecast(self, days):
        future_dates = self.df['ds'] + pd.Timedelta(days=days)
        future_dates = pd.DataFrame(future_dates[:days])
        self.res = self.prophet.fit(future_dates)
        return self.res
        