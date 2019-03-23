


class Stock:
    def __init__(self, stock=None):
        self.state = dict()
        if stock != None:
            self.state = stock

    def define(self, item_code, location_code, year, datetime, quantity):
        try:
            self.state[year][datetime][location_code][item_code] = quantity
        except KeyError:
            try:
                self.state[year][datetime][location_code] = dict()
                self.define(item_code, location_code, year, datetime, quantity)
            except KeyError:
                try:
                    self.state[year][datetime] = dict()
                    self.define(item_code, location_code, year, datetime, quantity)
                except KeyError:
                    self.state[year] = dict()
                    self.define(item_code, location_code, year, datetime, quantity)

    def get_day_iterable_of_year(self, year):
        if not year in self.state.keys():
            return []

        return self.state[year].keys()

if __name__=='__main__':
    stock = Stock()
    stock.define("ZDB", "UBADP", 2016, "2016-01-02T00:00:00.000Z", 4)
    stock.define("ZDB", "UBADP", 2016, "2016-01-02T00:00:00.000Z", 5)
    stock.define("ZDB", "AME", 2016, "2016-01-03T00:00:00.000Z", 10)
    print(stock.state)
