from .articles_cleaning import *
import pandas as pd

Location = pd.read_csv('data/Location.csv')
Location.set_index('Location (Code)', verify_integrity=True)
# Articles = pd.read_csv('data/Articles.csv')
# Market_Data = pd.read_csv('data/Market_Data.csv')
Sales = pd.read_csv('data/Sales.csv')
# Stock = pd.read_csv('data/Stock.csv')

print(Location)

# columns_to_use = Location.columns.difference(Sales.columns)
Location_Sales = Sales.merge(Location, on=['Location (Code)'], how='outer', suffixes=('', '_to_delete'))
Location_Sales.to_csv("final.csv",index=False)
print(Location_Sales)
