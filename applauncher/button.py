from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon

class IconButton(QPushButton):
    def __init__(self, icon, text, size, offset, row, index, keyPressFunc):
        super().__init__(icon, '')

        self.setIconSize(QSize(size - offset, size - offset))
        self.setFixedSize(QSize(size, size))
        self.row = row
        self.index = index
        self.keyPressFunc = keyPressFunc

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
