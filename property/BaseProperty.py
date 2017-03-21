'''base class of all properties'''
from abc import ABCMeta
from abc import abstractmethod

class BaseProperty(metaclass=ABCMeta):
    ''' a base class of all properties. all subclasses must implement value method
    and name property and __repr__ method'''

    def __init__(self, name, history, config):
        '''name String the name of the prooerty
        history DataFrame the daily history of a specfic stock
        '''
        if name is None or name == "":
            raise ValueError("the name of a property can't be empty.")
        if history is None:
            raise ValueError("history is None.")
        self._name = name
        self._history = history
        self._config = config

    @property
    def name(self):
        '''a unique name to identify the property'''
        return self._name

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
