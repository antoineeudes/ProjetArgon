from random_forest import trainRandomForest_on
from datetime import date, timedelta
import pandas as pd
import numpy as np
import category_encoders as ce
import multiprocessing

input_path = '../../../data/data_cleaned/'
output_path = '../../../data/data_cleaned/input/'

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
    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count()-1)

    # Make as many partition of the dataframe as cpu units
    nb_partition = multiprocessing.cpu_count()-1
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

def compute_demand_pool(df, i, kwargs):
    '''
        Compute and add the Y
    '''

    print('Starting process {}'.format(i))
    k = 0
    for index, row in df.iterrows():
        # print([row.to_list()])
        df.at[index, 'Y'] = kwargs['clf'].predict([row.to_list()[:-1]])[0]#get_y(row[item_key], row[location_key], row[period_key], row[year_key], period_length)
        print_percent(k, df.shape[0], prefix='Predict Y ({}) : '.format(i))
        k += 1

    return df

def encode_categorical_features(df, encoder=None):
    '''
        Encode the categorical features using BinaryEncoder.
    '''
    if encoder == None:
        encoder = ce.BinaryEncoder(cols=[location_key, item_key])
        encoder.fit(df)
    return encoder.transform(df), encoder

def compute_demand(min_date, max_date, dirname, save=True):
    nb_period = 365//period_length

    print('\nForecasting sales from {} to {}'.format(min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')))

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
    data = np.array([Loc_flat, Art_flat, Period_flat, Year_flat, Y_flat]).T

    del Loc_flat
    del Art_flat
    del D_flat
    del Period_flat
    del Year_flat
    del Y_flat

    print('\tBuilding dataframe from data array')
    df = pd.DataFrame(data, columns=[location_key, item_key, period_key, year_key, 'Y'])

    del data

    clf, encoder = trainRandomForest_on(dirname)
    df, encoder = encode_categorical_features(df, encoder)

    df = df_pool_computing(compute_demand_pool, df, clf=clf)

    if save:
        print('\nSaving')
        try:
            os.mkdir(output_path+dirname)
        except:
            pass
        print('\tDataframe')
        df.to_csv(output_path+dirname+'/demand.csv',index=False)

    return df


if __name__ == '__main__':
    min_date = date.fromisoformat('2019-01-01')
    max_date = date.fromisoformat('2020-01-01')
    # period_length = 7

    # clf, encoder = trainRandomForest_on('XY_stockbased_7')

    print(compute_demand(min_date, max_date, 'XY_stockbased_7', save=True))
