from python_os.core.os_core import os_instance
from python_os.gui.terminal import TerminalGUI
from python_os.gui.window_manager import WindowManager


def hello_world():
    return "Hello, World!"


def main():
    window_manager = WindowManager()

    # Create multiple terminal windows
    num_terminals = 3  # You can change this number to create more or fewer terminals
    for i in range(num_terminals):
        window_manager.create_window(
            TerminalGUI, os_core=os_instance, window_id=f"{i+1}"
        )

    # Run all windows
    window_manager.run_all_windows()


if __name__ == "__main__":
    main()
