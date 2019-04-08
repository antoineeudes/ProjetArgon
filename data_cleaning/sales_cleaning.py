import pandas as pd
from pandas import read_csv
from matplotlib import pyplot as plt
import numpy as np



def clean_sales():
    print("Cleaning Sales.csv...")
    sales = pd.read_csv('../data/data_raw/Sales.csv')
    sales = sales[sales["Sales units"]>0]
    sales.to_csv("../data/data_cleaned/Sales.csv", index=False, encoding='utf8')
    print("Done.")