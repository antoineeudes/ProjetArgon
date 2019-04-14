import random
import unittest
import sys
sys.path.append("..")
from structure.stock import Stock
from structure.demand import Demand
from structure.sales import Sales

from algo.compute_results.compute_sales import compute_sales_over_year


class ComputeSalesTest(unittest.TestCase):

    def test_create_stock(self):
        stock = Stock()
        stock.define_iso("ZDB", "UBADP", "2016-01-02", 4)
        stock.define_iso("ZDB", "UBADP", "2016-01-02", 5)
        stock.define_iso("ZDB", "UBADP", "2016-01-03", 2)
        stock.define_iso("ZDB", "AME", "2016-01-03", 10)

        demand = Demand()
        demand.set_demand_DLA(1, 'UBADP', 'ZDB', 3)
        demand.set_demand_DLA(2, 'UBADP', 'ZDB', 3)

        sales, remaining_stock = compute_sales_over_year(demand, stock, 2016)

        self.assertEqual(remaining_stock.get_stock('ZDB', 'UBADP', 2016, 1), 2)
        self.assertEqual(sales.get_sales_DLA(1, 'UBADP', 'ZDB'), 3)
        self.assertEqual(remaining_stock.get_stock('ZDB', 'UBADP', 2016, 2), 0)
        self.assertEqual(sales.get_sales_DLA(2, 'UBADP', 'ZDB'), 2)

        # sales.show_L('UBADP', ['ZDB'])
if __name__=="__main__":
    unittest.main()
