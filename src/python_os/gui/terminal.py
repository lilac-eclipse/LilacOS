# pylint: disable=no-name-in-module, import-error
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QTextCursor, QColor, QPalette, QFontMetrics
from PyQt5.QtCore import Qt, pyqtSignal


class TerminalGUI(QMainWindow):
    closed = pyqtSignal(str)

    def __init__(self, os_core, window_id):
        super().__init__()
        self.os_core = os_core
        self.window_id = window_id
        self.setWindowTitle(f"Terminal {window_id}")
        self.current_line = ""
        self.prompt = f"user@terminal{window_id}:~$ "
        self.setup_ui()
        self.apply_dark_theme()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(False)
        font = QFont("Consolas", 11)
        self.terminal.setFont(font)

        layout.addWidget(self.terminal)

        self.terminal.keyPressEvent = self.handle_key_press

        # Set a more appropriate size based on character width
        font_metrics = QFontMetrics(font)
        char_width = font_metrics.averageCharWidth()
        self.resize(char_width * 80, font_metrics.height() * 24)  # 80 columns, 24 rows

        self.display_prompt()

    def apply_dark_theme(self):
        # Dark theme for the terminal
        palette = QPalette()
        background_color = QColor(30, 30, 30)
        text_color = QColor(220, 220, 220)
        palette.setColor(QPalette.Base, background_color)
        palette.setColor(QPalette.Text, text_color)
        self.terminal.setPalette(palette)

        # Dark theme for the window and title bar
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

    def display_prompt(self):
        self.terminal.moveCursor(QTextCursor.End)
        self.terminal.insertPlainText(self.prompt)

    def handle_key_press(self, event):
        cursor = self.terminal.textCursor()

        if event.key() == Qt.Key_Return:
            self.process_command()
        elif event.key() == Qt.Key_Backspace:
            if cursor.positionInBlock() > len(self.prompt):
                QTextEdit.keyPressEvent(self.terminal, event)
        elif cursor.positionInBlock() >= len(self.prompt):
            QTextEdit.keyPressEvent(self.terminal, event)

    def process_command(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        full_line = cursor.selectedText()
        command = full_line[len(self.prompt) :].strip()

        self.terminal.append("")  # Move to the next line
        self.terminal.insertPlainText(f"You entered: {command}")
        self.terminal.append("")  # Add a blank line for better readability

        if command.lower() == "exit":
            self.close()

        self.display_prompt()

    # pylint: disable=invalid-name
    def closeEvent(self, event):
        self.closed.emit(self.window_id)
        super().closeEvent(event)
