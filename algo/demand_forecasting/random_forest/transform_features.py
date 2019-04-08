import pandas as pd

input_path = '../../../data/data_cleaned/'

Dataframe = pd.read_csv(input_path+'Sales_Articles_Location.csv')

X = []

Locations = pd.read_csv(input_path+'Location.csv')
print(Locations['Location_Code'])
