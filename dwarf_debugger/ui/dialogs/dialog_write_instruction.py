from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class WriteInstructionDialog(QDialog):
    def __init__(self, parent=None, input_content='', arch='', mode=''):
        super(WriteInstructionDialog, self).__init__(parent)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('insert instruction'))
        self.input_widget = QLineEdit(self)
        if len(input_content) > 0:
            self.input_widget.setText(input_content)
        self.input_widget.setMinimumWidth(350)
        layout.addWidget(self.input_widget)

        arch_mode_layout = QHBoxLayout()
        import keystone
        ks_objs = dir(keystone.keystone_const)

        self.arch = QComboBox(self)
        for w in ks_objs:
            if w.startswith('KS_ARCH_'):
                self.arch.addItem(w.replace('KS_ARCH_', '').lower())
                if w == arch:
                    self.arch.setCurrentIndex(self.arch.count() - 1)
        arch_mode_layout.addWidget(self.arch)

        self.mode = QComboBox(self)
        for w in ks_objs:
            if w.startswith('KS_MODE_'):
                self.mode.addItem(w.replace('KS_MODE_', '').lower())
                if w == mode:
                    self.mode.setCurrentIndex(self.mode.count() - 1)
        arch_mode_layout.addWidget(self.mode)

        layout.addLayout(arch_mode_layout)

        buttons = QHBoxLayout()
        ok = QPushButton('Ok')
        buttons.addWidget(ok)
        ok.clicked.connect(self.accept)
        cancel = QPushButton('cancel')
        cancel.clicked.connect(self.close)
        buttons.addWidget(cancel)
        layout.addLayout(buttons)

    def keyPressEvent(self, event):
        super(WriteInstructionDialog, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Return:
            self.accept()

    @staticmethod
    def show_dialog(input_content='', arch='', mode=''):
        dialog = WriteInstructionDialog(input_content=input_content, arch=arch, mode=mode)
        result = dialog.exec_()

        return result == QDialog.Accepted, \
               dialog.input_widget.text(), \
               dialog.arch.currentText(), \
               dialog.mode.currentText()
