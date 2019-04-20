import pandas as pd
import numpy as np
from datetime import date, timedelta
from get_y import *
import category_encoders as ce
from itertools import islice
import multiprocessing
from multiprocessing import Manager


input_path = '../../../data/data_cleaned/'
output_path = '../../../data/data_cleaned/'

# Columns names
location_key = 'Location_Code'
item_key = 'Item_Code'
date_key = 'Day_in_year_YYYYMMDD'
period_key = 'Period_number'
year_key = 'Year'

period_length = 7 # Length of the period in days

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

def df_pool_computing(function, df):
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
    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count()-1)

    # Make as many partition of the dataframe as cpu units
    nb_partition = multiprocessing.cpu_count()-1
    partition_width = df.shape[0]//nb_partition

    # Build the arguments to be passed to add_Y when mapping
    args = []
    for i in range(nb_partition):
        args.append((df.iloc[partition_width*i:partition_width*(i+1), :], i))

    # Mapping args to add_Y, each on a different process
    results = pool.starmap(function, args)

    # Closing Pool
    pool.close()
    pool.join()

    # Getting the results together
    return pd.concat(results)

def add_Y_pool(df, i=None):
    '''
        Compute and add the Y
    '''

    print('Starting process {}'.format(i))
    k = 0
    for index, row in df.iterrows():
        df.at[index, 'Y'] = get_y(row[item_key], row[location_key], row[date_key])
        print_percent(k, df.shape[0], prefix='Compute Y ({}) : '.format(i))
        k += 1

    return df

def reshape_date_pool(df, i=None):
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
    return df_pool_computing(add_Y_pool, df)

def encode_categorical_features(df):
    '''
        Encode the categorical features using BinaryEncoder.
    '''
    encoder = ce.BinaryEncoder(cols=[location_key, item_key])
    return encoder.fit_transform(df)

def drop_residual_columns(df):
    '''
        Remove the old date column.
    '''
    df.drop([date_key], axis=1, inplace=True)
    return df

def add_unsold_rows(df):
    min_date = date.fromisoformat('2016-01-01')#(0, 2016)
    max_date = date.fromisoformat('2019-01-01')#(0, 2019)

    # min_period, min_year = datetime_to_range_year(date.fromisoformat(min_date), period_length)
    # max_period, max_year = datetime_to_range_year(date.fromisoformat(max_date), period_length)

    nb_period = 365//period_length

    print('Reading Location.csv')
    Locations = pd.read_csv(input_path+'Location_MarketData.csv')
    print('Reading Articles.csv')
    Articles = pd.read_csv(input_path+'Articles.csv')
    Sales_Articles_Location_MarketData = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')
    Sales_Articles_Location_MarketData.drop_duplicates(subset=[item_key], inplace=True)

    Date = []
    Datetime = []
    for datetime in daterange(min_date, max_date):
        # Date.append(datetime.strftime('%Y-%m-%d'))
        period, year = datetime_to_range_year(datetime, period_length)
        if Date == [] or Date[-1] != [period, year]:
            Date.append([period, year])
            Datetime.append(datetime.strftime('%Y-%m-%d'))
            print(datetime.strftime('%Y-%m-%d'))

    print(Date)
    print('Meshgrid')
    Loc, Art, D = np.meshgrid(Locations[location_key], Sales_Articles_Location_MarketData[item_key], Datetime, indexing='ij')
    n1, n2, n3 = len(Locations[location_key]), len(Sales_Articles_Location_MarketData[item_key]), len(Datetime)
    print(n1)
    print(n2)
    print(n3)
    print(n1*n2*n3)
    # print(Loc)
    # print(Art)
    # print(D)
    # print(len(Loc.flatten()))
    # print(len(Art.flatten()))
    # print(len(D.flatten()[:, 0]))
    # print(len(D.flatten()[:, 1]))
    # print(D.shape)
    # D = D.flatten()
    # D = np.array(D)
    # print(D.shape)
    # print(D[0])
    # D = D.reshape(-1, D.shape[-1])
    # print(D)
    # print(D[:, 0])
    # data = np.array([Loc, Art, D.flatten()[:, 0], D.flatten()[:, 1]])
    # print(data)
    print('Flatten Loc')
    Loc_flat = Loc.flatten()[:1000]
    print(Loc_flat)
    print(len(Loc_flat))
    print('Flatten Art')
    Art_flat = Art.flatten()[:1000]
    print(Art_flat)
    print(len(Art_flat))
    print('Flatten D')
    D_flat = D.flatten()[:1000]
    print(D_flat)
    print(len(D_flat))

    fromisoformat_vect = np.vectorize(date.fromisoformat)
    Period_flat, Year_flat = datetime_to_range_year_vect(fromisoformat_vect(D_flat), period_length)

    nb_rows = len(Loc_flat)
    print('Nb rows '+str(nb_rows))
    print('Y')
    Y_flat = np.zeros(nb_rows)

    print('data')
    data = np.array([Loc_flat, Art_flat, D_flat, Period_flat, Year_flat, Y_flat]).T
    print(data)
    extra_df = pd.DataFrame(data, columns=[location_key, item_key, date_key, period_key, year_key, 'Y'])
    print('Concat extra df and df')
    df = pd.concat([df, extra_df], ignore_index=True)

    print(df)
    # print('Reshape date')
    # df = reshape_date(df)

    print('drop duplicates')
    df.drop_duplicates(subset=[location_key, item_key, period_key, year_key], inplace=True)
    # print(extra_df)
    # print(Loc)
    # print(Art)
    # print(D)
    # for loc in Locations[location_key]:
    #     for article in Articles[item_key]:



    # nb_period = 365//period_length
    #
    # for year in range(min_date[1], max_date[1]+1)
    #     for day_index in range()

    return df



def compute_XY(save = False, filename='XY.csv'):
    '''
        Read the Sales_Articles_Location_MarketData.csv file.
        Build the BinaryEncoded dataframe containing both the X and the Y.
    '''

    print('\nReading Sales_Articles_Location_MarketData.csv')
    df = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')

    df = select_columns_of_interest(df) # Keep only interesting columns
    df.drop_duplicates(inplace=True)
    df = reshape_date(df)
    # df = add_Y(df)
    df = add_unsold_rows(df)
    df = encode_categorical_features(df)
    df = drop_residual_columns(df)

    print(df)
    if save:
        print('Saving')
        df.to_csv(output_path+filename,index=False)

    return df

if __name__ == '__main__':
    compute_XY(save=True, filename='XYY_{}.csv'.format(period_length))
