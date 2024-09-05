from typing import Dict, List, Tuple, Optional, Union
from .hardware_abstraction import HardwareAbstractionLayer
from lilac_os.gui.memory_viewer import MemoryViewer

PAGE_SIZE: int = 16  # bytes
TOTAL_PAGES: int = 16  # 256 bytes total memory


class PageTableEntry:
    def __init__(self) -> None:
        self.physical_page: Optional[int] = None
        self.present: bool = False
        self.dirty: bool = False


class PageTable:
    def __init__(self) -> None:
        self.entries: Dict[int, PageTableEntry] = {}

    def get_entry(self, virtual_page_number: int) -> PageTableEntry:
        if virtual_page_number not in self.entries:
            self.entries[virtual_page_number] = PageTableEntry()
        return self.entries[virtual_page_number]


class Process:
    def __init__(self, pid: int, os_core: "OSCore") -> None:
        self.pid: int = pid
        self.os_core: "OSCore" = os_core
        self.page_table: PageTable = PageTable()
        self.memory_regions: Dict[int, int] = {}  # start_address -> size

    def malloc(self, size: int) -> int:
        return self.os_core.malloc(self.pid, size)

    def free(self, address: int) -> None:
        self.os_core.free(self.pid, address)

    def read_memory(self, address: int) -> int:
        return self.os_core.read_memory(self.pid, address)

    def write_memory(self, address: int, value: int) -> None:
        self.os_core.write_memory(self.pid, address, value)


class Program:
    def __init__(self, name: str, process: Process) -> None:
        self.name: str = name
        self.process: Process = process
        self.variables: Dict[str, Tuple[int, int]] = {}  # name -> (address, size)

    def allocate_variable(self, name: str, size: int) -> None:
        address = self.process.malloc(size)
        self.variables[name] = (address, size)

    def set_variable(self, name: str, value: Union[int, str]) -> None:
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not allocated")
        address, size = self.variables[name]
        if isinstance(value, int):
            self.process.write_memory(address, value)
        elif isinstance(value, str):
            for i, char in enumerate(value[:size]):
                self.process.write_memory(address + i, ord(char))

    def get_variable(self, name: str) -> Union[int, str]:
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not allocated")
        address, size = self.variables[name]
        values = [self.process.read_memory(address + i) for i in range(size)]
        if size == 1:
            return values[0]
        return "".join(chr(v) for v in values if v != 0)


class ProgramManager:
    def __init__(self, os_core: "OSCore") -> None:
        self.os_core: "OSCore" = os_core
        self.programs: Dict[str, Program] = {}
        self.current_program: Optional[Program] = None

    def create_program(self, name: str) -> Program:
        process = self.os_core.create_process()
        program = Program(name, process)
        self.programs[name] = program
        return program

    def set_current_program(self, name: str) -> None:
        if name in self.programs:
            self.current_program = self.programs[name]
        else:
            raise ValueError(f"Program '{name}' does not exist")

    def execute_command(self, command: str) -> str:
        parts = command.split()
        if not parts:
            return ""

        if parts[0] == "create_program":
            if len(parts) != 2:
                return "Usage: create_program <program_name>"
            program_name = parts[1]
            self.create_program(program_name)
            self.set_current_program(program_name)
            return f"Program '{program_name}' created and set as current program"

        if not self.current_program:
            return "No active program. Use 'create_program <name>' first."

        if parts[0] == "allocate":
            if len(parts) != 3:
                return "Usage: allocate <variable_name> <size>"
            var_name, size = parts[1], int(parts[2])
            self.current_program.allocate_variable(var_name, size)
            return f"Variable '{var_name}' allocated with size {size}"

        if parts[0] == "set":
            if len(parts) < 3:
                return "Usage: set <variable_name> <value>"
            var_name, value = parts[1], " ".join(parts[2:])
            try:
                value = int(value)
            except ValueError:
                pass
            self.current_program.set_variable(var_name, value)
            return f"Variable '{var_name}' set to {value}"

        if parts[0] == "get":
            if len(parts) != 2:
                return "Usage: get <variable_name>"
            var_name = parts[1]
            value = self.current_program.get_variable(var_name)
            return f"Value of '{var_name}': {value}"

        return f"Unknown command: {command}"


class OSCore:
    def __init__(self, hal: HardwareAbstractionLayer) -> None:
        self.hal: HardwareAbstractionLayer = hal
        self.processes: Dict[int, Process] = {}
        self.next_pid: int = 1
        self.free_pages: List[int] = list(range(TOTAL_PAGES))
        self.page_queue: List[Tuple[int, int, int]] = []  # (pid, vpn, ppn)
        self.virtual_memory_enabled: bool = False
        self.memory_viewer: Optional[MemoryViewer] = None
        self.program_manager: ProgramManager = ProgramManager(self)

    def set_memory_viewer(self, memory_viewer: MemoryViewer) -> None:
        self.memory_viewer = memory_viewer

    def create_process(self) -> Process:
        pid = self.next_pid
        self.next_pid += 1
        process = Process(pid, self)
        self.processes[pid] = process
        return process

    def malloc(self, pid: int, size: int) -> int:
        process = self.processes[pid]
        pages_needed = (size + PAGE_SIZE - 1) // PAGE_SIZE
        start_page = len(process.memory_regions)
        for i in range(pages_needed):
            process.memory_regions[start_page + i] = PAGE_SIZE
        return start_page * PAGE_SIZE

    def free(self, pid: int, address: int) -> None:
        process = self.processes[pid]
        page = address // PAGE_SIZE
        if page in process.memory_regions:
            del process.memory_regions[page]
            if self.virtual_memory_enabled:
                entry = process.page_table.get_entry(page)
                if entry.present and entry.physical_page is not None:
                    self.free_pages.append(entry.physical_page)
                    entry.present = False

    def read_memory(self, pid: int, address: int) -> int:
        physical_address = self.translate_address(pid, address)
        return self.hal.read_memory(physical_address)

    def write_memory(self, pid: int, address: int, value: int) -> None:
        physical_address = self.translate_address(pid, address)
        self.hal.write_memory(physical_address, value)
        if self.virtual_memory_enabled:
            process = self.processes[pid]
            virtual_page = address // PAGE_SIZE
            page_table_entry = process.page_table.get_entry(virtual_page)
            page_table_entry.dirty = True
        if self.memory_viewer:
            self.memory_viewer.update()

    def translate_address(self, pid: int, virtual_address: int) -> int:
        if not self.virtual_memory_enabled:
            return virtual_address

        process = self.processes[pid]
        virtual_page = virtual_address // PAGE_SIZE
        offset = virtual_address % PAGE_SIZE

        page_table_entry = process.page_table.get_entry(virtual_page)
        if not page_table_entry.present:
            physical_page = self.handle_page_fault(pid, virtual_address)
        else:
            physical_page = page_table_entry.physical_page

        if physical_page is None:
            raise ValueError("Physical page is None after translation")

        return (physical_page * PAGE_SIZE) + offset

    def handle_page_fault(self, pid: int, virtual_address: int) -> int:
        process = self.processes[pid]
        virtual_page = virtual_address // PAGE_SIZE

        if not self.free_pages:
            evicted_page = self.evict_page()
            self.free_pages.append(evicted_page)

        physical_page = self.free_pages.pop(0)
        self.page_queue.append((pid, virtual_page, physical_page))

        page_table_entry = process.page_table.get_entry(virtual_page)
        page_table_entry.physical_page = physical_page
        page_table_entry.present = True
        page_table_entry.dirty = False

        return physical_page

    def evict_page(self) -> int:
        evicted_pid, evicted_virtual_page, evicted_physical_page = self.page_queue.pop(
            0
        )
        evicted_process = self.processes[evicted_pid]
        evicted_entry = evicted_process.page_table.get_entry(evicted_virtual_page)

        if evicted_entry.dirty:
            # Write dirty page to disk (not implemented in this simplified version)
            pass

        evicted_entry.present = False
        evicted_entry.dirty = False
        return evicted_physical_page

    def set_virtual_memory_enabled(self, enabled: bool) -> None:
        self.virtual_memory_enabled = enabled
        print(f"Virtual Memory {'Enabled' if enabled else 'Disabled'}")

    def execute_command(self, command: str) -> str:
        return self.program_manager.execute_command(command)
