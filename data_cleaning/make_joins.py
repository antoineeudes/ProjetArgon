import pandas as pd
############################################################################
# Execute this file to make all possible joins of the tables in input_path #
############################################################################

input_path = '../data/data_raw/'
output_path = '../data/data_cleaned/'

#Keys name :
location_key = 'Location (Code)'
item_key = 'Item (Code)'

def delete_column_with_regex(df, regex):
    df = df[df.columns.drop(list(df.filter(regex=regex)))]
    return df

# Load all tables and set primary index if it exists
print('\nLoading csv...\nLocation.csv')
Location = pd.read_csv(input_path+'Location.csv')
Location.set_index('Location (Code)', verify_integrity=True)
print('Articles.csv')
Articles = pd.read_csv(input_path+'Articles.csv')
Articles.set_index('Item (Code)', verify_integrity=True)
print('Market_Data.csv')
Market_Data = pd.read_csv(input_path+'Market_Data.csv')
print('Sales.csv\n')
Sales = pd.read_csv(input_path+'Sales.csv')
# Stock = pd.read_csv('data/Stock.csv')


# Jointures :
Location_Sales = Sales.merge(Location, on=[location_key], how='outer', suffixes=('', '_to_delete'))
Location_Sales = delete_column_with_regex(Location_Sales, '_to_delete')

Location_MarketData = Market_Data.merge(Location, on=[location_key], how='outer', suffixes=('', '_to_delete'))
Location_MarketData = delete_column_with_regex(Location_MarketData, '_to_delete')

Articles_Sales = Sales.merge(Articles, on=[item_key], how='outer', suffixes=('', '_to_delete'))
Articles_Sales = delete_column_with_regex(Articles_Sales, '_to_delete')

Articles_Location_Sales = Articles_Sales.merge(Location, on=[location_key], how='outer', suffixes=('', '_to_delete'))
Articles_Location_Sales = delete_column_with_regex(Articles_Location_Sales, '_to_delete')

# Save joins
print('Saving...\nLocation_Sales.csv')
Location_Sales.to_csv(output_path+'Location_Sales.csv',index=False)
print('Location_MarketData.csv')
Location_MarketData.to_csv(output_path+'Location_MarketData.csv',index=False)
print('Articles_Sales.csv')
Articles_Sales.to_csv(output_path+'Articles_Sales.csv',index=False)
print('Articles_Location_Sales.csv')
Articles_Location_Sales.to_csv(output_path+'Articles_Location_Sales.csv',index=False)
