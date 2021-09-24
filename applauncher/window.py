import sys
import os
from functools import partial

from PyQt5.QtCore import QSize, Qt, QTimer, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QSplitter,  QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QIcon, QFont

from .button import *

class AppLauncherWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()

        self.normal_button = int(height * 0.35)
        self.small_button = int(height * 0.1)

        self.setWindowTitle("App Launcher")
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.main_screen = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.statusWindow())
        layout.addWidget(self.appWindow())
        layout.addWidget(self.settingWindow())
        layout.setContentsMargins(0, 50, 0, 50)
        self.main_screen.setLayout(layout)
        self.current_row = 0
        self.last_index = 0
        # self.main_screen.setStretchFactor(1, 0.2)

        self.setCentralWidget(self.main_screen)

    def statusWindow(self):
        window = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 50)
        font = QFont('SansSerif', 30)
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignCenter)
        self.clock.setFont(font)
        layout.addWidget(self.clock)
        window.setLayout(layout)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        return window

    # method called by timer
    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm')
        self.clock.setText(label_time)

    def appWindow(self):
        scroll = QScrollArea()
        window = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(100, 0, 100, 0)

        apps = [
            ('img/youtube.png', 'firefox -kiosk www.youtube.com/tv'),
            ('img/viki.png', 'firefox -kiosk www.viki.com'),
            ('img/dummy.jpg', ''),
            ('img/dummy.jpg', ''),
            ('img/dummy.jpg', ''),
            ('img/dummy.jpg', ''),
            ('img/dummy.jpg', '')
        ]

        i = 0
        for app in apps:
            button_icon = QIcon(QPixmap(app[0]))
            button = AppButton(button_icon, '', self.normal_button)
            button.clicked.connect(partial(self.buttonClicked, 0, i, app[1]))
            layout.addWidget(button)
            i += 1

        window.setLayout(layout)
        scroll.setWidget(window)
        scroll.setAlignment(Qt.AlignVCenter)
        scroll.horizontalScrollBar().hide()
        scroll.setFixedHeight(self.normal_button + 30)
        return scroll

    def settingWindow(self):
        window = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(200, 0, 200, 0)

        apps = [
            ('img/bluetooth.png', ''),
            ('img/settings.png', ''),
            ('img/power.png', '')
        ]

        for app in apps:
            button_icon = QIcon(QPixmap(app[0]))
            button = SettingButton(button_icon, '', self.small_button)
            button.clicked.connect(partial(self.buttonClicked, 1, 0, app[1]))
            layout.addWidget(button)

        window.setLayout(layout)
        return window

    def buttonClicked(self, row, index, command):
        print(f'Clicked button {index}')
        os.system(command)
