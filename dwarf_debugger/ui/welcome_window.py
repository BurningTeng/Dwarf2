import sys
import os
import random
import json

import requests

from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QPixmap, QIcon, QStandardItemModel, QStandardItem, QFontMetrics
from PyQt5.QtWidgets import (QWidget, QDialog, QLabel, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSpacerItem,
                             QSizePolicy, QStyle, qApp, QHeaderView, QMenu)

from dwarf_debugger.lib import utils, prefs
from dwarf_debugger.lib.git import Git
from dwarf_debugger.ui.widgets.list_view import DwarfListView


class UpdateBar(QWidget):
    onUpdateNowClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAutoFillBackground(True)
        self.setStyleSheet(
            'background-color: crimson; color: white; font-weight: bold; margin: 0; padding: 10px;'
        )
        self.setup()

    def setup(self):
        """ Setup ui
        """
        h_box = QHBoxLayout()
        h_box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(h_box)


    def showEvent(self, QShowEvent):
        h_center = self.update_button.parent().rect().center() - \
            self.update_button.rect().center()
        self.update_button.move(self.update_button.parent(
        ).width() - self.update_button.width() - 10, h_center.y())
        return super().showEvent(QShowEvent)


class WelcomeDialog(QDialog):
    onSessionSelected = pyqtSignal(str, name='onSessionSelected')
    onUpdateComplete = pyqtSignal(name='onUpdateComplete')
    onIsNewerVersion = pyqtSignal(name='onIsNewerVersion')

    def __init__(self, parent=None):
        super(WelcomeDialog, self).__init__(parent=parent)

        self._prefs = parent.prefs

        self._sub_titles = [
            ['duck', 'dumb', 'doctor', 'dutch', 'dark', 'dirty', 'debugging'],
            ['warriors', 'wardrobes', 'waffles', 'wishes', 'worcestershire'],
            ['are', 'aren\'t', 'ain\'t', 'appears to be'],
            ['rich', 'real', 'riffle', 'retarded', 'rock'],
            [
                'as fuck', 'fancy', 'fucked', 'front-ended', 'falafel',
                'french fries'
            ],
        ]

        self._update_thread = None

        # setup size and remove/disable titlebuttons
        self.desktop_geom = qApp.desktop().availableGeometry()
        self.setFixedSize(self.desktop_geom.width() * .45,
                          self.desktop_geom.height() * .4)
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(),
                               qApp.desktop().availableGeometry()))
        self.setSizeGripEnabled(False)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.setModal(True)

        self._recent_list_model = QStandardItemModel(0, 2)
        self._recent_list_model.setHeaderData(0, Qt.Horizontal, 'Type')
        self._recent_list_model.setHeaderData(1, Qt.Horizontal, 'Path')

        self._recent_list = DwarfListView(self)
        self._recent_list.setModel(self._recent_list_model)

        self._recent_list.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._recent_list.header().setSectionResizeMode(1, QHeaderView.Stretch)

        # setup ui elements
        self.setup_ui()

        random.seed(a=None, version=2)

        self._base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        path_to_gitignore = os.path.join(self._base_path, os.pardir, os.pardir, '.gitignore')
        is_git_version = os.path.exists(path_to_gitignore)

        # center
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(),
                               qApp.desktop().availableGeometry()))

    def setup_ui(self):
        """ Setup Ui
        """
        main_wrap = QVBoxLayout()
        main_wrap.setContentsMargins(0, 0, 0, 0)

        # main content
        h_box = QHBoxLayout()
        h_box.setContentsMargins(0, 0, 0, 0)
        wrapper = QVBoxLayout()
        head = QHBoxLayout()
        head.setContentsMargins(30, 20, 10, 10)
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
        font = QFont('Anton', 100, QFont.Bold)
        font.setPixelSize(120)
        title.setFont(font)
        title.setMaximumHeight(125)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        title.setAlignment(Qt.AlignCenter)
        head.addWidget(title)

        sub_title_text = (
            self._pick_random_word(0) + ' ' + self._pick_random_word(1) + ' ' +
            self._pick_random_word(2) + ' ' + self._pick_random_word(3) + ' ' +
            self._pick_random_word(4))
        sub_title_text = sub_title_text[:1].upper() + sub_title_text[1:]
        self._sub_title = QLabel(sub_title_text)
        font = QFont('OpenSans', 16, QFont.Bold)
        font.setPixelSize(24)
        self._sub_title.setFont(font)
        font_metric = QFontMetrics(self._sub_title.font())
        self._char_width = font_metric.widthChar('#')
        self._sub_title.setAlignment(Qt.AlignCenter)
        self._sub_title.setContentsMargins(175, 0, 0, 20)
        self._sub_title.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Minimum)
        v_box.addLayout(head)
        v_box.addWidget(self._sub_title)

        wrapper.addLayout(v_box)

        recent = QLabel('Recent saved Sessions')
        font = recent.font()
        font.setPixelSize(14)
        font.setBold(True)
        # font.setPointSize(10)
        recent.setFont(font)
        wrapper.addWidget(recent)
        wrapper.addWidget(self._recent_list)
        h_box.addLayout(wrapper, stretch=False)
        buttonSpacer = QSpacerItem(15, 100, QSizePolicy.Fixed,
                                   QSizePolicy.Minimum)
        h_box.addItem(buttonSpacer)
        wrapper = QVBoxLayout()

        btn = QPushButton()
        ico = QIcon(QPixmap(utils.resource_path('assets/android.svg')))
        btn.setIconSize(QSize(75, 75))
        btn.setIcon(ico)
        btn.setToolTip('New Android Session')
        btn.clicked.connect(self._on_android_button)
        wrapper.addWidget(btn)

        btn = QPushButton()
        ico = QIcon(QPixmap(utils.resource_path('assets/apple.svg')))
        btn.setIconSize(QSize(75, 75))
        btn.setIcon(ico)
        btn.setToolTip('New iOS Session')
        btn.clicked.connect(self._on_ios_button)
        wrapper.addWidget(btn)

        btn = QPushButton()
        ico = QIcon(QPixmap(utils.resource_path('assets/local.svg')))
        btn.setIconSize(QSize(75, 75))
        btn.setIcon(ico)
        btn.setToolTip('New Local Session')
        btn.clicked.connect(self._on_local_button)
        wrapper.addWidget(btn)

        btn = QPushButton()
        ico = QIcon(QPixmap(utils.resource_path('assets/remote.svg')))
        btn.setIconSize(QSize(75, 75))
        btn.setIcon(ico)
        btn.setToolTip('New Remote Session')
        btn.clicked.connect(self._on_remote_button)
        wrapper.addWidget(btn)

        h_box.addLayout(wrapper, stretch=False)
        main_wrap.addLayout(h_box)
        self.setLayout(main_wrap)

    def _update_finished(self):
        self.onUpdateComplete.emit()

    def _on_android_button(self):
        self.onSessionSelected.emit('Android')
        self.close()

    def _on_local_button(self):
        self.onSessionSelected.emit('Local')
        self.close()

    def _on_ios_button(self):
        self.onSessionSelected.emit('Ios')
        self.close()

    def _on_remote_button(self):
        self.onSessionSelected.emit('Remote')
        self.close()

    def _pick_random_word(self, arr):
        return self._sub_titles[arr][random.randint(
            0,
            len(self._sub_titles[arr]) - 1)]

    def showEvent(self, QShowEvent):
        """ override to change font size when subtitle is cutted
        """
        if len(self._sub_title.text()) * self._char_width > (
                self._sub_title.width() - 155):
            font = QFont('OpenSans', 14, QFont.Bold)
            font.setPixelSize(20)
            self._sub_title.setFont(font)
        return super().showEvent(QShowEvent)
