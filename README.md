# factor-momentum

# Factor Momentum {{in code}}
Converting the momentum strategy presented in *[Factor Momentum Everywhere](https://www.aqr.com/Insights/Research/Working-Paper/Factor-Momentum-Everywhere)* by Tarun Gupta and Bryan Kelly into python code.

## Abstract

The Sub Factor (SF) constructions are unique to those factors.  
Aggregate Sub Factors (ASF) are based on the correlation of returns of the Sub Factors.  

The Time Series Factor Momentum (TSFM) factor is then constructed from the Momentum of ASF (MASF). - **Not sure about that**. 

TSFM include 1-1, 2-12, 13-60, and 1-12 momentum portfolios.  
x-y refers to the factor level observed y months in the past less the level observed x months in the past. The exception is 1-1 which refers to the current level less the level observed one month ago.

## Implementation
Use one-month holding periods and consider various formation windows of one month up to five years (60 months).   

Dynamically scale one-month returns of the *i*th factor, $f_{i,t+1}$ according to its performance over the past *j* months.

### Scaled Factor returns
$f^{TSFM}_{i,j,t+1}=s_{i,j,t} \times f_{i,t+1}$  

```python
def scaled_factor_return(factor_returns:list(float), j:int) -> float:
    """
    Scaled Factor Return

    Scales the one month returns according to the performance over the past j months.
    Parameters
    ----------

    Returns
    -------
    scaled_return : float
    """
    if len(factor_returns) < j:
        print("j must be less than the length of the returns series")
        return;
    s = scaling_factor(factor_returns, j)
    scaled_return = factor_returns[0] * s
    return scaled_return
```

The scaling term *s* is used to time positions in factor *i* based on the factor's return over the formation period (*t* - *j* to *t*)

### Scaling Factor
$s _{i,j,t} = \min(\max(\frac{1}{\sigma_{i,j,t}} \Sigma^{j}_{T=1}{f_{i,t-T+1}}, -2),2)$

```python
import numpy as np
from scipy.stats.mstats import winsorize

def scaling_factor(factor_returns:list(float), j:int) -> float:
    ann_vol = 1.0 / sigma(factor_returns j)
    vol_scaled = ann_vol * np.sum(factor_returns)
    return winsorized(vol_scaled, (-2.0, 2.0))
```

The factor returns are scaled by a *z*-score winsorized at (-2, 2).  
The *z*-score is based on the annualized factor volatility over the past three years if j < 12, and over the past 10 years if j $\ge$ 12

```python
import numpy as np

def sigma(factor_returns:list(float), j:int) -> float:
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
    if j >= 12:
        j2 = 120
    else:
        j2 = 36
    _sigma = np.var(factor_returns[:j2])
    sigma = _sigma**(j2/12.0)
	return sigma
```

### Analysis of Factor Timing
Benefits of factor timing can be assessed in terms of alpha by regressing the scaled factor on the raw factor.
$f^{TSFM}_{i,j,t} = \alpha_{i,j} + \Beta_{i,j}f_{i,t} + e_{i,j,t}$


### Full Strategy
The overall TSFM strategy combines all individual factor time-series momentum strategies into a single portfolio. TSFM aggregates timed factors (with formation window *j*) according to:

$TSFM_{jt}=TSFM_{jt}^{Long} - TSFM_{jt}^{Short}$

Where
$TSFM_{jt}^{Long} = 
	\frac
		{\Sigma_{i}1_{\{s_{i,j,t} > 0\}}f^{TSFM}_{i,j,t+1}}
		{\Sigma_{i}1_{\{s_{i,j,t }> 0\}}s_{i,j,t}}$

$TSFM_{jt}^{Short} = 
	\frac
		{\Sigma_{i}1_{\{s_{i,j,t} \le 0\}}f^{TSFM}_{i,j,t+1}}
		{\Sigma_{i}1_{\{s_{i,j,t} \le 0\}}s_{i,j,t}}$

That is, the long and short legs are rescaled to for unit leverage ($1 long and $1 short) TSFM portfolio
Translated into python

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE4ODc4NTc0ODBdfQ==
-->