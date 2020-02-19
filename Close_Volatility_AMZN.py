# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 08:36:44 2020

@author: ppandya
"""

import numpy as np
import pandas as pd
from IPython import get_ipython

raw = pd.read_csv(r'C:\Users\ppandya\/tr_eikon_eod_data.csv', index_col=0, parse_dates=True)
amzn = pd.DataFrame(raw['AMZN.O'])
amzn.columns = ['Close']
#print(amzn.tail())

# 
amzn['Log_Ret'] = np.log(amzn['Close']/amzn['Close'].shift(1))
amzn['Volatility'] = amzn['Log_Ret'].rolling(window=252).std() * np.sqrt(252)

get_ipython().run_line_magic('matplotlib', 'inline')
amzn[['Close', 'Volatility']].plot(subplots=True, color='blue',
                                   figsize=(8, 6), grid=True);