import random
import unittest
import sys
sys.path.append("..")
from structure.stock import Stock
from structure.demand import Demand


class StockTest(unittest.TestCase):

    def test_create_stock(self):
        stock = Stock()
        stock.define("ZDB", "UBADP", "2016-01-02T00:00:00.000Z", 4)
        stock.define("ZDB", "UBADP", "2016-01-02T00:00:00.000Z", 5)
        stock.define("ZDB", "AME", "2016-01-03T00:00:00.000Z", 10)
        self.assertEqual(stock.state["2016-01-02T00:00:00.000Z"]["UBADP"]["ZDB"], 5)
        self.assertEqual(len(stock.state), 2)

class DemandTest(unittest.TestCase):

    def test_set_demand_range(self):
        demand = Demand()
        demand.set_demand_range_LA(5, 10, 'ZDB', 'AME', 3)

        self.assertEqual(demand.get_demand_DLA(5, 'ZDB', 'AME'), 3)
        self.assertEqual(demand.get_demand_DLA(9, 'ZDB', 'AME'), 3)
        self.assertEqual(demand.get_demand_DLA(10, 'ZDB', 'AME'), 0)

    def test_edit_existing_demand(self):
        demand = Demand()
        demand.set_demand_range_LA(5, 10, 'ZDB', 'AME', 3)
        demand.set_demand_range_LA(7, 8, 'ZDB', 'AME', 2)

        self.assertEqual(demand.get_demand_DLA(5, 'ZDB', 'AME'), 3)
        self.assertEqual(demand.get_demand_DLA(7, 'ZDB', 'AME'), 2)
        self.assertEqual(demand.get_demand_DLA(8, 'ZDB', 'AME'), 3)
        self.assertEqual(demand.get_demand_DLA(10, 'ZDB', 'AME'), 0)


if __name__=="__main__":
    unittest.main()
