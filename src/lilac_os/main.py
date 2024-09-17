from lilac_os.core.hardware import SimulatedHardware
from lilac_os.core.hardware_abstraction import HardwareAbstractionLayer
from lilac_os.core.os_core import OSCore
from lilac_os.gui.terminal import TerminalGUI
from lilac_os.gui.window_manager import WindowManager
from lilac_os.gui.memory_viewer import MemoryViewer
from lilac_os.core.terminal_controller import TerminalController


def main() -> None:
    # Create virtual hardware
    hardware: SimulatedHardware = SimulatedHardware()

    # Create hardware abstraction layer
    hal: HardwareAbstractionLayer = HardwareAbstractionLayer(hardware)

    # Launch OS kernel
    os_core: OSCore = OSCore(hal)

    # Initialize GUI
    window_manager = WindowManager()

    # Create memory viewer
    memory_viewer = MemoryViewer(hardware)
    memory_viewer.show()

    # Set memory viewer in OS core
    os_core.set_memory_viewer(memory_viewer)

    # Create terminal controller
    terminal_controller = TerminalController(os_core)

    # Create terminal
    window_manager.create_window(
        TerminalGUI, terminal_controller=terminal_controller, window_id="1"
    )

    # Update memory viewer initially
    memory_viewer.refresh_views()

    # Run all windows
    window_manager.run_all_windows()


if __name__ == "__main__":
    main()
