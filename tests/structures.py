import random
import unittest
import sys
sys.path.append("..")
from structure.stock import Stock


class StockTest(unittest.TestCase):

    def test_create_stock(self):
        stock = Stock()
        stock.define("ZDB", "UBADP", "2016-01-02T00:00:00.000Z", 4)
        stock.define("ZDB", "UBADP", "2016-01-02T00:00:00.000Z", 5)
        stock.define("ZDB", "AME", "2016-01-03T00:00:00.000Z", 10)
        self.assertEqual(stock.state["2016-01-02T00:00:00.000Z"]["UBADP"]["ZDB"], 5)
        self.assertEqual(len(stock.state), 2)

if __name__=="__main__":
    unittest.main()