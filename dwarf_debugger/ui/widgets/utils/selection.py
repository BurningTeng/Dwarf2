from PyQt5.Qt import QObject
from PyQt5.QtGui import QColor

class Selection(QObject):
    """ Selection
    """

    def __init__(self, start=0, end=0, active=True, color=QColor('#ef5350')):
        super(Selection, self).__init__()
        self._start = int(min(start, end))
        self._end = int(max(start, end))
        self.active = active
        self.color = color

    def __len__(self):
        """ len
        """
        return self._end - self._start

    def contains(self, address):
        """ contains addr
        """
        return self._end <= address <= self._start
        # return address >= self._start and address <= self._end

    # enforce that start <= end
    @property
    def start(self):
        """ Get StartPoint
        """
        return self._start

    @start.setter
    def start(self, value):
        """ Set Startpoint
        """
        if not self.active:
            self._start = self._end = value
            return
        self._start = int(min(value, self.end))
        self._end = int(max(value, self.end))

    @property
    def end(self):
        """ Get Endpoint
        """
        return self._end

    @end.setter
    def end(self, value):
        """ Set Endpoint
        """
        if not self.active:
            self._start = self._end = value
            return
        self._end = int(max(value, self.start))
        self._start = int(min(value, self.start))
