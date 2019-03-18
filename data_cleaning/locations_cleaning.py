import pandas as pd

def clean_locations():
    locations = pd.read_csv('../data/data_raw/Location.csv')
    locations = locations.drop(columns="isWFJactive")
    locations = locations[locations["IsOpen"]=="Open"]
    locations = locations.drop(columns="IsOpen")
    locations.to_csv("../data/data_cleaned/Location.csv", index=False, encoding='utf8')