from lilac_os.core.os_core import os_instance
from lilac_os.gui.terminal import TerminalGUI
from lilac_os.gui.window_manager import WindowManager


def hello_world() -> str:
    return "Hello, World!"


def main() -> None:
    window_manager = WindowManager()

    # Create multiple terminal windows
    num_terminals = 1  # You can change this number to create more or fewer terminals
    for i in range(num_terminals):
        window_manager.create_window(
            TerminalGUI, os_core=os_instance, window_id=f"{i+1}"
        )

    # Run all windows
    window_manager.run_all_windows()


if __name__ == "__main__":
    main()
