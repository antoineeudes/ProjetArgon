import pandas as pd

def clean_stock():
    print("Cleaning Stock.csv...")
    data = pd.read_csv('../data/data_raw/Stock.csv')
    data = data.rename(columns={
        'ITEM_CODE': 'Item_Code',
        'LOCATION_CODE': 'Location_Code'
    })
    data.to_csv("../data/data_cleaned/Stock.csv", index=False, encoding='utf8')
    print("Done.")