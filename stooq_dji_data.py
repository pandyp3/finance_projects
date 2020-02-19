# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 08:36:44 2020

@author: ppandya
"""

import numpy as np
import pandas as pd
#from pandas_datareader import data, wb
'''
IMPORTANT - the pandas_datareader module has to be downloaded, and given that paths are all relative to the .py file,
the file should be saved in the site-packages folder since that is where the libraries exist. So...
AppData\Local\Programs\Python\Python38\Lib\site-packages
'''

import pandas_datareader.data as web

f = web.DataReader('^DJI', 'stooq')

print(f[:10])