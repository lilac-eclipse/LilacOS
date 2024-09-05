class OSCore:
    def __init__(self):
        self.processes = []
        self.file_system = {}

    def execute_command(self, command):
        # This is a placeholder for actual command execution logic
        return f"Executed: {command}"

    def create_process(self, process):
        self.processes.append(process)

    def terminate_process(self, process):
        if process in self.processes:
            self.processes.remove(process)

    def write_file(self, path, content):
        self.file_system[path] = content

    def read_file(self, path):
        return self.file_system.get(path, "File not found")


os_instance = OSCore()  # Single instance of the OS core
