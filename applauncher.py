import sys

from PyQt5.QtWidgets import QApplication

from applauncher import AppLauncherWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    size = app.primaryScreen().size()

    window = AppLauncherWindow(size.width(), size.height())
    with open('appLauncher.qss', 'r') as file:
        window.setStyleSheet(file.read())
    window.show()

    app.exec()
