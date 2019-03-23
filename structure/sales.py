from matplotlib import pyplot as plt

class Sales():
    def __init__(self, sales = dict()):
        self._sales = sales

    def new_sale_DLA(self, day, location, article, quantity):
        assert(day >= 0)
        assert(day < 365)

        if not day in self._sales.keys():
            self._sales[day] = dict()
            self._sales[day][location] = dict()
            self._sales[day][location][article] = quantity

        elif not location in self._sales[day].keys():
            self._sales[day][location] = dict()
            self._sales[day][location][article] = quantity

        else:
            self._sales[day][location][article] = quantity

    def get_sales_DLA(self, day, location, article):
        if not day in self._sales.keys():
            return 0

        if not location in self._sales[day].keys():
            return 0

        if not article in self._sales[day][location].keys():
            return 0

        return self._sales[day][location][article]

    def show_L(self, location, articles = []):
        '''Plot chart of sales over time of an article in a location'''

        X = range(365)
        for article in articles:
            Y= []
            for i in X:
                Y.append(self.get_sales_DLA(i, location, article))
            plt.plot(X, Y, label=article)

        plt.show()
