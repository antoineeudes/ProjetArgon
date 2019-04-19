import pandas as pd
import numpy as np
from datetime import date
from get_y import *
import category_encoders as ce
from itertools import islice
import multiprocessing
from multiprocessing import Manager



# pd.set_option('display.max_columns', 500)

input_path = '../../../data/data_cleaned/'
output_path = '../../../data/data_cleaned/'

# Columns names
location_key = 'Location_Code'
item_key = 'Item_Code'
date_key = 'Day_in_year_YYYYMMDD'
period_key = 'Period_number'
year_key = 'Year'

period_length = 1 # Length of the period in days


def datetime_to_day_year(datetime):
    '''Given a datetime object, return the day of the year (from 0 to 365) and the year'''
    year = datetime.year
    d0 = date(year, 1, 1)
    day_index = (datetime-d0).days

    return day_index, year

def datetime_to_range_year(datetime, period_length):
    '''Given a datetime object, return the period of the year (from 0 to 365//period_length) and the year'''
    day_index, year = datetime_to_day_year(datetime)

    return day_index//period_length, year

def compute(df, i=None):
    print('Starting process {}'.format(i))
    k = 0
    for index, row in df.iterrows():
        datetime = date.fromisoformat(row[date_key])
        period_number, year = datetime_to_range_year(datetime, period_length)
        df.at[index, period_key] = period_number
        df.at[index, year_key] = year
        df.at[index, 'Y'] = get_y(row[item_key], row[location_key], row[date_key])
        if k % (df.shape[0]//1000) == 0:
            print(str(i)+' : '+str(round(100*k/df.shape[0], 1))+'%')
        k += 1

    return df

def compute_X(save = False):
    '''
        Read the Sales_Articles_Location_MarketData.csv file and build the one hot encoding
        vector (Location, Article, Day of the year, Year)
    '''

    print('\nReading Sales_Articles_Location_MarketData.csv')
    df = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')
    df = df[[location_key, item_key, date_key]]
    df.drop_duplicates(inplace=True)
    df[period_key] = 0
    df[year_key] = 0

    p = multiprocessing.Pool(processes = multiprocessing.cpu_count()-1)

    nb_rows = df.shape[0]
    nb_partition = multiprocessing.cpu_count()-1
    partition_width = nb_rows//nb_partition

    args = []
    for i in range(nb_partition):
        args.append((df.iloc[partition_width*i:partition_width*(i+1), :], i))

    results = p.starmap(compute, args)
    df = pd.concat(results)

    p.close()
    p.join()

    df.drop([date_key], axis=1, inplace=True)

    encoder = ce.BinaryEncoder(cols=[location_key, item_key])
    df = encoder.fit_transform(df)

    print(df)
    if save:
        df.to_csv(output_path+'RandomForest_X.csv',index=False)

    return df

if __name__ == '__main__':
    compute_X(save=True)
