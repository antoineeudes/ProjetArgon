import pandas as pd
from datetime import timedelta, date


file_test = '../../../data/data_cleaned/Sales_MarketData.csv'
dataframe = pd.read_csv(file_test)

# Columns names
location_key = 'Location_Code'
item_key = 'Item_Code'
date_key = 'Day_in_year_YYYYMMDD'
period_key = 'Period_number'
year_key = 'Year'

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

def datetime_to_day_year(datetime):
    '''Given a datetime object, return the day of the year (from 0 to 365) and the year'''
    year = datetime.year
    d0 = date(year, 1, 1)
    day_index = (datetime-d0).days

    return day_index, year

def datetime_to_range_year(datetime, period_length):
    '''Given a datetime object, return the period of the year (from 0 to 365//period_length) and the year'''
    day_index, year = datetime_to_day_year(datetime)

    return day_index//period_length, year

def print_percent(index, total, prefix='', rate=10000):
    if index % (total//rate) == 0:
        print(prefix+str(round(100*index/total, 1))+'%')

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
