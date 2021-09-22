from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, qApp, QStyle)


class DwarfDialog(QDialog):
    """ DwarfDialog
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._title = "Dwarf"
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

    # ************************************************************************
    # **************************** Properties ********************************
    # ************************************************************************

    @property
    def title(self):
        """ return title
        """
        return self._title

    @title.setter
    def title(self, value):
        """ set title
        """
        if isinstance(value, str):
            self._title = "Dwarf2 - " + value

    @property
    def modal(self):
        """ return ismodal
        """
        return self.isModal()

    @modal.setter
    def modal(self, value):
        """ set modal
        """
        if isinstance(value, bool):
            self.setModal(value)

    # override show
    def showEvent(self, QShowEvent):  # pylint: disable=invalid-name
        """ center dialog update title
        """
        self.setWindowTitle(self.title)
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(),
                               qApp.desktop().availableGeometry()))
        return super().showEvent(QShowEvent)
