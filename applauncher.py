import sys

from PyQt5.QtWidgets import QApplication

from applauncher import AppLauncherWindow
import applauncher.config as cfg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    size = app.primaryScreen().size()

    cfg.main_window = AppLauncherWindow(size.width(), size.height())
    with open('appLauncher.qss', 'r') as file:
        cfg.main_window.setStyleSheet(file.read())
    cfg.main_window.show()

    app.exec()
