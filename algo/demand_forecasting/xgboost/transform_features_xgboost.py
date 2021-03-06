import pandas as pd
import numpy as np
from datetime import date
from get_y import get_y

input_path = '../../../data/data_cleaned/'
output_path = '../../../data/data_cleaned/'

# Columns names
location_key = 'Location_Code'
item_key = 'Item_Code'
sales_units_key = 'Sales_units'
department_key = 'Sub_Department'#
price_key = 'Group_of_Level_Price_shortname' #

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

def compute_X(save = False):
    '''
        Read the Sales_Articles_Location_MarketData.csv file and build the one hot encoding
        vector (Location, Article, Day of the year, Year)
    '''

    print('\nReading Sales_Articles_Location_MarketData.csv')
    Sales_Articles_Location = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')
    X = []
    index_key = dict()

    print('Reading MarketData_Location.csv')
    Locations = pd.read_csv(input_path+'MarketData_Location.csv')

    print('Building index')
    k = 0
    for loc in Locations[location_key]:
        index_key[k] = 'L_'+loc # loc is a location_code
        k += 1

    Articles = pd.read_csv(input_path+'Articles.csv')

    # for item in Articles[item_key]:
    #     index_key[k] = 'I_'+item # item is a item_code
    #     k += 1
    # 
    for dep in Articles[department_key]:
        index_key[k] = 'D_'+dep #dep is a sub_Department
        k+=1
    
    for price in Articles[price_key]:
        index_key[k] = 'P_'+price
        k+=1

    # Adding to extra columns for
    index_key[k] = 'Period_number'
    index_key[k+1] = 'Year'
    index_key[k+2] = 'y'
    k+= 3

    # For any key (a location or item code), give it's position in the vector X
    key_index = {v: k for k, v in index_key.items()}

    print('\nBuilding RandomForest_X')
    print('Line (out of {}) :'.format(len(Sales_Articles_Location.index)))
    for index, row in Sales_Articles_Location.iterrows():
        print(index)
        datetime = date.fromisoformat(row['Day_in_year_YYYYMMDD'])
        period_number, year = datetime_to_range_year(datetime, period_length)

        # Compute the wanted indexes
        location_index = key_index['L_'+row[location_key]]
        item_index = key_index['I_'+row[item_key]]
        #department_index = key_index['D_'+row[department_key]]
        price_index = key_index['P_'+row[price_key]]
        period_index = key_index['Period_number']
        year_index = key_index['Year']
        # sales_units_index = key_index['Sales_units']
        y_index = key_index['y']

        new_entry = [0]*k

        # Compute new_entry
        new_entry[location_index] = 1
        #new_entry[item_index] = 1
        new_entry[department_index] = 1
        new_entry[price_index] = 1
        new_entry[period_index] = period_number
        new_entry[year_index] = year
        # new_entry[sales_units_index] = row[sales_units_key]
        new_entry[y_index] = get_y(row[item_key], row[location_key], row['Day_in_year_YYYYMMDD'])
        # new_entry[]

        X.append(new_entry)
        if (index+1) % 10000 == 0:
            print('\t'+str(index))
            break

    # Get all columns
    columns = list(key_index.keys())

    # Save vector X as csv file
    if save:
        file = open(output_path+'RandomForest_X.csv', 'w')

        print('\nWriting RandomForest_X.csv')
        print('Line (out of {}) :'.format(len(Sales_Articles_Location.index)))

        string = ''
        for j in range(k):
            string += ','+columns[j]
        file.write(string+'\n')
        for i in range(1, len(X)):
            string = str(i)
            for j in range(k):
                string += ','+str(X[i][j])
            file.write(string+'\n')
            if i % 10000 == 0:
                print('\t'+str(i))

        file.close()

    return X

if __name__ == '__main__':
    compute_X(save=True)
