import pandas as pd
from datetime import timedelta, date
from tools import *


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

def get_y_dict_fast(number_days_in_period):
    global dataframe
    Count = dict()
    k = 0
    for index, row in dataframe.iterrows():
        location_code = row[location_key]
        item_code = row[item_key]
        number_period, year = datetime_to_range_year(date.fromisoformat(row[date_key]), number_days_in_period)
        key = (location_code, item_code, number_period, year)
        if not key in Count:
            Count[key] = row['Sales_units']
        else:
            Count[key] += row['Sales_units']
        print_percent(k, dataframe.shape[0], prefix='Build sales dict (0) : ')
        k += 1

    return Count

if __name__=='__main__':
    print(get_y('SLT', 'MCA', 0, 2016, 7))
