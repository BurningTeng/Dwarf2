from PyQt5.Qt import QObject, pyqtSignal


class Caret(QObject):
    """ Caret

        mode = 'hex' or 'ascii'

        Signals:
            posChanged()
    """
    posChanged = pyqtSignal(name='posChanged')

    def __init__(self, mode='hex', pos=0, nibble=0):
        super(Caret, self).__init__()
        self._mode = mode
        self._pos = pos
        self._nibble = nibble

    @property
    def position(self):
        """ Get Position
        """
        return self._pos

    @position.setter
    def position(self, value):
        """ Set Position
        """
        if value >= 0:
            self._pos = value
            self.posChanged.emit()

    @property
    def mode(self):
        """ Get Mode
        """
        return self._mode

    @mode.setter
    def mode(self, value):
        """ Set Mode
            value = 'hex' or 'ascii'
        """
        if value in ('hex', 'ascii'):
            self._mode = value

    @property
    def nibble(self):
        """ Get Nibble
        """
        return self._nibble

    @nibble.setter
    def nibble(self, value):
        """ Set Nibble
        """
        if self._mode == 'hex':
            self._nibble = value
            self.posChanged.emit()

    def update(self, other_cursor):
        """ Update
        """
        # swich between hex and ascii col
        self._mode = other_cursor.mode
        # set position if needed
        if not self.position == other_cursor.position:
            self._pos = other_cursor.position
            self.posChanged.emit()
        if not self.nibble == other_cursor.nibble:
            self._nibble = other_cursor.nibble
            self.posChanged.emit()

    def move_right(self, end):
        """ Move right 1 pos
        """
        self._pos += 1
        if self._pos >= end:
            self._pos = end - 1
        self.posChanged.emit()

    def move_left(self):
        """ Move left 1 pos
        """
        self._pos -= 1
        if self._pos <= 0:
            self._pos = 0
        self.posChanged.emit()

    def move_up(self, bytes_per_line):
        """ Move up 1 line
        """
        self._pos -= bytes_per_line
        if self._pos <= 0:
            self._pos = 0
        self.posChanged.emit()

    def move_down(self, bytes_per_line, end):
        """ Move down 1 line
        """
        self._pos += bytes_per_line
        if self._pos >= end:
            self._pos = end - 1
        self.posChanged.emit()
