from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

from dwarf_debugger.ui.widgets.code_editor import JsCodeEditor


class InputDialogTextEdit(JsCodeEditor):
    def __init__(self, dialog, *__args):
        super().__init__(show_linenumes=True)
        self.dialog = dialog

        self.setStyleSheet('padding: 0; padding: 0 5px;')

        bar = QScrollBar()
        bar.setFixedHeight(0)
        bar.setFixedWidth(0)

    def keyPressEvent(self, event):
        # when code completion popup dont respond to enter
        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            event.ignore()
        super(InputDialogTextEdit, self).keyPressEvent(event)


class InputMultilineDialog(QDialog):
    def __init__(self, parent=None, hint=None, input_content='', min_width=0):
        super(InputMultilineDialog, self).__init__(parent)

        layout = QVBoxLayout(self)

        if hint:
            layout.addWidget(QLabel(hint))
        self.input_widget = InputDialogTextEdit(self)
        if min_width > 0:
            self.input_widget.setMinimumWidth(min_width)

        if len(input_content) > 0:
            self.input_widget.setPlainText(input_content)
        layout.addWidget(self.input_widget)

        buttons = QHBoxLayout()
        ok = QPushButton('ok')
        buttons.addWidget(ok)
        ok.clicked.connect(self.accept)
        cancel = QPushButton('cancel')
        cancel.clicked.connect(self.close)
        buttons.addWidget(cancel)
        layout.addLayout(buttons)

    def sizeHint(self):
        return QSize(1024, 500)

    @staticmethod
    def input(hint=None, input_content='', min_width=0):
        dialog = InputMultilineDialog(hint=hint, input_content=input_content, min_width=min_width)
        result = dialog.exec_()

        return result == QDialog.Accepted, \
               dialog.input_widget.toPlainText()
