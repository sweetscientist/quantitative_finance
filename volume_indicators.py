# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 18:56:14 2020

@author: Benjamin Lee
"""

import pandas as pd
import yfinance as yf
import datetime
import numpy as np
import matplotlib.pyplot as plt

import utils

from scipy import stats

# The following is a class that helps the user create technical indicators for analysis

class volume_indicators():
    
    def __init__(self, data):
        
        self.data = data
    
    def force_index(self):
        '''
        Force Index
        
        Indicates how strong the actual buying or selling pressure is.
        High = Rising Trend
        Low = Downward Trend
        
        ref: https://school.stockcharts.com/doku.php?id=technical_indicators:force_index
        
        '''
        fi = (self.data.Close - self.data.Close.shift(1)) * self.data.Volume
        return utils.ema(fi)
    
    def vwap(self, n):
        '''        
        Volume Weighted Average Price    
        
        Is the dollar value of all trading periods divided by total volume of current day
        The calculation starts/ends with the market
        It is usually used for intraday tading
        
        ref: https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday
        '''
        # Usual Price
        up = (self.data.High + self.data.Low + self.data.Close) / 3
        
        # Usual Volume Price
        vup = (up * self.data.Volume)
        
        # Total Volume Price
        total_vup = vup.rolling(n).sum()
        
        # Total Voume
        tv = self.data.Volume.rolling(n).sum()
        
        return total_vup / tv
                
    def obv(self):
        '''
        On Balance Volume
        
        Running total of positive and negative volume
        
        ref: https://school.stockcharts.com/doku.php?id=technical_indicators:on_balance_volume_obv
        '''
        obv = np.where(self.data.Close < self.data.Close.shift(1), -self.data.Volume, self.data.Volume)
        
        return  pd.Series(obv, index = self.data.index).cumsum()
    
    def adi(self):
        '''
        Accumulation Distribution Index
        
        Originally referred as Cumulative Money Flow Line
        
        Calculate money flow multiplier
        Multiply by volume
        Caculate running sum
        
        ref: https://school.stockcharts.com/doku.php?id=technical_indicators:accumulation_distribution_line
        '''
        
        clv = ((self.data.Close - self.data.Low) - (self.data.High - self.data.Close)) / (self.data.High - self.data.Low)
        clv = clv.fillna(0.0)
        ad = self.data.Volume * clv
        return ad.cumsum()
    
    def cmf(self, n):
        '''
        Chaikin Money Flow 

        Indicates sum of Money Flow Volume for a specific look-back period
        
        ref: https://school.stockcharts.com/doku.php?id=technical_indicators:chaikin_money_flow_cmf
        '''
        mfv = ((self.data.Close - self.data.Low) - (self.data.High - self.data.Close)) / (self.data.High - self.data.Low)
        mfv = mfv.fillna(0.0)
        mfv = mfv * self.data.Volume
        return mfv.rolling(n).sum() / self.data.Volume.rolling(n).sum()
    
    def eom(self):
        '''
        Ease of Movement
        
        Indicates an price change to the volume
        Particularly useful for assessing the trend
        
        ref: https://school.stockcharts.com/doku.php?id=technical_indicators:ease_of_movement_emv
        '''
        distance =  ((self.data.High + self.data.Low) / 2) - (self.data.High.diff(1) + self.data.Low.diff(1) / 2)
        boxratio = (self.data.Volume / 100000000) / (self.data.High - self.data.Low)
        return distance / boxratio
        
                                                              
        
    
        
if __name__ == "__main__":
    # Download Stock Data
    spy = yf.download('SPY', '1990-01-01')
    
    # Initial Indicator object
    ta = volume_indicators(spy)
    
    # Get Force Index
    fi = ta.force_index()
    # Get Volume Weighted Average Price
    vwap = ta.vwap(300) 
    # Get On Balance Volume
    obv = ta.obv()
    # Get adi
    adi = ta.adi()    
    # Get Chaikin Money Flow
    cmf = ta.cmf(300)
    # Get Ease of Movment
    eom = ta.eom()
    
    ind_data = pd.DataFrame({'spy': spy.Close,
                            'fi': fi, 
                            'vwap': vwap,
                            'obv': obv,
                            'cmf': cmf,
                            'eom': eom})
    plt.hist(spy.Close)
    plt.hist(ind_data.fi)
    plt.hist(ind_data.vwap) 
    plt.hist(obv)
    plt.hist(adi)
    plt.hist(cmf)
    plt.hist(eom)
    
    utils.normaltest(spy.Close, 0.05)
    utils.normaltest(fi, 0.05)
    utils.normaltest(vwap, 0.05)
    utils.normaltest(obv, 0.05)
    utils.normaltest(adi, 0.05)
    utils.normaltest(cmf, 0.05)
    utils.normaltest(eom, 0.05)
    