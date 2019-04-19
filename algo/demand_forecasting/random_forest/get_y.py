import pandas as pd


file_test = '../../../data/data_cleaned/Sales_MarketData.csv'

dataframe = pd.read_csv(file_test)
def get_y(item_code, location_code, date):
    global dataframe
    df = dataframe.query('Item_Code == @item_code & Location_Code == @location_code & Day_in_year_YYYYMMDD == @date')

    s = 0
    for index, row in df.iterrows():
        s+= int(row["Sales_units"])

    return s


if __name__=='__main__':
    print(get_y('SLT', 'MCA', '2016-04-15'))
    print(get_y('SLT', 'MCA', '2016-09-06'))
