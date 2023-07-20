# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 19:35:59 2020

@author: Benjamin Lee
"""

import math

import numpy as np
import pandas as pd

from scipy import stats


def sma(series, periods: int, fillna: bool = False):
    min_periods = 0 if fillna else periods
    return series.rolling(window=periods, min_periods=min_periods).mean()


def ema(series, periods = 3, fillna=False):
    min_periods = 0 if fillna else periods
    return series.ewm(span=periods, min_periods=min_periods, adjust=False).mean()    

def normaltest(x, alpha):
    k3, p = stats.normaltest(x)
       
    if p < alpha: # Null Hypothesis: X comes from a normal distribution
        print("Not Normal")
    else:
        print("Normal")