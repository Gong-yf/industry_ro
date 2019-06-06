# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:58:32 2019

@author: yifan.gong
"""

import sys
sys.path.append("C:\\Users\yifan.gong\Documents\PythonWorkspace\privatelibs")
sys.path.append("C:\\Users\yifan.gong\Documents\PythonWorkspace")

from set_col import set_col
from dictfile import save_obj,load_obj   
path_day = 'C:\\Users\yifan.gong\Documents\PythonWorkspace\data\\'
import pandas as pd
import numpy as np
#%%
fast_window = 20
slow_window = 240
'''signal by price and volumn'''
industry_close = pd.read_csv('industry_close.csv',index_col = 0)
industry_volumn = pd.read_csv('industry_volumn.csv',index_col = 0)

'''price'''
price_w = industry_close.rolling(window = fast_window,axis = 1).mean()
price_m = industry_close.rolling(window = fast_window,axis = 1).mean().shift(slow_window,axis=1)
price_tmp = (price_w - price_m)/price_m
price_signal = np.sign(price_tmp - price_tmp.shift(fast_window,axis = 1))

'''volumn'''
volumn_w = industry_volumn.rolling(window = slow_window,axis = 1).sum()
volumn_m = industry_volumn.shift(slow_window,axis=1).rolling(window = slow_window,axis = 1).sum()
volumn_tmp = (volumn_w - volumn_m)/volumn_m
volumn_signal = np.sign(volumn_tmp - volumn_tmp.shift(fast_window,axis = 1))

signal = (price_signal + volumn_signal)/2
signal_long = signal[signal==1].count()
signal_short = signal[signal==-1].count()
signal_none = signal[signal==0].count()

signal_1 = pd.Series(index = signal_long.index)
for ind in signal_1.index:
    if signal_long[ind]>5 and signal_short[ind]<5:
        signal_1[ind] = 1
    elif signal_long[ind]<5 and signal_short[ind]>5:
        signal_1[ind] = -1
    else:
        signal_1[ind] = 0

#%%
'''signal by ma'''
fast_window = 20
slow_window = 120
ma_fast = industry_close.rolling(window = fast_window,axis = 1).mean()
ma_slow = industry_close.rolling(window = slow_window,axis = 1).mean()
ma_signal = np.sign(ma_fast - ma_slow)

signal_long = ma_signal[ma_signal==1].count()
signal_short = ma_signal[ma_signal==-1].count()
signal_none = ma_signal[ma_signal==0].count()

signal_2 = pd.Series(index = signal_long.index)
for ind in signal_2.index:
    if signal_long[ind]>5 and signal_short[ind]<5:
        signal_2[ind] = 1
    elif signal_long[ind]<5 and signal_short[ind]>5:
        signal_2[ind] = -1
    else:
        signal_2[ind] = 0
        
'''signal final'''
signal_final = signal_1+signal_2
signal_final = signal_final.apply(lambda x: np.sign(x))
signal_final = signal_final.replace(0,-1)

signal.to_csv('C:\\Users\yifan.gong\\Documents\PythonWorkspace\industry_ro\signal_pv.csv')
ma_signal.to_csv('C:\\Users\yifan.gong\\Documents\PythonWorkspace\industry_ro\signal_ma.csv')
signal_final.to_csv('C:\\Users\yifan.gong\\Documents\PythonWorkspace\industry_ro\signal_final.csv')