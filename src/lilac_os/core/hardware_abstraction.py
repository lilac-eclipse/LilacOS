from .hardware import SimulatedHardware


class HardwareAbstractionLayer:
    def __init__(self, hardware: SimulatedHardware) -> None:
        self.hardware = hardware

    def read_memory(self, address: int) -> int:
        return self.hardware.memory.read_byte(address)

    def write_memory(self, address: int, value: int) -> None:
        self.hardware.memory.write_byte(address, value)

    def read_disk_block(self, block_number: int) -> bytes:
        return bytes(self.hardware.disk.read_block(block_number))

    def write_disk_block(self, block_number: int, data: bytes) -> None:
        self.hardware.disk.write_block(block_number, bytearray(data))

    # Add more methods as needed, e.g., for CPU operations, I/O, etc.
