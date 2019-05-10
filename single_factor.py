from core import *
import pandas as pd

factor_prices = pd.read_csv(
    'data/factor-prices-clean.csv', index_col='Date', parse_dates=True)

test1 = factor_prices['R1FPMF Index']

j = 6
factor_returns = test1.resample('M').last().pct_change()

sfr = factor_returns.rolling(j).apply(scaled_factor_return, kwargs={'j':j})
sc = factor_returns.rolling(j).apply(scaling_factor, kwargs={'j':j})

sfr.to_csv('data/single_factor.csv')

sc.to_csv('data/single_factor_scaling.csv')

factor_returns.to_csv('data/single_returns.csv')
