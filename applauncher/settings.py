import sys
import os
from functools import partial
import subprocess

from PyQt5.QtCore import QSize, Qt, QEventLoop, QPoint
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy, QFrame
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
            ('img/update.png', self.updateMenu),
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

    def doNothing(self, button):
        print('Not implemented yet!')

    def updateMenu(self, button):
        pop_up = UpdateMenu(cfg.main_window)
        pop_up.exec()
        button.setFocus()

    def powerMenu(self, button):
        pop_up = PowerMenu(cfg.main_window)
        pop_up.exec()
        button.setFocus()

    def getButtons(self):
        return self.buttons

class PopUp(QWidget):
    def __init__(self, parent, text, buttons):
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
        text_container = QWidget()
        text_container.setFixedWidth(width)
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(35,35,35,30)
        text.setWordWrap(True)
        font = QFont('SansSerif', 20)
        text.setFont(font)
        text_layout.addWidget(text)
        layout.addWidget(text_container)

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

class UpdateMenu(PopUp):
    def __init__(self, parent):
        self.title = QLabel('Do you want to search for updates?', alignment=Qt.AlignCenter)

        self.width = int(cfg.main_window.width / 3.5)
        self.cancel = DialogButton('Cancel', self.width/2, 60, -1)
        self.yes = DialogButton('Yes', self.width/2, 60, 1)
        self.cancel.clicked.connect(self.close)
        self.yes.clicked.connect(self.check_updates)
        buttons = [self.cancel, self.yes]

        super().__init__(parent, self.title, buttons)
        self.cancel.setFocus()

    def check_updates(self):
        try:
            subprocess.check_output(['pamac', 'checkupdates'])
            updates = False
        except subprocess.CalledProcessError as e:
            out = e.output.decode('utf-8')
            updates = True

        if updates:
            self.title.setText(f"{out.partition(':')[0]}. Do you want to update now? The system will restart after the update.")
            self.yes.clicked.connect(self.update)
        else:
            self.title.setText('Your system is already up to date.')
            self.ok_button()

    def update(self):
        self.title.setText('Updating, please wait...')
        subprocess.call(['pamac', 'update'])
        self.title.setText('Update successful, system will restart now.')
        if not cfg.DEV_MODE:
            self.ok_button(funct=partial.functools(subprocess.call, ['reboot']))
        else:
            self.ok_button()

    def close(self):
        self.loop.quit()

    def ok_button(self, funct=None):
        self.button_layout.removeWidget(self.yes)
        self.yes.deleteLater()
        self.yes = None
        self.cancel.setText('Ok')
        self.cancel.setWidth(self.width)
        self.cancel.setFocus()
        if funct is not None:
            self.canclel.clicked.connect(funct)

class PowerMenu(PopUp):
    def __init__(self, parent):
        title = QLabel('Please select a shutdown option.', alignment=Qt.AlignCenter)

        width = int(cfg.main_window.width / 3.5)
        cancel = DialogButton('Cancel', width/3, 60, -1)
        reboot = DialogButton('Reboot', width/3, 60, 0)
        shutdown = DialogButton('Power Off', width/3, 60, 1)
        cancel.clicked.connect(self.close)
        reboot.clicked.connect(self.reboot)
        shutdown.clicked.connect(self.shutdown)
        buttons = [cancel, reboot, shutdown]

        super().__init__(parent, title, buttons)
        cancel.setFocus()

    def close(self):
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
