from articles_cleaning import clean_articles
from locations_cleaning import clean_locations
import pandas as pd

def copy(path):
    data = pd.read_csv('../data/data_raw/Articles.csv')
    data.to_csv('../data/data_cleaned/'+path)

def remove_spaces_in_column_names():
    file_paths = ["Articles.csv", "Sales.csv", "Location.csv", 'Market_Data.csv', "Stock.csv"]
    for file_path in file_paths:
        data = pd.read_csv('../data/data_raw/'+file_path)
        columns_name = data.colums.tolist()
        print(columns_name)


clean_articles()
clean_locations()
remove_spaces_in_column_names()


Location = pd.read_csv('../data/data_raw/Location.csv')
Location.set_index('Location (Code)', verify_integrity=True)
# Articles = pd.read_csv('data/Articles.csv')
# Market_Data = pd.read_csv('data/Market_Data.csv')
Sales = pd.read_csv('../data/data_raw/Sales.csv')
# Stock = pd.read_csv('data/Stock.csv')

print(Location)

# columns_to_use = Location.columns.difference(Sales.columns)
Location_Sales = Sales.merge(Location, on=['Location (Code)'], how='outer', suffixes=('', '_to_delete'))
Location_Sales.to_csv("../data/data_cleaned/Location_Sales.csv",index=False)
print(Location_Sales)
