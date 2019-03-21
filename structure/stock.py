


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


if __name__=='__main__':
    stock = Stock()
    stock.define("ZDB", "UBADP", "2016-01-02T00:00:00.000Z", 4)
    stock.define("ZDB", "UBADP", "2016-01-02T00:00:00.000Z", 5)
    stock.define("ZDB", "AME", "2016-01-03T00:00:00.000Z", 10)
    print(stock.state)