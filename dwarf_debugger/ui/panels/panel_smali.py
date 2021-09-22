import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFileDialog, QSpinBox, QLabel, QWidget, QPlainTextEdit, QCompleter
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QFontDatabase, QPainter, QTextCursor
from PyQt5.QtCore import QFile, QRegExp, Qt, QRegularExpression, QRect, QSize, QStringListModel, pyqtSignal

from dwarf_debugger.lib.utils import get_os_monospace_font
from dwarf_debugger.lib.prefs import Prefs


class SmaliPanel(QPlainTextEdit):

    def __init__(self, parent=None):
        super(SmaliPanel, self).__init__(parent)
        self.setReadOnly(True)

    def set_file(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'rt') as smali_file:
                self.setPlainText(smali_file.read())
