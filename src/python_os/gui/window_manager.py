# pylint: disable=no-name-in-module, import-error
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer


class WindowManager:
    def __init__(self):
        self.app = QApplication([])
        self.windows = {}

    def create_window(self, window_type, os_core, window_id):
        window = window_type(os_core, window_id)
        self.windows[window_id] = window
        window.closed.connect(self.close_window)
        window.show()
        return window

    def close_window(self, window_id):
        if window_id in self.windows:
            del self.windows[window_id]
        if not self.windows:
            QTimer.singleShot(0, self.app.quit)

    def get_active_windows(self):
        return list(self.windows.values())

    def run_all_windows(self):
        self.app.exec_()
