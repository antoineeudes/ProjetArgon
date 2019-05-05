from random_forest import trainRandomForest_on
import pandas as pd
import numpy as np
import category_encoders as ce
from tools import *
import pickle


def compute_demand_pool(df, i, kwargs):
    '''
        Compute and add the Y
    '''

    print('Starting process {}'.format(i))
    k = 0
    for index, row in df.iterrows():
        df.at[index, 'Y'] = kwargs['clf'].predict([row.to_list()[:-2]])[0]#get_y(row[item_key], row[location_key], row[period_key], row[year_key], period_length)
        print_percent(k, df.shape[0], prefix='Predict Y ({}) : '.format(i))
        k += 1

    return df

def encode_categorical_features(df, encoder=None):
    '''
        Encode the categorical features using BinaryEncoder.
    '''
    if encoder == None:
        encoder = ce.BinaryEncoder(cols=[location_key, class_key, subdepartment_key])
        encoder.fit(df)
    return encoder.transform(df), encoder

def decode_categorical_features(df, encoder):
    '''
        Decode the categorical features using BinaryEncoder.
    '''
    return encoder.inverse_transform(df)

def compute_demand(min_date, max_date, dirname, save=True):
    nb_period = 365//period_length

    print('\nForecasting sales from {} to {}'.format(min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')))

    print('\tReading Stock_MarketData')
    Stock_MarketData_Articles = pd.read_csv(input_path+'Stock_MarketData_Articles.csv')

    Locations = Stock_MarketData_Articles[location_key]
    Articles = Stock_MarketData_Articles[item_key]
    Classes = Stock_MarketData_Articles[class_key]
    SubDepartments = Stock_MarketData_Articles[subdepartment_key]

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
    Cla, D = np.meshgrid(Classes, Datetime, indexing='ij')
    SubD, D = np.meshgrid(SubDepartments, Datetime, indexing='ij')

    print('\tFlatten Locations')
    Loc_flat = Loc.flatten()
    print('\tFlatten Articles')
    Art_flat = Art.flatten()
    print('\tFlatten Classes')
    Cla_flat = Cla.flatten()
    print('\tFlatten SubDepartments')
    SubD_flat = SubD.flatten()
    print('\tFlatten Dates')
    D_flat = D.flatten()

    nb_rows = len(Loc_flat)
    print('\tBuild Y')
    Y_flat = np.zeros(nb_rows)

    print('\tBuild Period_flat and Year_flat')
    fromisoformat_vect = np.vectorize(date.fromisoformat)
    Period_flat, Year_flat = datetime_to_range_year_vect(fromisoformat_vect(D_flat), period_length)

    print('\tBuilding data array with {} rows'.format(nb_rows))
    data = np.array([Loc_flat, Cla_flat, SubD_flat, Period_flat, Year_flat, Art_flat, Y_flat]).T

    del Loc_flat
    del Cla_flat
    del SubD_flat
    del D_flat
    del Period_flat
    del Year_flat
    del Y_flat

    print('\tBuilding dataframe from data array')
    df = pd.DataFrame(data, columns=[location_key, class_key, subdepartment_key, period_key, year_key, item_key, 'Y'])

    del data

    encoder = pickle.load(open(model_input_path+dirname+'/encoder.sav', 'rb'))

    clf, _ = trainRandomForest_on(dirname)
    df, _ = encode_categorical_features(df, encoder)

    df = df_pool_computing(compute_demand_pool, df, clf=clf)
    print(df)

    df = decode_categorical_features(df, encoder)
    df.drop([class_key, subdepartment_key], axis=1, inplace=True)

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

    print(compute_demand(min_date, max_date, 'XY_stockbased_{}'.format(period_length), save=True))
