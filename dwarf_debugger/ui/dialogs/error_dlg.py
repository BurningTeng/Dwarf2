from PyQt5.Qt import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit

from dwarf_debugger.ui.dialogs.dwarf_dialog import DwarfDialog


class ErrorDialog(DwarfDialog):
    def __init__(self, parent=None, label_txt="", text_txt=""):
        super().__init__(parent=parent)

        h_box = QHBoxLayout(self)

        v_box = QVBoxLayout()
        icon = QLabel()
        icon.setPixmap(QIcon('assets/icons/issue.svg').pixmap(QSize(75, 75)))
        icon.setAlignment(Qt.AlignTop)
        h_box.addWidget(icon)

        label = QLabel(label_txt)
        v_box.addWidget(label)

        text = QPlainTextEdit(text_txt)
        text.setReadOnly(True)
        text.setMinimumWidth(550)
        text.setMinimumHeight(300)
        v_box.addWidget(text)
        h_box.addLayout(v_box)

        self.title = "Error"
