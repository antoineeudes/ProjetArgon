import pandas as pd
import numpy as np
from datetime import date, timedelta
from get_y import *
import category_encoders as ce
from itertools import islice
import multiprocessing
from multiprocessing import Manager
import os, sys
import pickle


input_path = '../../../data/data_cleaned/'
output_path = '../../../data/data_cleaned/input/'
try:
    os.mkdir(output_path)
except:
    pass


# Columns names
location_key = 'Location_Code'
item_key = 'Item_Code'
date_key = 'Day_in_year_YYYYMMDD'
period_key = 'Period_number'
year_key = 'Year'

period_length = 60 # Length of the period in days

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

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

datetime_to_range_year_vect = np.vectorize(datetime_to_range_year)

def print_percent(index, total, prefix='', rate=10000):
    if index % (total//rate) == 0:
        print(prefix+str(round(100*index/total, 1))+'%')

def df_pool_computing(function, df, **kwargs):
    '''
        Call the given function on the dataframe df using multiprocessing.
        The dataframe is partitioned and the function is called on each partition.
        Each call is executed on a different process allowing multiprocessing.

        function is given two arguments: a part of the dataframe and the number of the process
        Must return a df.
        function(sub_df, i) -> df

        Return the modified dataframe df.
    '''
    # Create Pool for multiprocessing
    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())

    # Make as many partition of the dataframe as cpu units
    nb_partition = multiprocessing.cpu_count()
    partition_width = df.shape[0]//nb_partition

    # Build the arguments to be passed to add_Y when mapping
    args = []
    for i in range(nb_partition):
        args.append((df.iloc[partition_width*i:partition_width*(i+1), :], i, kwargs))

    # Mapping args to add_Y, each on a different process
    results = pool.starmap(function, args)

    del args

    # Closing Pool
    pool.close()
    pool.join()

    # Getting the results together
    return pd.concat(results)

def add_Y_pool(df, i, kwargs):
    '''
        Compute and add the Y
    '''

    print('Starting process {}'.format(i))
    k = 0
    for index, row in df.iterrows():
        df.at[index, 'Y'] = get_y(row[item_key], row[location_key], row[period_key], row[year_key], period_length)
        print_percent(k, df.shape[0], prefix='Compute Y ({}) : '.format(i))
        k += 1

    return df

def add_Y_pool_fast(df, i=None, kwarg={'y_dict': dict()}):
    '''
        Compute and add the Y
    '''

    print('Starting process {}'.format(i))
    k = 0
    y_dict = kwarg['y_dict']
    for index, row in df.iterrows():
        try:
            df.at[index, 'Y'] = y_dict[(row[location_key], row[item_key], row[period_key], row[year_key])]#get_y(row[item_key], row[location_key], row[period_key], row[year_key], period_length)
        except:
            df.at[index, 'Y'] = 0
        print_percent(k, df.shape[0], prefix='Compute Y ({}) : '.format(i))
        k += 1

    return df

def reshape_date_pool(df, i, kwargs):
    '''
        Compute the Period_number and Year columns.
    '''

    print('Starting process {}'.format(i))
    k = 0
    for index, row in df.iterrows():
        datetime = date.fromisoformat(row[date_key])
        period_number, year = datetime_to_range_year(datetime, period_length)
        df.at[index, period_key] = period_number
        df.at[index, year_key] = year
        print_percent(k, df.shape[0], prefix='Reshape date ({}) : '.format(i))
        k += 1

    return df

def select_columns_of_interest(df):
    '''
        Select only interesting columns
    '''
    return df[[location_key, item_key, date_key]]

def reshape_date(df):
    '''
        Compute and add the Period_number and Year columns.
    '''
    df[period_key], df[year_key] = 0, 0 # Add extra columns for new date format
    df = df_pool_computing(reshape_date_pool, df)
    # Drop the duplicates which could have appeared when turning date to period
    df.drop_duplicates(subset=[location_key, item_key, period_key, year_key], inplace=True)
    return df

def add_Y(df):
    '''
        Compute and add the Y column.
    '''
    Count = get_y_dict_fast(period_length)
    # print(Count)
    return df_pool_computing(add_Y_pool_fast, df, y_dict=Count)

def encode_categorical_features(df, encoder=None):
    '''
        Encode the categorical features using BinaryEncoder.
    '''
    if encoder == None:
        encoder = ce.BinaryEncoder(cols=[location_key, item_key])
        encoder.fit(df)
    return encoder.transform(df), encoder

def drop_residual_columns(df):
    '''
        Remove the old date column.
    '''
    df.drop([date_key], axis=1, inplace=True)
    return df

def add_unsold_rows(df):
    min_date = date.fromisoformat('2016-01-01')
    max_date = date.fromisoformat('2019-01-01')

    nb_period = 365//period_length

    print('\nAdding unsold rows from {} to {}'.format(min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')))

    print('\tReading Location.csv')
    Locations = pd.read_csv(input_path+'Location_MarketData.csv')

    print('\tReading Articles.csv')
    Articles = pd.read_csv(input_path+'Articles.csv')
    Sales_Articles_Location_MarketData = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')
    Sales_Articles_Location_MarketData.drop_duplicates(subset=[item_key], inplace=True)

    Seen = dict()
    Datetime = []
    for datetime in daterange(min_date, max_date):
        period, year = datetime_to_range_year(datetime, period_length)
        if not (period, year) in Seen:
            Seen[(period, year)] = True
            Datetime.append(datetime.strftime('%Y-%m-%d'))

    print('\tMeshgrid with Locations, Articles, Dates')
    Loc, Art, D = np.meshgrid(Locations[location_key], Sales_Articles_Location_MarketData[item_key], Datetime, indexing='ij')

    del Locations
    del Sales_Articles_Location_MarketData
    del Datetime

    print('\tFlatten Locations')
    Loc_flat = Loc.flatten()
    print('\tFlatten Articles')
    Art_flat = Art.flatten()
    print('\tFlatten Dates')
    D_flat = D.flatten()

    del Loc
    del Art
    del D

    nb_rows = len(Loc_flat)
    print('\tBuild Y')
    Y_flat = np.zeros(nb_rows)

    print('\tBuild Period_flat and Year_flat')
    fromisoformat_vect = np.vectorize(date.fromisoformat)
    Period_flat, Year_flat = datetime_to_range_year_vect(fromisoformat_vect(D_flat), period_length)

    print('\tBuilding data array with {} rows'.format(nb_rows))
    data = np.array([Loc_flat, Art_flat, D_flat, Period_flat, Year_flat, Y_flat]).T

    del Loc_flat
    del Art_flat
    del D_flat
    del Period_flat
    del Year_flat
    del Y_flat

    print('\tBuilding dataframe from data array')
    extra_df = pd.DataFrame(data, columns=[location_key, item_key, date_key, period_key, year_key, 'Y'])

    del data

    print('\tConcat the two dataframes')
    df = pd.concat([df, extra_df], ignore_index=True, sort=False)

    del extra_df

    print('\tDrop duplicates')
    df.drop_duplicates(subset=[location_key, item_key, period_key, year_key], inplace=True)

    return df

def add_unsold_rows2(df):
    '''
        Add unsold rows considering only couples (Location, Article) present in the Stock_MarketData.csv
        i.e articles having been sold at least once in this location
        (To avoid adding fake info on articles which can't be sold in a location)
    '''
    min_date = date.fromisoformat('2016-01-01')
    max_date = date.fromisoformat('2019-01-01')

    nb_period = 365//period_length

    print('\nAdding unsold rows from {} to {}'.format(min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')))

    print('\tReading Stock_MarketData')
    Stock_MarketData = pd.read_csv(input_path+'Stock_MarketData.csv')

    Locations = Stock_MarketData[location_key]
    Articles = Stock_MarketData[item_key]

    Seen = dict()
    Datetime = []
    for datetime in daterange(min_date, max_date):
        period, year = datetime_to_range_year(datetime, period_length)
        if not (period, year) in Seen:
            Seen[(period, year)] = True
            Datetime.append(datetime.strftime('%Y-%m-%d'))

    print('\tMeshgrid with Locations, Articles, Dates')
    Loc, D = np.meshgrid(Locations, Datetime, indexing='ij')
    Art, D = np.meshgrid(Articles, Datetime, indexing='ij')

    print('\tFlatten Locations')
    Loc_flat = Loc.flatten()
    print('\tFlatten Articles')
    Art_flat = Art.flatten()
    print('\tFlatten Dates')
    D_flat = D.flatten()

    nb_rows = len(Loc_flat)
    print('\tBuild Y')
    Y_flat = np.zeros(nb_rows)

    print('\tBuild Period_flat and Year_flat')
    fromisoformat_vect = np.vectorize(date.fromisoformat)
    Period_flat, Year_flat = datetime_to_range_year_vect(fromisoformat_vect(D_flat), period_length)

    print('\tBuilding data array with {} rows'.format(nb_rows))
    data = np.array([Loc_flat, Art_flat, D_flat, Period_flat, Year_flat, Y_flat]).T

    del Loc_flat
    del Art_flat
    del D_flat
    del Period_flat
    del Year_flat
    del Y_flat

    print('\tBuilding dataframe from data array')
    extra_df = pd.DataFrame(data, columns=[location_key, item_key, date_key, period_key, year_key, 'Y'])

    del data

    print('\tConcat the two dataframes')
    df = pd.concat([df, extra_df], ignore_index=True, sort=False)

    del extra_df

    print('\tDrop duplicates')
    df.drop_duplicates(subset=[location_key, item_key, period_key, year_key], inplace=True)

    return df

def compute_XY(save = False, dirname='XY.csv'):
    '''
        Read the Sales_Articles_Location_MarketData.csv file.
        Build the BinaryEncoded dataframe containing both the X and the Y.
    '''

    print('\nReading Sales_Articles_Location_MarketData.csv')
    df = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')

    df = select_columns_of_interest(df) # Keep only interesting columns
    df = reshape_date(df)
    df.drop_duplicates(subset=[location_key, item_key, period_key, year_key], inplace=True)
    df = add_Y(df)
    df = add_unsold_rows2(df)
    df = drop_residual_columns(df)
    df, encoder = encode_categorical_features(df)

    if save:
        print('\nSaving')
        try:
            os.mkdir(output_path+dirname)
        except:
            pass
        print('\tDataframe')
        df.to_csv(output_path+dirname+'/XY.csv',index=False)
        print('\tEncoder')
        pickle.dump(encoder, open(output_path+dirname+'/encoder.sav', 'wb'))

    print(df)
    return df

def describeY(filename='XY.csv'):
    dataframe = pd.read_csv(output_path+'XY_stockbased_'+str(period_length)+'/'+filename)
    Y = dataframe["Y"]
    print(Y.describe())

if __name__ == '__main__':
    compute_XY(save=True, dirname='XY_stockbased_{}'.format(period_length))
