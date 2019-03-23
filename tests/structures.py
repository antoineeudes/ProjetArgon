import random
import unittest
import sys
sys.path.append("..")
from structure.stock import Stock
from structure.demand import Demand
from structure.sales import Sales


class StockTest(unittest.TestCase):

    def test_create_stock(self):
        stock = Stock()
        stock.define("ZDB", "UBADP", "2016-01-02", 4)
        stock.define("ZDB", "UBADP", "2016-01-02", 5)
        stock.define("ZDB", "AME", "2016-01-03", 10)

        self.assertEqual(stock.get_stock_iso('ZDB', 'UBADP', '2016-01-02'), 5)
        self.assertEqual(stock.get_stock('ZDB', 'UBADP', 2016, 1), 5)
        # self.assertEqual(len(stock.state[2016]), 2)

    def test_get_iterable(self):
        stock = Stock()
        iter = stock.get_day_iterable_of_year(2016)

        self.assertEqual(iter, [])

        stock.define("ZDB", "UBADP", "2016-01-02", 4)
        stock.define("ZDB", "UBADP", "2016-01-02", 5)
        stock.define("ZDB", "AME", "2016-01-03", 10)
        stock.define("ZDB", "AME", "2017-01-04", 10)
        iter = stock.get_day_iterable_of_year(2016)

        self.assertTrue(1 in iter)
        self.assertFalse(3 in iter)

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

class SalesTest(unittest.TestCase):

    def test_set_demand(self):
        sales = Sales()
        sales.new_sale_DLA(5, 'ZDB', 'AME', 2)

        self.assertEqual(sales.get_sales_DLA(5, 'ZDB', 'AME'), 2)
        self.assertEqual(sales.get_sales_DLA(6, 'ZDB', 'AME'), 0)

if __name__=="__main__":
    unittest.main()
