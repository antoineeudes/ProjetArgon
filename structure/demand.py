class Demand:
    def __init__(self, demand = dict()):
        self._demand = demand

    def set_demand_DLA(day, location, article, demand):
        assert(day >= 0)
        assert(day < 365)

        if not day in self._demand.keys():
            self._demand[day] = dict()
            self._demand[day][location] = dict()
            self._demand[day][location][article] = demand

        elif not location in self._demand[day].keys():
            self._demand[day][location] = dict()
            self._demand[day][location][article] = demand

        else:
            pass
