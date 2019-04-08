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

print(datetime_to_day_year(datetime))
print(datetime_to_range_year(datetime, 7))

Sales_Articles_Location = pd.read_csv(input_path+'Sales_Articles_Location.csv')
# Sales_Articles_Location.info()
X = []

Locations = pd.read_csv(input_path+'Location.csv')
# print(Locations[location_key])
columns = []

for loc in Locations[location_key]:
    columns.append('L_'+loc)

Articles = pd.read_csv(input_path+'Articles.csv')
# print(Articles[item_key])

for item in Articles[item_key]:
    columns.append('I_'+item)

columns.append('Range_index')
columns.append('Year')

X_Dataframe = pd.DataFrame(columns=columns)


for index, row in Sales_Articles_Location.iterrows():
    range_index, year = datetime_to_range_year(date.fromisoformat(row['Day_in_year_YYYYMMDD']), range_width)
    # print('{} {}'.format(range_index, year))
    df = pd.DataFrame(np.array([[1, 1, range_index, year]]), columns=['L_'+row[location_key], 'I_'+row[item_key], 'Range_index', 'Year'])
    X_Dataframe = pd.concat([X_Dataframe,df], axis=0, ignore_index=True)
    print(index)
    # print(df)
    # df.append(X_Dataframe, ignore_index=True)
    # if index > 10:
    #     break
# print(X_Dataframe)


X_Dataframe.fillna(0, inplace=True)
print(X_Dataframe)
X_Dataframe.to_csv(output_path+'RandomForest_X.csv')
