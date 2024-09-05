from typing import List, Dict


# pylint: disable=too-few-public-methods
class Process:
    # Placeholder for a more detailed Process class
    pass


class OSCore:
    def __init__(self) -> None:
        self.processes: List[Process] = []
        self.file_system: Dict[str, str] = {}

    def execute_command(self, command: str) -> str:
        # This is a placeholder for actual command execution logic
        return f"Executed: {command}"

    def create_process(self, process: Process) -> None:
        self.processes.append(process)

    def terminate_process(self, process: Process) -> None:
        if process in self.processes:
            self.processes.remove(process)

    def write_file(self, path: str, content: str) -> None:
        self.file_system[path] = content

    def read_file(self, path: str) -> str:
        return self.file_system.get(path, "File not found")


os_instance: OSCore = OSCore()  # Single instance of the OS core
