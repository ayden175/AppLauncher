import sys
import os
from functools import partial

from PyQt5.QtCore import QSize, Qt, QTimer, QTime, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QSplitter,  QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QIcon, QFont

from .button import *
from .settings import SettingsWidget

class AppLauncherWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.normal_button = int(height * 0.35)
        self.buttons = 2 * [None]

        self.setWindowTitle("App Launcher")
        self.showMaximized()
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.main_screen = QWidget()
        layout = QVBoxLayout(self.main_screen)
        layout.addWidget(self.statusWindow())
        layout.addWidget(self.appWindow())
        settingsWidget = SettingsWidget(width, height, self.keyPressEventButton)
        layout.addWidget(settingsWidget)
        layout.setContentsMargins(0, 50, 0, 50)

        self.current_row = 0
        self.last_index = 0

        self.setCentralWidget(self.main_screen)
        self.buttons[1] = settingsWidget.getButtons()
        self.buttons[0][0].setFocus()

    def keyPressEventButton(self, event, row, index):
        key = event.key()

        if key == Qt.Key_Left and index > 0:
            new_button = self.buttons[row][index-1]
            new_button.setFocus()
            self.ensureButtonVisible(new_button)

        elif key == Qt.Key_Right and index < len(self.buttons[row]) - 1:
            new_button = self.buttons[row][index+1]
            new_button.setFocus()
            self.ensureButtonVisible(new_button)

        elif key == Qt.Key_Up and row == 1:
            self.buttons[row-1][self.last_index].setFocus()
            self.last_index = index

        elif key == Qt.Key_Down and row == 0:
            self.buttons[row+1][self.last_index].setFocus()
            self.last_index = index

    def ensureButtonVisible(self, button):
        pos = button.mapToGlobal(QPoint(0, 0)).x()
        scroll_bar = self.scroll.horizontalScrollBar()
        if pos < 0:
            scroll_bar.setValue(scroll_bar.value() - (self.normal_button + 6))
        elif pos + self.normal_button > self.width:
            scroll_bar.setValue(scroll_bar.value() + (self.normal_button + 6))

    def statusWindow(self):
        window = QWidget()
        layout = QVBoxLayout(window)
        layout.setContentsMargins(0, 0, 0, 50)
        font = QFont('SansSerif', 50)
        self.clock = QLabel()
        self.clock.setStyleSheet("color: rgb(240, 240, 240);")
        self.clock.setAlignment(Qt.AlignCenter)
        self.clock.setFont(font)
        layout.addWidget(self.clock)
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
        layout = QHBoxLayout(window)
        layout.setContentsMargins(self.normal_button/1.92, 0, self.normal_button/1.92, 0)

        apps = [
            ('img/youtube.png', 'YouTube', 'firefox -kiosk www.youtube.com/tv'),
            ('img/viki.png', 'Viki', 'firefox -kiosk www.viki.com'),
            ('img/dummy.jpg', 'Empty', ''),
            ('img/dummy.jpg', 'Empty', ''),
            ('img/dummy.jpg', 'Empty', ''),
            ('img/dummy.jpg', 'Empty', '')
        ]

        self.buttons[0] = []
        i = 0
        for app in apps:
            image, title, command = app
            button_icon = QIcon(QPixmap(image))
            button = AppButton(button_icon, title, self.normal_button, i, self.keyPressEventButton)
            button.clicked.connect(partial(self.buttonClicked, 0, i, command))
            self.buttons[0].append(button)
            layout.addWidget(button)
            i += 1

        scroll.setWidget(window)
        scroll.setAlignment(Qt.AlignVCenter)
        scroll.horizontalScrollBar().hide()
        scroll.setFixedHeight(self.normal_button + 30)
        self.scroll = scroll
        return scroll

    def buttonClicked(self, row, index, command):
        print(f'Clicked button {index}')
        os.system(command)
