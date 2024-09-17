from typing import Optional
from lilac_os.core.os_core import OSCore


class TerminalController:
    def __init__(self, os_core: OSCore) -> None:
        self.os_core: OSCore = os_core
        self.interpreter_mode: bool = False
        self.current_program: Optional[str] = None

    def process_command(self, command: str) -> str:
        if command.lower() == "exit":
            if self.interpreter_mode:
                self.interpreter_mode = False
                return "Exiting interpreter mode"

            return "EXIT"

        if command.lower() == "interpreter":
            self.interpreter_mode = True
            return "Entering interpreter mode. Type 'exit' to leave."

        return self.os_core.execute_command(command)

    def get_prompt(self) -> str:
        if self.interpreter_mode:
            return ">>> "

        if self.current_program:
            return f"{self.current_program}> "

        return "$ "

    def is_interpreter_mode(self) -> bool:
        return self.interpreter_mode
