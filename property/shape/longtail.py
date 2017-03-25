'''定义了一个判断长尾图形的类'''
from property.property import BaseProperty

class LongTail(BaseProperty):
    '''k线图图形中的长尾巴图形'''
    name = "longtail"

    def init(self, config):
        self.day = config["day"] if config and "day" in config else 0
        self.tail = config["tail"] if config and "tail" in config else 0.5
        self.head = config["head"] if config and "head" in config else 0.3

    def value(self):
        p_open = self._history.open[self.day]
        p_close = self._history.close[self.day]
        p_high = self._history.high[self.day]
        p_low = self._history.low[self.day]
        body_h = max(p_open, p_close)
        body_l = min(p_open, p_close)
        head = (p_high - body_h) / (p_high - p_low)
        tail = (body_l - p_low) / (p_high - p_low)
        return head <= self.head and tail >= self.tail

    def __repr__(self):
        return "day " + str(self.day) + " is " if self.value() else " is not " + self.name
