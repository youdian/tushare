'''the volume of a stock on some day'''
from property.property import BaseProperty

class Volume(BaseProperty):
    '''the volume of a stock in rencent days
    config parameters: day integer default 0. ie,
    config = {"day": 1}
    '''
    name = "volume"

    def init(self, config):
        self.day = self._config["day"] if self._config is not None else 0

    def value(self):
        return self._history[self.name][self.day]

    def __repr__(self):
        return self.name + " of day " + str(self.day) + \
         " is " + str(self.value())
