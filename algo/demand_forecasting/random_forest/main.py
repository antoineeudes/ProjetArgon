
from transform_features import compute_XY
from random_forest import trainRandomForest_on
from compute_demand import compute_demand
from datetime import date

if __name__ == '__main__':
    compute_XY(save=True, dirname='XY_stockbased_{}'.format(period_length))
    clf, encoder = trainRandomForest_on('XY_stockbased_{}'.format(period_length))
    min_date = date.fromisoformat('2019-01-01')
    max_date = date.fromisoformat('2020-01-01')
    print(compute_demand(min_date, max_date, 'XY_stockbased_{}'.format(period_length), save=True))
