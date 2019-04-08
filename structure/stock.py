
import pandas as ps

class Stock:
    def __init__(self, stock=dict()):
        self.state = stock

    def define(self, item_code, location_code, datetime, quantity):
        try:
            self.state[datetime][location_code][item_code] = quantity
        except KeyError:
            try:
                self.state[datetime][location_code] = dict()
                self.define(item_code, location_code, datetime, quantity)
            except KeyError:
                self.state[datetime] = dict()
                self.define(item_code, location_code, datetime, quantity)

    def getAllTimeStock(self, stock_file_path="../data/data_cleaned/Stock.py", sales_file_path="../data/data_cleaned/"):
        sales = pd.read_csv(stock_file_path)
        sales.describe()


    