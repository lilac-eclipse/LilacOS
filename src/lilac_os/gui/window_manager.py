# pylint: disable=no-name-in-module, import-error
from typing import Dict, List, Any, Callable
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from lilac_os.core.os_core import OSCore


class WindowManager:
    def __init__(self) -> None:
        self.app: QApplication = QApplication([])
        self.windows: Dict[str, QMainWindow] = {}

    def create_window(
        self,
        window_class: Callable[[Any, str], QMainWindow],
        os_core: OSCore,
        window_id: str,
    ) -> QMainWindow:

        window = window_class(os_core, window_id)
        self.windows[window_id] = window
        window.closed.connect(lambda: self.close_window(window_id))
        window.show()
        return window

    def close_window(self, window_id: str) -> None:
        if window_id in self.windows:
            del self.windows[window_id]
        if not self.windows:
            QTimer.singleShot(0, self.app.quit)

    def get_active_windows(self) -> List[QMainWindow]:
        return list(self.windows.values())

    def run_all_windows(self) -> None:
        self.app.exec_()
