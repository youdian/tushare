'''the volume of a stock on some day'''
from property.BaseProperty import BaseProperty

class Volume(BaseProperty):
    '''the volume of a stock in rencent days'''

    def value(self):
        day = 0
        if self._config is not None:
            day = self._config['day']
        return self._history[self._name][day]

    def __repr__(self):
        return self._name + " is " + self.value()
