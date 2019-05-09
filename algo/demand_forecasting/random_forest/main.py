
from transform_features import compute_XY
from random_forest import trainRandomForest_on, testRandomForest_on
from compute_demand import compute_demand
from datetime import date
from tools import period_length, describeY

if __name__ == '__main__':
    dirname = 'XY_stockbased_{}'.format(period_length)

    compute_XY(save=True, dirname=dirname)
    # print(testRandomForest_on(dirname))
    min_date = date.fromisoformat('2019-01-01')
    max_date = date.fromisoformat('2020-01-01')
    demand = compute_demand(min_date, max_date, dirname, save=True)
    print(demand)
    describeY('demand.csv')
