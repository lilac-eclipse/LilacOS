# pylint: disable=no-name-in-module
from typing import Any

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QTextCursor, QColor, QPalette, QFontMetrics, QKeyEvent
from PyQt5.QtCore import Qt, pyqtSignal

from lilac_os.core.terminal_controller import TerminalController


class TerminalGUI(QMainWindow):
    closed = pyqtSignal(str)

    def __init__(self, terminal_controller: TerminalController, window_id: str) -> None:
        super().__init__()
        self.terminal_controller = terminal_controller
        self.window_id = window_id
        self.setWindowTitle(f"Terminal {window_id}")
        self.current_line = ""
        self.setup_ui()
        self.apply_dark_theme()

    def setup_ui(self) -> None:
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(False)
        font = QFont("Consolas", 11)
        self.terminal.setFont(font)

        layout.addWidget(self.terminal)

        self.terminal.keyPressEvent = self.handle_key_press  # type: ignore

        font_metrics = QFontMetrics(font)
        char_width = font_metrics.averageCharWidth()
        self.resize(char_width * 80, font_metrics.height() * 24)

        self.display_prompt()

    def apply_dark_theme(self) -> None:
        palette = QPalette()
        background_color = QColor(30, 30, 30)
        text_color = QColor(220, 220, 220)
        palette.setColor(QPalette.ColorRole.Base, background_color)
        palette.setColor(QPalette.ColorRole.Text, text_color)
        self.terminal.setPalette(palette)

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMainWindow::title {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 5px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: none;
            }
        """
        )

    def display_prompt(self) -> None:
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)
        self.terminal.insertPlainText(self.terminal_controller.get_prompt())

    def handle_key_press(self, event: QKeyEvent) -> None:
        cursor = self.terminal.textCursor()

        if event.key() == Qt.Key.Key_Return:
            self.process_command()
        elif event.key() == Qt.Key.Key_Backspace:
            current_prompt = self.terminal_controller.get_prompt()
            if cursor.positionInBlock() > len(current_prompt):
                QTextEdit.keyPressEvent(self.terminal, event)
        elif cursor.positionInBlock() >= len(self.terminal_controller.get_prompt()):
            QTextEdit.keyPressEvent(self.terminal, event)

    def process_command(self) -> None:
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.movePosition(
            QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor
        )
        full_line = cursor.selectedText()
        current_prompt = self.terminal_controller.get_prompt()
        command = full_line[len(current_prompt) :].strip()

        self.terminal.append("")  # Move to the next line

        result = self.terminal_controller.process_command(command)
        if result == "EXIT":
            self.close()
        else:
            self.terminal.insertPlainText(result)

        self.terminal.append("")  # Add a blank line for better readability
        self.display_prompt()

    def close_event(self, event: Any) -> None:
        self.closed.emit(self.window_id)
        super().closeEvent(event)
