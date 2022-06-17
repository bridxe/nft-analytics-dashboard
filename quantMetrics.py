import numpy as np
import pandas as pd

class QuantMetrics:
    def __init__(self, df):
        self.df = df

    def get_src(self):
        return self.df

    def estimated_returns(self):
        er = np.array([1 - self.df['y'][i] / self.df['y'][i-1] for i in range(1, len(self.df))])
        er[-1] = 0
        er = np.append(er, [0])
        self.df['er'] = pd.Series(er)
        return er
