import pandas as pd
############################################################################
# Execute this file to make all possible joins of the tables in input_path #
############################################################################

input_path = '../data/data_raw/'
output_path = '../data/data_cleaned/'


def delete_column_with_regex(df, regex):
    df = df[df.columns.drop(list(df.filter(regex=regex)))]
    return df

# Load all tables and set primary index if it exists
print('\nLoading csv...\nLocation.csv')
Location = pd.read_csv(input_path+'Location.csv')
Location.set_index('Location (Code)', verify_integrity=True)
# Articles = pd.read_csv('data/Articles.csv')
print('Market_Data.csv')
Market_Data = pd.read_csv(input_path+'Market_Data.csv')
print('Sales.csv\n')
Sales = pd.read_csv(input_path+'Sales.csv')
# Stock = pd.read_csv('data/Stock.csv')


# Jointures :
Location_Sales = Sales.merge(Location, on=['Location (Code)'], how='outer', suffixes=('', '_to_delete'))
Location_Sales = delete_column_with_regex(Location_Sales, '_to_delete')

Location_MarketData = Market_Data.merge(Location, on=['Location (Code)'], how='outer', suffixes=('', '_to_delete'))
Location_MarketData = delete_column_with_regex(Location_MarketData, '_to_delete')

# Save joins
print('Saving...')
Location_Sales.to_csv(output_path+'/Location_Sales.csv',index=False)
Location_MarketData.to_csv(output_path+'Location_MarketData.csv',index=False)
