import pandas as pd

def delete_column_with_regex(df, regex):
    df = df[df.columns.drop(list(df.filter(regex=regex)))]
    return df

data_path = '../data/data_raw/'
Location = pd.read_csv(data_path+'Location.csv')
Location.set_index('Location (Code)', verify_integrity=True)
# Articles = pd.read_csv('data/Articles.csv')
# Market_Data = pd.read_csv('data/Market_Data.csv')
Sales = pd.read_csv(data_path+'Sales.csv')
# Stock = pd.read_csv('data/Stock.csv')

print(Location)

# columns_to_use = Location.columns.difference(Sales.columns)
# Jointures :
Location_Sales = Sales.merge(Location, on=['Location (Code)'], how='outer', suffixes=('', '_to_delete'))
Location_Sales = delete_column_with_regex(Location_Sales, '_to_delete')

Location_Sales.to_csv("../data/data_cleaned/Location_Sales.csv",index=False)
print(Location_Sales)
