import pandas as pd
from pandas import read_csv
from matplotlib import pyplot as plt
import numpy as np

def add_stock_max(location):
    # stock_data = read_csv('../data/data_cleaned/Stock.csv')
    
    # loc=stock_data["Location_Code"].unique()
    # weeks=stock_data["DAY_IN_YEAR"].unique()
    # loc_stock=np.zeros((len(loc),len(weeks)))
    
    # for l in range(len(loc)):
    #     looc=stock_data[stock_data["Location_Code"]==loc[l]]
    #     for w in range(len(weeks)):
    #         loc_stock[l,w]=sum(looc[looc["DAY_IN_YEAR"]==weeks[w]]["STOCK_QUANTITY_ON_HAND"])
    # st_max=[]
    # for l in range(len(loc)):
    #     st_max.append(max(loc_stock[l,:]))
    # new_df=pd.DataFrame({"Location_Code":stock_data["Location_Code"],"STOCK_MAX":st_max}, columns =  ["Location_Code","STOCK_MAX"])
    # return location + new_df
    return location


def clean_locations():
    print("Cleaning Location.csv...")
    locations = pd.read_csv('../data/data_raw/Location.csv')
    locations = locations.drop(columns="isWFJactive")
    locations = locations[locations["IsOpen"]=="Open"]
    locations = locations.drop(columns="IsOpen")
    locations = add_stock_max(locations)
    locations.to_csv("../data/data_cleaned/Location.csv", index=False, encoding='utf8')
    print("Done.")