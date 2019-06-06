# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:27:21 2019

@author: yifan.gong
"""

import sys
sys.path.append("C:\\Users\yifan.gong\Documents\PythonWorkspace\privatelibs")
sys.path.append("C:\\Users\yifan.gong\Documents\PythonWorkspace")

from set_col import set_col
from dictfile import save_obj,load_obj   
path_day = 'C:\\Users\yifan.gong\Documents\PythonWorkspace\data\\'
#%%
import pandas as pd

Open = pd.read_csv(path_day+'open.csv',index_col = 0).T
close = pd.read_csv(path_day+'close.csv',index_col = 0).T
pre_close = pd.read_csv(path_day+'pre_close.csv',index_col = 0).T
adjfactor = pd.read_csv(path_day+'adjfactor.csv',index_col = 0).T
maxupordown = pd.read_csv(path_day+'maxupordown.csv',index_col = 0).T
suspend = pd.read_csv(path_day+'suspend.csv',index_col = 0).T
timedelta_ipo = pd.read_csv(path_day+'timedelta_ipo.csv',index_col = 0).T
mkt_cap_float  = pd.read_csv(path_day+'mkt_cap_float.csv',index_col = 0).T
delist = pd.read_csv(path_day+'delist.csv',index_col = 0).T
pct_chg = pd.read_csv(path_day+'pct_chg.csv',index_col = 0).T
sw1_industry = pd.read_csv(path_day+'sw1_industry.csv',index_col = 0).T
volumn = pd.read_csv(path_day+'volumn.csv',index_col = 0).T
set_col(volumn)
set_col(sw1_industry)
set_col(pct_chg)
set_col(delist)
set_col(mkt_cap_float)
set_col(Open)
set_col(close)
set_col(pre_close)
set_col(adjfactor)
set_col(maxupordown)
set_col(suspend)
set_col(timedelta_ipo)
#%%
industry_close = pd.DataFrame(index = range(1,29),columns = sw1_industry.columns)

for date0 in industry_close.columns:
    for i in industry_close.index:
        tmp = sw1_industry.loc[:,date0]
        ind = tmp[tmp == i].index
        ind_close = (close.loc[ind,date0]*adjfactor.loc[ind,date0]*mkt_cap_float.loc[ind,date0]).sum()/mkt_cap_float.loc[ind,date0].sum()
        industry_close.loc[i,date0] = ind_close
        print((i,date0))
        
industry_volumn = pd.DataFrame(index = range(1,29),columns = sw1_industry.columns)
for date0 in industry_volumn.columns:
    for i in industry_volumn.index:
        tmp = sw1_industry.loc[:,date0]
        ind = tmp[tmp == i].index
        ind_volumn = volumn.loc[ind,date0].sum()
        industry_volumn.loc[i,date0] = ind_volumn
        print((i,date0))

industry_close.to_csv('C:\\Users\yifan.gong\\Documents\PythonWorkspace\industry_ro\industry_close.csv')
industry_volumn.to_csv('C:\\Users\yifan.gong\\Documents\PythonWorkspace\industry_ro\industry_volumn.csv')
