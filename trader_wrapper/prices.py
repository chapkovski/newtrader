"""
This module generates prices. It is totally independent from the rest of the app
(that way we can move it somewhere else (AWS LAmbda?) or send back to others for developemnt.
"""

import numpy as np
import numpy.random as npr

allowed_types = ['normal', 'etf']
# TODO: move most of these params to be read from params.csv or S3 or google drive.
#  Right now it's better to keep then inhouse
T = 1  # end of round
r = 0.1  # risk-free rate
sigma = 0.2  # stock volatility
pi = 0.2  # Sharpe ratio of the stock


class Stock:
    dt = None

    def __init__(self, initial, leverage=1, **kwargs):
        self.leverage = leverage
        self.initial = initial
        # these following we need so we can override them for specific stocks
        self.sigma = kwargs.get('sigma', sigma)
        self.pi = kwargs.get('pi', pi)
        self.r = kwargs.get('r', r)

    def generate_prices(self, n):
        u = self.leverage
        r = self.r
        pi = self.pi
        sigma = self.sigma
        dt = np.float(T) / n
        S = np.zeros(n)
        shocks = npr.randn(n + 1)
        S[0] = self.initial
        for t in range(1, n):
            S[t] = S[t - 1] * np.exp(
                (r + u * pi * sigma - 0.5 * (u * sigma) ** 2) * dt + u * sigma * np.sqrt(dt) * shocks[t])
        return S.tolist()


def get_prices(stocks, n):
    """
    n - length of the price array;
    stocks - stock params
    stock param looks like an obj/dict with the following params

        - leverage (optional; default: 1, used for etfs only)
        - initial value;
        - pi; optional.default: see top of the module ; Sharpe ratio of the stock
        - sigma; optional.default: see top of the module ; stock volatility
        - r; optional.default: see top of the module ;  risk-free rate
        example of stocks:
        [{'leverage':2,'initial':100}]
        type of the stock (normal vs. etf) is implicitly set via leverage.
    return array of arrays of values of length n each.
    """
    stocks_to_update = stocks.copy()

    for i in stocks_to_update:
        s = Stock(**i)
        i['prices'] = s.generate_prices(n)
    return stocks_to_update
