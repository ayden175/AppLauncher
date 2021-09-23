from PyQt5.QtWidgets import QApplication, QWidget

# Only needed for access to command line arguments
import sys


class AppLauncherApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
        # Create a Qt widget, which will be our window.
        window = QWidget()
        window.show()  # IMPORTANT!!!!! Windows are hidden by default.
        print("Test")

    def exec_(self):
        self.exec()
