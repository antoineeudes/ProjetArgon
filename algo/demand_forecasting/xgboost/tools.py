import pandas as pd
import numpy as np
from datetime import date, timedelta
import multiprocessing

input_path = '../../../data/data_cleaned/'
model_input_path = '../../../data/data_cleaned/input/'
output_path = '../../../data/data_cleaned/input/'
try:
    os.mkdir(output_path)
except:
    pass

# Columns names
location_key = 'Location_Code'
class_key = 'Class'
subdepartment_key = 'Sub_Department'
date_key = 'Day_in_year_YYYYMMDD'
period_key = 'Period_number'
year_key = 'Year'

period_length = 14 # Length of the period in days

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
    if (total//rate) == 0 or index % (total//rate) == 0:
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

def describeY(filename='XY.csv'):
    dataframe = pd.read_csv(output_path+'XY_stockbased_'+str(period_length)+'/'+filename)
    Y = dataframe["Y"]
    print(Y.describe())
