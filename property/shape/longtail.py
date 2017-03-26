'''定义了一个判断长尾图形的类'''
from property.property import BaseProperty

class LongTail(BaseProperty):
    '''k线图图形中的长尾巴图形'''
    name = "longtail"
    __days = []
    def init(self, config):
        self.start = config["start"] if config and "start" in config else 0
        self.end = config["end"] if config and "end" in config else self.start + 1
        self.tail = config["tail"] if config and "tail" in config else 0.45
        self.head = config["head"] if config and "head" in config else 0.3
        self.swing = config["swing"] if config and "swing" in config else 0.02
    def value(self):
        has = False
        for day in range(self.start, self.end):
            if self.longtail(day):
                has = True
                self.__days.append(self._history.index[day])
        return has

    def __repr__(self):
        if self.value():
            return "it has " + self.name + " on " + ",".join(self.__days)
        else:
            return "it has no " + self.name

    def longtail(self, day):
        '''whether the shape on the day is long tail'''
        p_open = self._history.open[day]
        p_close = self._history.close[day]
        p_last_close = self._history.close[day + 1]
        p_high = self._history.high[day]
        p_low = self._history.low[day]
        swing = (p_high - p_low) / p_last_close
        if swing < self.swing:
            return False
        body_h = max(p_open, p_close)
        body_l = min(p_open, p_close)
        head = (p_high - body_h) / (p_high - p_low)
        tail = (body_l - p_low) / (p_high - p_low)
        return head <= self.head and tail >= self.tail
