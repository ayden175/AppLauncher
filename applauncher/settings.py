import sys
import os
from functools import partial

from PyQt5.QtCore import QSize, Qt, QEventLoop, QPoint
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QFont

from .button import SettingButton, DialogButton
import applauncher.config as cfg

class SettingsWidget(QWidget):
    def __init__(self, width, height, keyPressEventButton):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(width/3, 0, width/3, 0)

        apps = [
            ('img/bluetooth.png', self.doNothing),
            ('img/settings.png', self.doNothing),
            ('img/power.png', self.powerMenu)
        ]

        self.buttons = []
        i = 0
        for app in apps:
            button_icon = QIcon(QPixmap(app[0]))
            button = SettingButton(button_icon, '', int(height * 0.08), i, keyPressEventButton)
            button.clicked.connect(partial(app[1], button))
            self.buttons.append(button)
            layout.addWidget(button)
            i += 1

    def doNothing(self):
        print('Not implemented yet!')

    def powerMenu(self, button):
        pop_up = PowerMenu(cfg.main_window)
        pop_up.exec()
        button.setFocus()

    def getButtons(self):
        return self.buttons

class PopUp(QWidget):
    def __init__(self, parent, content):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.container = QWidget(autoFillBackground=True, objectName='container')
        layout.addWidget(self.container, alignment=Qt.AlignCenter)
        self.container.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.container.setLayout(content)
        self.loop = QEventLoop(self)

    def showEvent(self, event):
        self.setGeometry(self.parent().rect())

    def exec(self):
        self.show()
        self.raise_()
        self.loop.exec_()
        self.hide()

class PowerMenu(PopUp):
    def __init__(self, parent):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,35,0,0)
        layout.setSpacing(30)

        title = QLabel('Select a shutdown option', alignment=Qt.AlignCenter)
        font = QFont('SansSerif', 20)
        title.setFont(font)

        button_box = QWidget()
        button_layout = QHBoxLayout(button_box)
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setSpacing(0)
        cancel = DialogButton('Cancel', -1)
        reboot = DialogButton('Reboot', 0)
        shutdown = DialogButton('Power Off', 1)
        cancel.clicked.connect(self.cancel)
        reboot.clicked.connect(self.reboot)
        shutdown.clicked.connect(self.shutdown)
        button_layout.addWidget(cancel)
        button_layout.addWidget(reboot)
        button_layout.addWidget(shutdown)

        layout.addWidget(title)
        layout.addWidget(button_box)

        super().__init__(parent, layout)

        cancel.setFocus()

    def cancel(self):
        self.loop.quit()

    def reboot(self):
        if not cfg.DEV_MODE:
            os.system('reboot')
        else:
            print('triggered: reboot')
            self.loop.quit()

    def shutdown(self):
        if not cfg.DEV_MODE:
            os.system('shutdown now')
        else:
            print('triggered: shutdown now')
            self.loop.quit()
