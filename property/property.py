'''base class of all properties'''
from abc import ABCMeta
from abc import abstractmethod

class BaseProperty(metaclass=ABCMeta):
    ''' a base class of all properties. all subclasses must implement value method
    and name property and __repr__ method'''

    def __init__(self, history, config):
        '''history DataFrame the daily history of a specfic stock'''
        if history is None:
            raise ValueError("history is None.")
        self._history = history
        self._config = config
        self.init(self._config)

    @abstractmethod
    def init(self, config):
        '''use config to init variable'''
        raise NotImplementedError()

    @abstractmethod
    def value(self):
        '''calculate and return the value defined by self.__config . the value
        maybe a boolean value or a number.
        '''
        raise NotImplementedError()

    @abstractmethod
    def __repr__(self):
        '''return a readable str describing this property'''
        raise NotImplementedError()
