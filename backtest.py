# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:05:10 2019

@author: yifan.gong
"""
import sys
sys.path.append("C:\\Users\yifan.gong\Documents\PythonWorkspace\privatelibs")
sys.path.append("C:\\Users\yifan.gong\Documents\PythonWorkspace")

from set_col import set_col
from dictfile import save_obj,load_obj   
import pandas as pd
import numpy as np
path_day = 'C:\\Users\yifan.gong\Documents\PythonWorkspace\data\\'

signal_final = pd.read_csv('signal_final.csv',index_col = 0).T
set_col(signal_final)
signal_final = signal_final.iloc[0]

close000300 = pd.read_csv(path_day+'000300.SH_close.csv',index_col = 0).T
pre_close000300 = pd.read_csv(path_day+'000300.SH_pre_close.csv',index_col = 0).T
set_col(close000300)
set_col(pre_close000300)
close000300 = close000300.iloc[0]
pre_close000300 = pre_close000300.iloc[0]

#%%
from matplotlib import pyplot as plt
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
datelist = close000300.index
ax1.plot(datelist,close000300.values)

xt = np.arange(0,int(len(datelist)/10)*10,int(len(datelist)/100)*8+3)
xtick = [datelist[x] for x in xt]
ax1.set_xticks(xtick)
plt.xticks(rotation = 45)

#%%
'''backtest'''
cash = 10000000
stock_vol = 0
signal_pre = signal_final.shift()
asset = {}
flag = 0
for date0 in signal_final.index:
    if flag == 1:
        if signal_pre[date0] == 1:
            stock_vol = cash//close000300[date0]
            cash = cash - close000300[date0]*stock_vol
        elif signal_pre[date0] == -1:
            cash = cash + close000300[date0]*stock_vol
            stock_vol = 0
    asset[date0] = cash + stock_vol*close000300[date0]
    if signal_final[date0] == signal_pre[date0]:
        flag = 0
    else:
        flag = 1

datelist = list(asset.keys())

plt_asset = [v/(list(asset.values())[0]) for v in list(asset.values())]
plt_300 = [v/(list(close000300[datelist])[0]) for v in list(close000300[datelist])]
fig2 = plt.figure(figsize = (16,9),dpi = 200)
ax2 = fig2.add_subplot(111)
plt.xticks(rotation = 45)
ax2.plot(datelist,plt_asset,'r')
ax2.plot(datelist,plt_300)
#ax1 = ax2.twinx()
#ax1.plot(datelist,plt_300)

xt = np.arange(0,int(len(datelist)/10)*10,int(len(datelist)/100)*8+3)
xtick = [datelist[x] for x in xt]
ax2.set_xticks(xtick)
fig2.savefig('pnl.png')


#%%
'''test'''
tmp = pd.Series(asset) 
tmp1 = tmp.shift()
tmp2 = 100*(tmp-tmp1)/tmp1

tmp300 = 100*(close000300-pre_close000300)/pre_close000300
fig3 = plt.figure(figsize = (16,9),dpi = 200)
ax1 = fig3.add_subplot(111)
plt.xticks(rotation = 45)
ax1.scatter(datelist,tmp2.values,c = 'r', s=3)
ax1.scatter(datelist,tmp300[datelist].values, c='b', s=1)

xt = np.arange(0,int(len(datelist)/10)*10,int(len(datelist)/100)*8+3)
xtick = [datelist[x] for x in xt]
ax1.set_xticks(xtick)
fig3.savefig('pct_chg.png')
