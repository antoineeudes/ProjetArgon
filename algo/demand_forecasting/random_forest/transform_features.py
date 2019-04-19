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

def add_Y(df, i=None):
    '''
        Compute and add the Y, Period_number and Year columns.
    '''

    print('Starting process {}'.format(i))
    k = 0
    for index, row in df.iterrows():
        datetime = date.fromisoformat(row[date_key])
        period_number, year = datetime_to_range_year(datetime, period_length)
        df.at[index, period_key] = period_number
        df.at[index, year_key] = year
        df.at[index, 'Y'] = get_y(row[item_key], row[location_key], row[date_key])
        if k % (df.shape[0]//10000) == 0:
            print(str(i)+' : '+str(round(100*k/df.shape[0], 1))+'%')
        k += 1

    return df

def compute_XY(save = False, filename='XY.csv'):
    '''
        Read the Sales_Articles_Location_MarketData.csv file and build the one hot encoding
        vector (Location, Article, Day of the year, Year)
    '''

    print('\nReading Sales_Articles_Location_MarketData.csv')
    df = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')

    # Keep only interesting columns
    df = df[[location_key, item_key, date_key]]

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Add extra columns for new date format
    df[period_key] = 0
    df[year_key] = 0

    # Computing the Y
    # Create Pool for multiprocessing
    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count()-1)

    # Make as many partition of the dataframe as cpu units
    nb_partition = multiprocessing.cpu_count()-1
    partition_width = df.shape[0]//nb_partition

    # Build the arguments to be passed to add_Y when mapping
    args = []
    for i in range(nb_partition):
        args.append((df.iloc[partition_width*i:partition_width*(i+1), :], i))

    # Mapping args to add_Y, each on a different process
    results = pool.starmap(add_Y, args)

    # Getting the results together
    df = pd.concat(results)

    # Closing Pool
    pool.close()
    pool.join()

    # Drop old date column
    df.drop([date_key], axis=1, inplace=True)

    # Encode the categorical features
    encoder = ce.BinaryEncoder(cols=[location_key, item_key])
    df = encoder.fit_transform(df)

    print(df)
    if save:
        df.to_csv(output_path+filename,index=False)

    return df

if __name__ == '__main__':
    compute_XY(save=False, filename='RandomForest_XY.csv')
