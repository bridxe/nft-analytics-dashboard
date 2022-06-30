from darts import TimeSeries
from darts.models.forecasting.tft_model import TFTModel
from darts.models import ExponentialSmoothing

class TsForecast:
    def __init__(self, df):
        self.df = df

    def create_ts(self, col):
        self.ts = TimeSeries.from_dataframe(self.df, 'ds', col)

    def cv_ets(self, steps):
        train, val = self.ts[:-steps], self.ts[-steps:]
        model = ExponentialSmoothing()
        model.fit(train)
        prediction = model.predict(len(val), num_samples=1000)
        self.ts.plot()
        prediction.plot(low_quantile=0.05, high_quantile=0.95)

    def predict_ets(self, steps):
        model = ExponentialSmoothing()
        model.fit(self.ts)
        prediction = model.predict(steps, num_samples=1000)
        self.ts.plot()
        prediction.plot(low_quantile=0.05, high_quantile=0.95)