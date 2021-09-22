from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget


class PickList(QListWidget):
    def __init__(self, callback, *__args):
        super().__init__(*__args)

        self.callback = callback
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.itemDoubleClicked.connect(self._callback)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self._callback()
        else:
            super(PickList, self).keyPressEvent(event)

    def _callback(self):
        if len(self.selectedItems()) > 0:
            self.callback(self.selectedItems()[0])
