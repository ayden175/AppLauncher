from playsound import playsound

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont

import applauncher.config as cfg

class IconButton(QPushButton):
    def __init__(self, icon, text, size, offset, row, index, sound, keyPressFunc):
        super().__init__(icon, '')

        self.setIconSize(QSize(size - offset, size - offset))
        self.setFixedSize(QSize(size, size))
        self.row = row
        self.index = index
        self.sound = sound
        self.keyPressFunc = keyPressFunc

    def enterEvent(self, event):
        self.setFocus()
        # TODO: prevent super fast scrolling or just disable?
        cfg.main_window.ensureButtonVisible(self)

    def keyPressEvent(self, event):
        if event.key() ==  Qt.Key_Space:
            #playsound('sounds/'+self.sound+'.mp3')
            print('Press 1')
            super().keyPressEvent(event)
            print('Press 2')
        elif (event.key() == Qt.Key_Left or event.key() == Qt.Key_Right or
              event.key() == Qt.Key_Up   or event.key() == Qt.Key_Down):
            #playsound('sounds/switch.mp3')
            self.keyPressFunc(event, self.row, self.index)

class AppButton(IconButton):
    def __init__(self, icon, text, size, index, keyPressFunc):
        super().__init__(icon, text, size, 18, 0, index, 'start', keyPressFunc)

class SettingButton(IconButton):
    def __init__(self, icon, text, size, index, keyPressFunc):
        super().__init__(icon, text, size, 10, 1, index, 'ok', keyPressFunc)
        self.setStyleSheet(f"border-radius: {int(size/2)};")

class DialogButton(QPushButton):
    def __init__(self, text, width, height, pos, sound, align='center'):
        super().__init__(text)
        self.setFixedSize(QSize(width, height))
        font = QFont('SansSerif', 16)
        self.setFont(font)
        # pos: -1 left most, 1 right most, 0 otherwise, 2 can't move at all
        self.pos = pos
        self.height = height
        self.sound = sound
        self.setStyleSheet("QPushButton { text-align: "+align+"; }")

    def setWidth(self, width):
        self.setFixedSize(QSize(width, self.height))

    def keyPressEvent(self, event):
        #if event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
            #playsound('sounds/switch.mp3')
        #elif event.key() == Qt.Key_Space:
            #playsound('sounds/'+self.sound+'.mp3')

        if (event.key() == Qt.Key_Space or self.pos != 2 and
            (event.key() == Qt.Key_Left  and self.pos != -1 or
            event.key() == Qt.Key_Right and self.pos != 1)):
            super().keyPressEvent(event)

class WrappedLabel(QWidget):
    def __init__(self, text='', font=None):
        super().__init__()
        wrapped_label = QLabel(text, font=font)
        wrapped_layout = QVBoxLayout(self)
        wrapped_layout.addWidget(wrapped_label)
        self.setStyleSheet('QWidget { padding-top: 15px; padding-left: 10px; padding-bottom: 5px; }')
