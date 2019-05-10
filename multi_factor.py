import pandas as pd
import numpy as np
from core import *

factor_prices = pd.read_csv(
    'data/factor-prices-clean.csv',
    index_col='Date',
    parse_dates=True)

monthly_returns = factor_prices.resample('M').last().pct_change()
window = 6
sfr = monthly_returns.rolling(window).apply(scaled_factor_return, kwargs={'j':window}, raw=True)

scale = monthly_returns.rolling(window).apply(scaling_factor, kwargs={'j':window}, raw=True)


# TSFM_Long
ln = sfr[scale > 0.0].sum(axis=1)
ld = scale[scale > 0.0].sum(axis=1)

tsfm_long = ln.div(ld).fillna(0.0)

sn = sfr[scale <= 0.0].sum(axis=1)
sd = scale[scale <= 0.0].sum(axis=1)

tsfm_short = sn.div(sd).fillna(0.0)

tsfm_LS = tsfm_long + tsfm_short

print(np.cumprod(tsfm_LS + 1.0) - 1.0)