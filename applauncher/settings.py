import sys
import os
import select
from functools import partial
import subprocess

from PyQt5.QtCore import QSize, Qt, QEventLoop, QPoint
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSizePolicy, QFrame, qApp, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap, QIcon, QFont

from .button import SettingButton, DialogButton, WrappedLabel
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

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        scroll = QScrollArea()
        window = QWidget(autoFillBackground=True, objectName='container')
        content_layout = QVBoxLayout(window)
        content_layout.setContentsMargins(0,0,0,0)
        content_layout.setSpacing(0)

        out = subprocess.check_output(['bluetoothctl', 'devices']).decode().split('\n')
        font = QFont('SansSerif', 18)
        content_layout.addWidget(WrappedLabel('Paired devices', font=font))
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        content_layout.addWidget(line)
        paired = QWidget()
        self.paired_layout = QVBoxLayout(paired)
        self.paired_layout.setContentsMargins(0,0,0,0)
        self.paired_layout.setSpacing(0)
        pos = -1
        for device in out:
            if device == '': continue
            d = device.partition(' ')[2]
            mac, _, name = d.partition(' ')

            button = DialogButton(name, self.width, 60, pos, 'ok', 'left')
            button.clicked.connect(partial(self.connect, mac))
            self.paired_layout.addWidget(button)
            if pos < 0:
                self.focus = button
                pos = 0
        content_layout.addWidget(paired)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        content_layout.addWidget(line)
        #content_layout.addWidget(WrappedLabel('Available devices', font=font))

        #timer = QTimer(self)
        #timer.timeout.connect(self.scanDevices)
        #timer.start(1000)

        scroll.setWidget(window)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll)

        self.cancel = DialogButton('Cancel', self.width, 60, 1, 'cancel')
        self.cancel.clicked.connect(self.close)
        buttons = [self.cancel]

        super().__init__(parent, buttons, content=layout)
        self.focus.setFocus()

    def connect(self, mac):
        subprocess.run(['bluetoothctl', 'connect', mac])

    # TODO: fix me! Does not print lines as received by the running process
    def scanDevices(self):
        p = subprocess.Popen(['bluetoothctl', 'scan', 'on'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
        for line in iter(p.stdout.readline,''):
           print(line.rstrip())

        # https://unix.stackexchange.com/questions/551514/list-nearby-bluetooth-devices-on-raspberry-pi

        # bluetoothctl scan on

        # sudo tshark -i bluetooth0 -Y "(bthci_evt.code == 0x2f) || (bthci_evt.le_meta_subevent == 0x2 && btcommon.eir_ad.entry.device_name != '')" -T fields -e bthci_evt.bd_addr -e btcommon.eir_ad.entry.device_name


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
