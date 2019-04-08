
import pandas as ps
from datetime import date

class Stock:
    def __init__(self, stock=None):
        self.state = dict()
        if stock != None:
            self.state = stock

    def define(self, item_code, location_code, year, day_index, quantity):
        try:
            self.state[year][day_index][location_code][item_code] = quantity
        except KeyError:
            try:
                self.state[year][day_index][location_code] = dict()
                self.define(item_code, location_code, year, day_index, quantity)
            except KeyError:
                try:
                    self.state[year][day_index] = dict()
                    self.define(item_code, location_code, year, day_index, quantity)
                except KeyError:
                    self.state[year] = dict()
                    self.define(item_code, location_code, year, day_index, quantity)

    def define_iso(self, item_code, location_code, datetime_iso, quantity):

        datetime = date.fromisoformat(datetime_iso)
        year = datetime.year
        d0 = date(year, 1, 1)
        day_index = (datetime-d0).days

        return self.define(item_code, location_code, year, day_index, quantity)

    def get_stock(self, item_code, location_code, year, day_index):
        if not year in self.state.keys():
            return 0

        if not day_index in self.state[year].keys():
            return 0

        if not location_code in self.state[year][day_index].keys():
            return 0

        if not item_code in self.state[year][day_index][location_code].keys():
            return 0

        return self.state[year][day_index][location_code][item_code]

    def get_stock_iso(self, item_code, location_code, datetime_iso):
        datetime = date.fromisoformat(datetime_iso)
        year = datetime.year
        d0 = date(year, 1, 1)
        day_index = (datetime-d0).days

        return self.get_stock(item_code, location_code, year, day_index)


    def get_day_iterable_of_year(self, year):
        if not year in self.state.keys():
            return []
        return self.state[year].keys()

    def getAllTimeStock(self, stock_file_path="../data/data_cleaned/Stock.py", sales_file_path="../data/data_cleaned/"):
        sales = pd.read_csv(stock_file_path)
        sales.describe()

        
if __name__=='__main__':
    stock = Stock()
    stock.define("ZDB", "UBADP", 2016, "2016-01-02T00:00:00.000Z", 4)
    stock.define("ZDB", "UBADP", 2016, "2016-01-02T00:00:00.000Z", 5)
    stock.define("ZDB", "AME", 2016, "2016-01-03T00:00:00.000Z", 10)
    print(stock.state)
