class Demand:
    def __init__(self, demand = None):
        self._demand = dict()
        if demand != None:
            self._demand = demand

    def set_demand_DLA(self, day, location, article, demand):
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
            self._demand[day][location][article] = demand

    def set_demand_range_LA(self, start_day, end_day, location, article, demand):
        for day in range(start_day, end_day):
            self.set_demand_DLA(day, location, article, demand)

    def get_demand_DLA(self, day, location, article):
        if not day in self._demand.keys():
            return 0

        if not location in self._demand[day].keys():
            return 0

        if not article in self._demand[day][location].keys():
            return 0

        return self._demand[day][location][article]

    def get_demand_DL(self, day, location):
        if not day in self._demand.keys():
            return 0

        if not location in self._demand[day].keys():
            return dict()

        return self._demand[day][location]

    def get_demand_D(self, day):
        if not day in self._demand.keys():
            return dict()

        return self._demand[day]

    def get_demand(self):
        return self._demand

    def get_day_iterable(self):
        return range(365)
