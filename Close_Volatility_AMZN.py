import numpy as np
import pandas as pd
from IPython import get_ipython

raw = pd.read_csv(r'C:\Users\ppandya\/tr_eikon_eod_data.csv', index_col=0, parse_dates=True)
amzn = pd.DataFrame(raw['AMZN.O'])
amzn.columns = ['Close']
#print(amzn.tail())

# Shift index by 1 period
# Calculate the series of logs of the closing price divided by the trailing price
amzn['Log_Ret'] = np.log(amzn['Close']/amzn['Close'].shift(1))

# Volatility is calculated as the rolling (252 observations) standard deviation of the log_ret observations
amzn['Volatility'] = amzn['Log_Ret'].rolling(window=252).std() * np.sqrt(252)

get_ipython().run_line_magic('matplotlib', 'inline')
amzn[['Close', 'Volatility']].plot(subplots=True, color='blue',
                                   figsize=(8, 6), grid=True);
