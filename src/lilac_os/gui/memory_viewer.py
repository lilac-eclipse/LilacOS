# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QTabWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from lilac_os.core.hardware import SimulatedHardware, MEMORY_SIZE, DISK_SIZE


class MemoryViewer(QWidget):
    def __init__(self, hardware: SimulatedHardware) -> None:
        super().__init__()
        self.hardware = hardware
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.memory_view = QTextEdit()
        self.disk_view = QTextEdit()

        for view in [self.memory_view, self.disk_view]:
            view.setFont(QFont("Courier", 10))
            view.setReadOnly(True)

        self.tab_widget.addTab(self.memory_view, "Memory")
        self.tab_widget.addTab(self.disk_view, "Disk")

        self.setWindowTitle("Memory Viewer")
        self.resize(1000, 800)

    def update_memory_view(self) -> None:
        content = ""
        for i in range(0, MEMORY_SIZE, 16):
            line = f"{i:04X}: "
            hex_values = " ".join(
                [f"{self.hardware.memory.read_byte(j):02X}" for j in range(i, i + 16)]
            )
            ascii_values = "".join(
                [
                    (
                        chr(self.hardware.memory.read_byte(j))
                        if 32 <= self.hardware.memory.read_byte(j) < 127
                        else "."
                    )
                    for j in range(i, i + 16)
                ]
            )
            content += f"{line}{hex_values}  {ascii_values}\n"
        self.memory_view.setText(content)

    def update_disk_view(self) -> None:
        content = ""
        for block in range(DISK_SIZE // 16):
            data = self.hardware.disk.read_block(block)
            line = f"{block*16:04X}: "
            hex_values = " ".join([f"{b:02X}" for b in data])
            ascii_values = "".join([chr(b) if 32 <= b < 127 else "." for b in data])
            content += f"{line}{hex_values}  {ascii_values}\n"
        self.disk_view.setText(content)

    def update(self) -> None:
        self.update_memory_view()
        self.update_disk_view()
