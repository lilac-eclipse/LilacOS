from typing import Dict, Tuple, Union, Optional
from typing import TYPE_CHECKING
from .memory import PageTable

if TYPE_CHECKING:
    from .os_core import OSCore


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
        # pylint: disable=R0911 (too-many-return-statements)
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
            var_name, size_str = parts[1], parts[2]
            try:
                size = int(size_str)
            except ValueError:
                return f"Invalid size: {size_str}. Please provide an integer."
            self.current_program.allocate_variable(var_name, size)
            return f"Variable '{var_name}' allocated with size {size}"

        if parts[0] == "set":
            if len(parts) < 3:
                return "Usage: set <variable_name> <value>"
            var_name, value_str = parts[1], " ".join(parts[2:])
            try:
                value: Union[int, str] = int(value_str)
            except ValueError:
                value = value_str
            self.current_program.set_variable(var_name, value)
            return f"Variable '{var_name}' set to {value}"

        if parts[0] == "get":
            if len(parts) != 2:
                return "Usage: get <variable_name>"
            var_name = parts[1]
            value = self.current_program.get_variable(var_name)
            return f"Value of '{var_name}': {value}"

        return f"Unknown command: {command}"
