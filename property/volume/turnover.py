'''the turnover of a stock on some day'''
from property.property import BaseProperty

class Turnover(BaseProperty):
    '''the turnover of a stock'''
    name = "turnover"

    def init(self, config):
        self.day = config["day"] if config is not None else 0

    def value(self):
        return self._history[self.name][self.day]

    def __repr__(self):
        return self.name + " of day " + str(self.day) + \
         " is " + str(self.value())
