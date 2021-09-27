from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QFont

import applauncher.config as cfg

class IconButton(QPushButton):
    def __init__(self, icon, text, size, offset, row, index, keyPressFunc):
        super().__init__(icon, '')

        self.setIconSize(QSize(size - offset, size - offset))
        self.setFixedSize(QSize(size, size))
        self.row = row
        self.index = index
        self.keyPressFunc = keyPressFunc

    def enterEvent(self, event):
        self.setFocus()
        # TODO: prevent super fast scrolling or just disable?
        cfg.main_window.ensureButtonVisible(self)

    def keyPressEvent(self, event):
        if event.key() ==  Qt.Key_Space:
            super().keyPressEvent(event)
        else:
            self.keyPressFunc(event, self.row, self.index)

class AppButton(IconButton):
    def __init__(self, icon, text, size, index, keyPressFunc):
        super().__init__(icon, text, size, 18, 0, index, keyPressFunc)

class SettingButton(IconButton):
    def __init__(self, icon, text, size, index, keyPressFunc):
        super().__init__(icon, text, size, 10, 1, index, keyPressFunc)
        self.setStyleSheet(f"border-radius: {int(size/2)};")

class DialogButton(QPushButton):
    def __init__(self, text, width, height, pos):
        super().__init__(text)
        self.setFixedSize(QSize(width, height))
        font = QFont('SansSerif', 16)
        self.setFont(font)
        # pos: -1 left most, 1 right most, 0 otherwise
        self.pos = pos
        self.height = height

    def setWidth(self, width):
        self.setFixedSize(QSize(width, self.height))

    def keyPressEvent(self, event):
        if (event.key() ==  Qt.Key_Space or
            event.key() == Qt.Key_Left and self.pos != -1 or
            event.key() == Qt.Key_Right and self.pos != 1):
            super().keyPressEvent(event)
