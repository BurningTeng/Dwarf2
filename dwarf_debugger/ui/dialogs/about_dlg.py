from PyQt5.Qt import Qt, QSize, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from dwarf_debugger.ui.dialogs.dwarf_dialog import DwarfDialog

from dwarf_debugger.version import DWARF_VERSION
from dwarf_debugger.lib import utils


class AboutDialog(DwarfDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.title = 'About'
        self.modal = True

        self.setup_ui()

    def setup_ui(self):
        v_box = QVBoxLayout()
        head = QHBoxLayout()
        head.setContentsMargins(10, 10, 0, 10)
        # dwarf icon
        icon = QLabel()
        icon.setPixmap(QPixmap(utils.resource_path('assets/dwarf.svg')))
        icon.setAlignment(Qt.AlignCenter)
        icon.setMinimumSize(QSize(125, 125))
        icon.setMaximumSize(QSize(125, 125))
        head.addWidget(icon)

        # main title
        v_box = QVBoxLayout()
        title = QLabel('Dwarf2')
        title.setContentsMargins(0, 0, 0, 0)
        title.setFont(QFont('Anton', 100, QFont.Bold))
        title.setMaximumHeight(125)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        head.addWidget(title)
        v_box.addLayout(head)

        self.setLayout(v_box)
