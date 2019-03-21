import pandas as pd
# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

input_path = '../../data/data_cleaned/'

def mean_model():
    Sales = pd.read_csv(input_path+'Sales.csv')

    # Test model on a single location
    most_frequent_location = Sales['Location_Code'].value_counts().idxmax()
    most_frequent_location_count = Sales['Location_Code'].value_counts().max()
    print(most_frequent_location)
    print(most_frequent_location_count)

    Sales_in_MFL = Sales.loc[Sales['Location_Code'] == most_frequent_location]
    # Sales_in_MFL['Sales_units'] = Sales_in_MFL['Sales_units'].cumsum()
    # Sales_in_MFL['Day_in_year_YYYYMMDD'] = pd.to_datetime(Sales_in_MFL.Day_in_year_YYYYMMDD)
    # Sales_in_MFL['Sales_units'].to_csv('test.csv')
    print(Sales_in_MFL.describe())
    # Sales_in_MFL.plot(x='Day_in_year_YYYYMMDD', y='Sales_units')
    # plt.show()
    # print(Sales_in_MFL)
    # print(Sales)
