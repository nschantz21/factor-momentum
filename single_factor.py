from core import *
import pandas as pd
from scipy.stats.mstats import winsorize

factor_prices = pd.read_csv(
    'data/factor-prices-clean.csv', index_col='Date', parse_dates=True)

test1 = factor_prices['R1FPMF Index']

j = 6
factor_returns = test1.resample('M').last().pct_change()

print(factor_returns.rolling(j).apply(scaled_factor_return, kwargs={'j':j}))
print(factor_returns.rolling(j).apply(scaling_factor, kwargs={'j':j}))

