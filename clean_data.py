import pandas as pd

factor_prices = pd.read_csv('data/factor-prices.csv', parse_dates = ['Date'], index_col = 'Date').dropna(how='all')
factor_prices.fillna(method='pad', inplace=True)
factor_prices.dropna(inplace=True)
factor_prices.to_csv('data/factor-prices-clean.csv')