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

    def calmar(self, days):
        calmar, max_drawdown, returns = [], [], []
        for i in range(0, len(self.df) - days):
            sample = self.df['y'][i:i+days]
            print(sample)
            peak = trough = sample[i]
            drawdown = 1
            for j in range(1, days):
                # case 1: greater than previous peak
                if sample[i+j] > peak:
                    drawdown = min((trough - peak) / peak, drawdown)
                    peak = trough = sample[i+j]
                else:
                    trough = min(sample[i+j], trough)
            drawdown = min((trough - peak) / peak, drawdown)
            max_drawdown.append(drawdown)

            ret = (sample[i+days-1] - sample[i]) / sample[i]
            returns.append(ret)

            calmar.append(ret / drawdown)

        self.df['max_drawdown'] = pd.Series(np.array(max_drawdown))
        self.df['returns'] = pd.Series(np.array(returns))
        self.df['calmar'] = pd.Series(np.array(calmar))

        return self.df[['max_drawdown', 'returns', 'calmar']]

    def sharpe(self, days):
        er = self.estimated_returns()
        sharpe = []
        for i in range(0, len(er) - days):
            er_sample = er[i:i+days]
            sharpe.append(er_sample.mean() / er_sample.std())
        self.df['sharpe'] = pd.Series(np.array(sharpe))

    def sortino(self, days):
        er = self.estimated_returns()
        sortino = []
        for i in range(0, len(er) - days):
            er_sample = er[i:i+days]
            downside = np.array([x for x in er_sample if x < 0])
            dr = downside.std() if len(downside) > 0 else 0
            sortino.append((er_sample.mean() * days) / (dr * np.sqrt(days)))
        self.df['sortino'] = pd.Series(np.array(sortino))
        