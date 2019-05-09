import numpy as np
from scipy.stats.mstats import winsorize
from typing import List
Vector = List[float]



def sigma(factor_returns: Vector, j: int) -> float:
    """
    Annulaized Factor Volatility

    Parameters
    ----------
    factor_returns : array-like
        Monthly returns of the factor.
    j : int
        Formation window in months.

    Returns
    -------
    sigma : float
        Annualized factor volatility
    """
    time_period = lambda x: 36 if j < 12 else 120
    tp = time_period(j)
    factor_vol = factor_returns[-tp:].var()**(12.0 / tp)
    return factor_vol


def scaling_factor(factor_returns: Vector, j: int) -> float:
    ann_vol = 1.0 / sigma(factor_returns, j)
    vol_scaled = ann_vol * factor_returns[-j:].sum()
    return vol_scaled.clip(-2.0, 2.0)


def scaled_factor_return(factor_returns: Vector, j: int) -> float:
    """
    Scaled Factor Return

    Scales the one month returns
    according to the performance over the past j months.

    Parameters
    ----------

    Returns
    -------
    scaled_return : float
    """
    if len(factor_returns) < j:
        print("j must be less than the length of the returns series")
        return
    s = scaling_factor(factor_returns, j)
    scaled_return = factor_returns[-1] * s
    return scaled_return


