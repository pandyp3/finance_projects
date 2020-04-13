# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 14:57:30 2020

@author: Parth



create a bar graph to chart the most frequented "To" and "From" bike station locations (by intersection, not id)
create a heatmap

"""

import os, glob
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import re

#create a method that does the following
def combine_biking_data():
    #set active dir
    dr_2017 = "C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/bikeshare-ridership-2017/2017 Data/"
    comb_2017 = glob.glob(os.path.join(dr_2017, "Bikeshare Ridership (2017 Q*).csv"))
    
    # print(comb_2017)
    
    
    dr_2018 = "C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/bikeshare2018/bikeshare2018/"
    comb_2018 = glob.glob(os.path.join(dr_2018, "Bike Share Toronto Ridership_Q* 2018.csv"))
    
    all_df = []
    for f in comb_2017:
        df = pd.read_csv(f, sep=',')
        end_path = f.split('/')[-1]
        df['fileName'] = end_path.split('\\')[-1]
        all_df.append(df)
    
    for f in comb_2018:
        df = pd.read_csv(f, sep=',')
        end_path = f.split('/')[-1]
        df['fileName'] = end_path.split('\\')[-1]
        all_df.append(df)
    merged_df = pd.concat(all_df, ignore_index=True, sort=True)
    # if not os.path.exists(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data.csv"):
    #     merged_df.to_csv(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data.csv")
    # else:
    #     print('Already exists')
        
        #the csv and df of the combined data is too large to work with
        #create csv files for 2017 and 2018 and work with those
        #create graphs for each year
        
    df_2017 = []
    for f in comb_2017:
        df = pd.read_csv(f, sep=',')
        end_path = f.split('/')[-1]
        df['fileName'] = end_path.split('\\')[-1]
        df_2017.append(df)
    merged_df_2017 = pd.concat(df_2017, ignore_index=True, sort=True)
    # if not os.path.exists(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2017.csv"):
    #     merged_df_2017.to_csv(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2017.csv")
    # else:
    #     print('Already exists')
        
    df_2018 = []
    for f in comb_2018:
        df = pd.read_csv(f, sep=',')
        end_path = f.split('/')[-1]
        df['fileName'] = end_path.split('\\')[-1]
        df_2018.append(df)
    merged_df_2018 = pd.concat(df_2018, ignore_index=True, sort=True)
    # if not os.path.exists(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2018.csv"):
    #     merged_df_2018.to_csv(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2018.csv")
    # else:
    #     print('Already exists')
        
    return merged_df_2017, merged_df_2018
    
    
# combine_biking_data()

def graphing_to_from():
    # df = pd.read_csv("C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data.csv")
    # we shouldn't need to create the dataframe again so I commented out the above
    merged_df_2017, merged_df_2018 = combine_biking_data()
    
    # let's see how the number of Members and Casuals have grown in 2017
    # first thing I want to do is add a new column for Year + Quarter
    # I don't really know how to use regex to find both so I'll create separate columns for Year and Quarter
    
    merged_df_2017['fileName'] = [re.compile(r'\d\d\d\d\sQ\d').findall(str(x)) for x in merged_df_2017['fileName']]
    merged_df_2017['Quarter'] = [','.join(map(str, l)) for l in merged_df_2017['fileName']]
    del merged_df_2017['fileName']
    
    # if not os.path.exists(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2017_full.csv"):
    #     merged_df_2017.to_csv(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2017_full.csv")
    # else:
    #     print('Already exists')
        
    # merged_df_2018['Quarter'] = [re.compile(r'Q\d\s\d\d\d\d').findall(str(x)) for x in merged_df_2018['fileName']]
    # del merged_df_2018['fileName']
    
    # if not os.path.exists(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2018_full.csv"):
    #     merged_df_2018.to_csv(r"C:/Users/Parth/Documents/Data Files/toronto-bikeshare-data/total_bikeshare_data_2018_full.csv")
    # else:
    #     print('Already exists')

    df_Member = []
    for index, row in merged_df_2017.iterrows():
        if row['user_type'] = 'Member'
        merged_df_2017.append(df_Member)
        
    
    label_2017 = list(set(merged_df_2017['Quarter']))
    
    merged_df_2017['user_type'].value_counts().plot(kind='barh', subplots=True)
   
        
    
    

 

graphing_to_from()
    
    
    
    
    