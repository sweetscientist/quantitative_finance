# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 22:16:48 2020

@author: Benjamin Lee
"""

import pandas as pd
import yfinance as yf
import datetime
import numpy as np
import matplotlib.pyplot as plt

import utils

from scipy import stats

class volatility_indicators:
        
    def __init__(self, data):
        
        self.data = data
    
    # Bollinger Ban
    def bb(self):
        '''
        Bollinger Bands
        
        Volatility bands placed above and below a moving average based on standard deviations
        Volatility UP: Wider
        Volatility DOWN: Contract
        
        ref: https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_bands        
        '''
        
        
    
    def dc(self):
        '''
        Donchian Channel

        
        '''

    def ui(self):
        '''
        Ulcer Index
        '''
        
    def kc(self):
        '''
        Keltner Channel
        '''
        
    def atr(self):
        '''
        Average True Range
        
        
        
        ref: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr
        '''
        
if __name__ == "__main__":
    # Download Stock Data
    spy = yf.download('SPY', '1990-01-01')
    
    vi = volatility_indicators(spy)
