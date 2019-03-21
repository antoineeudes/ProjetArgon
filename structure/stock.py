


class Stock:
    def __init__(self, stock=dict()):
        self.state = stock

    def define(self, item_code, location_code, datetime, quantity):
        try:
            self.state[datetime][location_code][item_code] = quantity
        except:
            try:
                self.state[datetime][location_code] = dict()
                self.define(item_code, location_code, datetime, quantity)
            except:
                self.state[datetime] = dict()
                self.define(item_code, location_code, datetime, quantity)

    def 
if __name__=='__main__':
    stock = Stock()
    stock.define("ZDB", "UBADP", "00:00:00Z01:01:2018T", 4)
    
    stock.define("ZDB", "UBADP", "00:00:00Z02:01:2018T", 5)
    stock.define("ZDB", "AME", "00:00:00Z02:01:2018T", 5)
    print(stock.state)