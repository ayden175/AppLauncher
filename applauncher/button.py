from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon


class AppButton(QPushButton):
    def __init__(self, icon, text, size):
        super().__init__(icon, '')

        self.setIconSize(QSize(size - 18, size - 18))
        self.setFixedSize(QSize(size, size))

class SettingButton(QPushButton):
    def __init__(self, icon, text, size):
        super().__init__(icon, '')

        self.setIconSize(QSize(size - 10, size - 10))
        self.setFixedSize(QSize(size, size))
        #bababa hex code icon
        self.setStyleSheet(f"border-radius: {int(size/2)};")
