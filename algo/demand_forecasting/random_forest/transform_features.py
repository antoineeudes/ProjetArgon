import pandas as pd
import numpy as np
from datetime import date

input_path = '../../../data/data_cleaned/'
output_path = '../../../data/data_cleaned/'

location_key = 'Location_Code'
item_key = 'Item_Code'

range_width = 1 # Précision 1 jour



def datetime_to_day_year(datetime):
    year = datetime.year
    d0 = date(year, 1, 1)
    day_index = (datetime-d0).days

    return day_index, year

datetime = date.fromisoformat('2016-02-08')

def datetime_to_range_year(datetime, range_width):
    day_index, year = datetime_to_day_year(datetime)
    return day_index//range_width, year


Sales_Articles_Location = pd.read_csv(input_path+'Sales_Articles_Location_MarketData.csv')
X = []
index_key = dict()

Locations = pd.read_csv(input_path+'MarketData_Location.csv')
k = 0

for loc in Locations[location_key]:
    index_key[k] = 'L_'+loc
    k += 1

Articles = pd.read_csv(input_path+'Articles.csv')

for item in Articles[item_key]:
    index_key[k] = 'I_'+item
    k += 1

index_key[k] = 'Range_number'
index_key[k+1] = 'Year'
k+= 2

# For any key (ex: a location or item code), give it's position in the vector X
key_index = {v: k for k, v in index_key.items()}

# print(key_index)

# X_Dataframe = pd.DataFrame(columns=columns)
#
#
for index, row in Sales_Articles_Location.iterrows():
    range_number, year = datetime_to_range_year(date.fromisoformat(row['Day_in_year_YYYYMMDD']), range_width)

    location_index = key_index['L_'+row[location_key]]
    item_index = key_index['I_'+row[item_key]]
    range_index = key_index['Range_number']
    year_index = key_index['Year']

    new_entry = [0]*k

    new_entry[location_index] = 1
    new_entry[item_index] = 1
    new_entry[range_index] = range_number
    new_entry[year_index] = year

    X.append(new_entry)
    print(index)
    # if index > 10000:
    #     break

# print(X)
columns = list(key_index.keys())
# print(columns)

# print('Creating dataframe')
# X_Dataframe = pd.DataFrame(data=X, columns=columns)

# print(X_Dataframe)

#
# X_Dataframe.fillna(0, inplace=True)
# print(X_Dataframe)
print('Writing dataframe')
# X_Dataframe.to_csv(output_path+'RandomForest_X.csv')
file = open(output_path+'RandomForest_X.csv', 'w')

for j in range(k):
    file.write(','+columns[j])
file.write('\n')
for i in range(1, len(X)):
    print(i)
    file.write(str(i))
    for j in range(k):
        file.write(','+columns[j])
    file.write('\n')

file.close()
