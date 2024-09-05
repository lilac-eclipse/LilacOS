from typing import Dict

MEMORY_SIZE: int = 256  # 256 bytes
DISK_SIZE: int = 1024  # 1 KB


class SimulatedMemory:
    def __init__(self) -> None:
        self.memory: bytearray = bytearray(MEMORY_SIZE)

    def read_byte(self, address: int) -> int:
        return self.memory[address]

    def write_byte(self, address: int, value: int) -> None:
        self.memory[address] = value


class SimulatedDisk:
    def __init__(self) -> None:
        self.storage: Dict[int, bytearray] = {}
        self.size: int = DISK_SIZE

    def read_block(self, block_number: int) -> bytearray:
        return self.storage.get(block_number, bytearray(16))  # 16-byte blocks

    def write_block(self, block_number: int, data: bytearray) -> None:
        if len(data) != 16:
            raise ValueError("Block size must be 16 bytes")
        self.storage[block_number] = data


class SimulatedHardware:
    def __init__(self) -> None:
        self.memory: SimulatedMemory = SimulatedMemory()
        self.disk: SimulatedDisk = SimulatedDisk()
