import sys
import os
from functools import partial
import subprocess

from PyQt5.QtCore import QSize, Qt, QEventLoop, QPoint
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy, QFrame, qApp
from PyQt5.QtGui import QPixmap, QIcon, QFont

from .button import SettingButton, DialogButton
import applauncher.config as cfg

class PopUp(QWidget):
    def __init__(self, parent, buttons, text=None, content=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAutoFillBackground(True)

        # create container for pop up
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.container = QWidget(autoFillBackground=True, objectName='container')
        layout.addWidget(self.container, alignment=Qt.AlignCenter)
        self.container.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # create layout for content
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0,0,0,0)
        width = int(cfg.main_window.width / 3.5)

        # create text
        main_container = QWidget()
        main_container.setFixedWidth(width)
        if content is None and not text is None:
            main_layout = QVBoxLayout(main_container)
            main_layout.setContentsMargins(35,35,35,30)
            text.setWordWrap(True)
            font = QFont('SansSerif', 20)
            text.setFont(font)
            main_layout.addWidget(text)
        elif text is None and not content is None:
            main_container.setLayout(content)
        layout.addWidget(main_container)

        # create button layout and add buttons
        button_box = QWidget()
        self.button_layout = QHBoxLayout(button_box)
        self.button_layout.setContentsMargins(0,0,0,0)
        self.button_layout.setSpacing(0)
        for button in buttons:
            self.button_layout.addWidget(button)
        layout.addWidget(button_box)

        self.loop = QEventLoop(self)

    def showEvent(self, event):
        self.setGeometry(self.parent().rect())

    def exec(self):
        self.show()
        self.raise_()
        self.loop.exec_()
        self.hide()

    def close(self):
        self.loop.quit()
