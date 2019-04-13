import pandas as pd


file_test = '../../../data/data_cleaned/Sales_MarketData.csv'

def get_y(item_code, location_code, date, fichier=file_test):
    dataframe = pd.read_csv(fichier)
    dataframe = dataframe[dataframe['Item_Code']==item_code]
    dataframe = dataframe[dataframe['Location_Code']==location_code]
    dataframe = dataframe[dataframe['Day_in_year_YYYYMMDD']==date]
    s = 0
    for index, row in dataframe.iterrows():
        s+= int(row["Sales_units"])
    return s

if __name__=='__main__':
    print(get_y('SLT', 'MCA', '2016-04-15'))