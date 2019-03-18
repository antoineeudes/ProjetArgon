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
