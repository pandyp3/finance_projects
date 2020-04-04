# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:11:38 2020

@author: Parth
"""

#We will be grabbing the s&P 500 tickers

import bs4 as bs
import datetime as dt
import os
#import pandas as pd
import pandas_datareader.data as web
import pickle #This module allows serializing python objects
import requests
#theres an issue with YahooDailyReader that requires a few additional modules
#import fix_yahoo_finance as yf

#yf.pdr_override

def save_sp500_tickers():
    #first thing we will do is grab the source code for the wiki page
    # with all of the tickers listed
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    #create an empty tickers list which will store as we iterate through
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    f = open("sp500tickers.pickle", "wb")
    pickle.dump(tickers, f)
    
    print(tickers)
    
    return tickers
    
#save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        f = open("sp500tickers.pickle", "rb")
        tickers = pickle.load(f)
    #create a directory if it doesnot already exist
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    #establish our dates
    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2018, 12, 31)

    for ticker in tickers[1:10]:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv.'.format(ticker)):
            #if the csv file does not exist, create it
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv.'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
            
#get_data_from_yahoo()

def clean_up_csv_files():
    folder = 'stock_dfs'
    for filename in os.listdir(folder):
        #create the path
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

#clean_up_csv_files()