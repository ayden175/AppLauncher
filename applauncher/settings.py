import sys
import os
from functools import partial
import subprocess

from PyQt5.QtCore import QSize, Qt, QEventLoop, QPoint
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy, QFrame, qApp
from PyQt5.QtGui import QPixmap, QIcon, QFont

from .button import SettingButton, DialogButton
from .popup import PopUp
import applauncher.config as cfg

class SettingsWidget(QWidget):
    def __init__(self, width, height, keyPressEventButton):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(width/3, 0, width/3, 0)

        apps = [
            ('img/bluetooth.png', self.bluetoothMenu),
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

    def bluetoothMenu(self, button):
        pop_up = BluetoothMenu(cfg.main_window)
        pop_up.exec()
        button.setFocus()

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

class BluetoothMenu(PopUp):
    def __init__(self, parent):
        self.width = int(cfg.main_window.width / 3.5)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0,0,0,0)
        content_layout.setSpacing(0)
        out = subprocess.check_output(['bluetoothctl', 'devices']).decode().split('\n')
        #self.devices = {}
        pos = -1
        for device in out:
            if device == '': continue
            d = device.partition(' ')[2]
            mac, _, name = d.partition(' ')
            #self.devices[name] = mac

            button = DialogButton(name, self.width, 60, pos, 'ok', 'left')
            button.clicked.connect(partial(self.connect, mac))
            content_layout.addWidget(button)
            if pos < 0:
                self.focus = button
                pos = 0

        self.cancel = DialogButton('Cancel', self.width, 60, 1, 'cancel')
        self.cancel.clicked.connect(self.close)
        buttons = [self.cancel]

        super().__init__(parent, buttons, content=content_layout)
        self.focus.setFocus()

    def connect(self, mac):
        subprocess.run(['bluetoothctl', 'connect', mac])

class UpdateMenu(PopUp):
    def __init__(self, parent):
        self.title = QLabel('Do you want to search for updates?', alignment=Qt.AlignCenter)

        self.width = int(cfg.main_window.width / 3.5)
        self.cancel = DialogButton('Cancel', self.width/2, 60, -1, 'cancel')
        self.yes = DialogButton('Yes', self.width/2, 60, 1, 'ok')
        self.cancel.clicked.connect(self.close)
        self.yes.clicked.connect(self.check_updates)
        buttons = [self.cancel, self.yes]

        super().__init__(parent, buttons, text=self.title)
        self.cancel.setFocus()

    def check_updates(self):
        try:
            subprocess.run(['pamac', 'checkupdates'])
            updates = False
        except subprocess.CalledProcessError as e:
            out = e.output.decode('utf-8')
            updates = True

        if updates:
            self.title.setText(f"{out.partition(':')[0]}. Do you want to update now? The system will restart after the update.")
            self.yes.clicked.disconnect()
            self.yes.clicked.connect(self.update)
        else:
            self.title.setText('Your system is already up to date.')
            self.ok_button()

    def update(self):
        self.title.setText('Updating, please wait...')
        qApp.processEvents()
        p = subprocess.Popen(['pamac', 'update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        p.stdin.write('y'.encode())
        p.communicate()
        self.title.setText('Update successful, system will restart now.')
        if not cfg.DEV_MODE:
            self.ok_button(funct=partial(subprocess.call, ['reboot']))
        else:
            self.ok_button()

    def ok_button(self, funct=None):
        self.button_layout.removeWidget(self.cancel)
        self.cancel.deleteLater()
        self.cancel = None
        self.yes.setText('Ok')
        self.yes.setWidth(self.width)
        self.yes.setFocus()
        self.yes.clicked.disconnect()
        if funct is not None:
            self.yes.clicked.connect(funct)
        else:
            self.yes.clicked.connect(self.close)
        self.yes.pos = 2

class PowerMenu(PopUp):
    def __init__(self, parent):
        title = QLabel('Please select a shutdown option.', alignment=Qt.AlignCenter)

        width = int(cfg.main_window.width / 3.5)
        cancel = DialogButton('Cancel', width/3, 60, -1, 'cancel')
        reboot = DialogButton('Reboot', width/3, 60, 0, 'ok')
        shutdown = DialogButton('Power Off', width/3, 60, 1, 'ok')
        cancel.clicked.connect(self.close)
        reboot.clicked.connect(self.reboot)
        shutdown.clicked.connect(self.shutdown)
        buttons = [cancel, reboot, shutdown]

        super().__init__(parent, buttons, text=title)
        cancel.setFocus()

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
