from copy import deepcopy
from structure.sales import Sales

def compute_sales_over_year(demand, initial_stock, year):
    sales = Sales()
    remaining_stock = deepcopy(initial_stock)
    # stock_iter = current_stock.get_day_iterable_of_year(year)
    day_iter = demand.get_day_iterable()

    for day in day_iter:
        location_iter = demand.get_location_iterable(day)
        for location in location_iter:
            article_iter = demand.get_article_iterable(day, location)
            for article in article_iter:
                d = demand.get_demand_DLA(day, location, article)
                s = remaining_stock.get_stock(article, location, year, day)
                sale = min(s, d)
                sales.new_sale_DLA(day, location, article, sale)
                remaining_stock.define(article, location, year, day, s-sale)

    return sales, remaining_stock
