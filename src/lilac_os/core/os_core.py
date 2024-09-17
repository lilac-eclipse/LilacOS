# os_core.py
from typing import Dict, Optional
from lilac_os.gui.memory_viewer import MemoryViewer
from .hardware_abstraction import HardwareAbstractionLayer
from .process import Process, ProgramManager
from .memory import MemoryManager


class OSCore:
    def __init__(self, hal: HardwareAbstractionLayer) -> None:
        self.hal: HardwareAbstractionLayer = hal
        self.processes: Dict[int, Process] = {}
        self.next_pid: int = 1
        self.memory_manager: MemoryManager = MemoryManager(self)
        self.program_manager: ProgramManager = ProgramManager(self)
        self.memory_viewer: Optional[MemoryViewer] = None

    def set_memory_viewer(self, memory_viewer: MemoryViewer) -> None:
        self.memory_viewer = memory_viewer

    def create_process(self) -> Process:
        pid = self.next_pid
        self.next_pid += 1
        process = Process(pid, self)
        self.processes[pid] = process
        return process

    def malloc(self, pid: int, size: int) -> int:
        return self.memory_manager.malloc(pid, size)

    def free(self, pid: int, address: int) -> None:
        self.memory_manager.free(pid, address)

    def read_memory(self, pid: int, address: int) -> int:
        return self.memory_manager.read_memory(pid, address)

    def write_memory(self, pid: int, address: int, value: int) -> None:
        self.memory_manager.write_memory(pid, address, value)

    def translate_address(self, pid: int, virtual_address: int) -> int:
        return self.memory_manager.translate_address(pid, virtual_address)

    def handle_page_fault(self, pid: int, virtual_address: int) -> int:
        return self.memory_manager.handle_page_fault(pid, virtual_address)

    def set_virtual_memory_enabled(self, enabled: bool) -> None:
        self.memory_manager.set_virtual_memory_enabled(enabled)

    def execute_command(self, command: str) -> str:
        return self.program_manager.execute_command(command)
