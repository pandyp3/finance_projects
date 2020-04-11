import bs4 as bs
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import pickle
import requests
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
# import fix_yahoo_finance as yf
from collections import Counter
from sklearn import svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

# yf.pdr_override

style.use('ggplot')

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('.', '-')
        ticker = ticker[:-1]
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers



def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2019, 6, 8)
    end = dt.datetime.now()
    for ticker in tickers[1:10]:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = pdr.get_data_yahoo(ticker, start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


#save_sp500_tickers()
#get_data_from_yahoo()

def clean_up_csv_files():
    folder = 'stock_dfs'
    for filename in os.listdir(folder):
        #create the path
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

# clean_up_csv_files()
            
#here, we will combine the Adj Close of all tickers into a single file
def compile_data():
    #let's open up the binary of the tickers list we've saved
    f = open("sp500tickers.pickle", "rb")
    tickers = pickle.load(f)
    
    #create an empty dataframe object    
    main_df = pd.DataFrame()
    
    for count, ticker in enumerate(tickers[1:10]):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        #set the index
        df.set_index('Date', inplace=True)
        
        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Volume', 'Close'], 1, inplace=True)
        
        #running this if condition because you can't join to an empty dataframe
        if main_df.empty:
            main_df=df
        else:
            main_df = main_df.join(df, how='outer')

    print(main_df.head())
    main_df.to_csv('sp550_combined_close.csv')
    
#compile_data()

def visualize_data():
    df = pd.read_csv('sp550_combined_close.csv')
    # df['AMD'].plot()
    # plt.show()
    df_corr = df.corr()
    
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()
   
    
#visualize_data()

def process_data_for_labels(ticker):
    #labels are the classification
    #We also need to define our time period
    hm_days = 7
    df = pd.read_csv('sp550_combined_close.csv', index_col=0)
    tickers = df.columns.values.tolist()
#    print(tickers)
    df.fillna(0, inplace=True)
    
    for i in range(1, hm_days+1):
        #normalize the data. This calculates the percentage % in price per ticker 
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    
    df.fillna(0, inplace=True)    
    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02 #our signal is when price changes (in either direction) by more than 2%
    for col in cols:
        if col > requirement:
            return 1
        elif col < -requirement:
            return -1
        else:
            return 0
        
def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)
    #creates a new column ticker_target that contains either 1, -1, or 0
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, df['{}_1d'.format(ticker)], df['{}_2d'.format(ticker)], df['{}_3d'.format(ticker)], df['{}_4d'.format(ticker)], df['{}_5d'.format(ticker)], df['{}_6d'.format(ticker)], df['{}_7d'.format(ticker)]))
    
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_values = [str(i) for i in vals]
    print('Data spread:', Counter(str_values))
                                              
    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)
    
    X = df_vals.values
    Y = df['{}_target'.format(ticker)].values

    return X, Y, df

def do_ml(ticker):
    X, Y, df = extract_featuresets(ticker)
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5)
    
    #clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])
    
    clf.fit(X_train, Y_train)
    confidence = clf.score(X_test, Y_test)
    
    print('Accuracy', confidence)
    
    predictions = clf.predict(X_test)
    print('Predicted spread:', Counter(predictions))
    
    return confidence

do_ml('AAP')

        
        
        
        
    
