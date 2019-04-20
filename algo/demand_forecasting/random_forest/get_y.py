import pandas as pd
from datetime import timedelta, date


file_test = '../../../data/data_cleaned/Sales_MarketData.csv'
dataframe = pd.read_csv(file_test)

def list_of_days_in_period(year, number_period=0, number_days_in_period=0):
    list_of_days = []
    firstJanuary = date(year, 1, 1)
    beginingDate = firstJanuary + timedelta(days=number_period*number_days_in_period)
    list_of_days.append(beginingDate.strftime("%Y-%m-%d"))
    datetoappend = beginingDate
    for i in range(number_days_in_period-1):
        datetoappend = datetoappend + timedelta(days=1)
        list_of_days.append(datetoappend.strftime("%Y-%m-%d"))
    return list_of_days

def get_y(item_code, location_code, number_period, year, number_days_in_period):
    global dataframe
    s = 0
    list_of_days_to_consider = list_of_days_in_period(year, number_period, number_days_in_period)
    for date in list_of_days_to_consider:
        df = dataframe.query('Item_Code == @item_code & Location_Code == @location_code & Day_in_year_YYYYMMDD == @date')
        for index, row in df.iterrows():
            s+= int(row["Sales_units"])
    return s


if __name__=='__main__':
    print(get_y('SLT', 'MCA', 0, 2016, 7))


