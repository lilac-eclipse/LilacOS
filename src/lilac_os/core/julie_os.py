from collections import defaultdict

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

PHYSICAL_MEMORY_SIZE = 256  # bytes
PAGE_SIZE = 16  # bytes
TOTAL_PAGES = PHYSICAL_MEMORY_SIZE // PAGE_SIZE


# Base classes for student implementation
class BaseVirtualMemoryManager:
    def __init__(self, physical_memory, secondary_storage):
        self.physical_memory = physical_memory
        self.secondary_storage = secondary_storage
        self.free_pages = set(range(TOTAL_PAGES))
        self.page_queue = []  # For FIFO page replacement

    def handle_page_fault(self, process, virtual_page_number):
        raise NotImplementedError("Subclasses must implement this method")

    def evict_page(self, process, virtual_page_number):
        raise NotImplementedError("Subclasses must implement this method")


class BaseOS:
    def __init__(self):
        self.physical_memory = PhysicalMemory(PHYSICAL_MEMORY_SIZE)
        self.secondary_storage = SecondaryStorage()
        self.virtual_memory_manager = None  # Will be set in subclass
        self.processes = {}
        self.next_pid = 1
        self.virtual_memory_enabled = False
        self.programs = {}

    def create_process(self):
        pid = self.next_pid
        self.next_pid += 1
        process = Process(pid, self)
        self.processes[pid] = process
        return process

    def terminate_process(self, pid):
        if pid in self.processes:
            process = self.processes[pid]
            for start_address, size in process.memory_regions.items():
                self.free(pid, start_address)
            del self.processes[pid]

    def mmap(self, pid, size):
        return self.malloc(pid, size)

    def malloc(self, pid, size):
        raise NotImplementedError("Subclasses must implement this method")

    def free(self, pid, address):
        raise NotImplementedError("Subclasses must implement this method")

    def read_memory(self, pid, address):
        raise NotImplementedError("Subclasses must implement this method")

    def write_memory(self, pid, address, value):
        raise NotImplementedError("Subclasses must implement this method")

    def handle_page_fault(self, pid, virtual_address):
        raise NotImplementedError("Subclasses must implement this method")

    def translate_address(self, pid, virtual_address):
        raise NotImplementedError("Subclasses must implement this method")

    def set_virtual_memory_enabled(self, enabled):
        self.virtual_memory_enabled = enabled
        print(f"Virtual Memory {'Enabled' if enabled else 'Disabled'}")

    def create_program(self, program_class):
        process = self.create_process()
        program = program_class(process)
        self.programs[process.pid] = program
        return process.pid

    def execute_program_step(self, pid, step_number):
        if pid not in self.programs:
            raise ValueError(f"No program found with PID {pid}")
        self.programs[pid].execute_step(step_number)

    def dump_memory(self):
        print("Physical Memory Dump:")
        for i in range(0, len(self.physical_memory.memory), 16):
            chunk = self.physical_memory.memory[i : i + 16]
            hex_values = " ".join([f"{b:02x}" for b in chunk])
            ascii_values = "".join([chr(b) if 32 <= b < 127 else "." for b in chunk])
            print(f"{i:04x}: {hex_values:<48} {ascii_values}")

    def get_memory_usage(self):
        memory_usage = []
        for pid, process in self.processes.items():
            for start_address, size in process.memory_regions.items():
                memory_usage.append((start_address, size, f"Process {pid}"))

        memory_usage.sort(key=lambda x: x[0])

        free_spaces = []
        last_end = 0
        for start, size, _ in memory_usage:
            if start > last_end:
                free_spaces.append((last_end, start - last_end, "Free"))
            last_end = start + size
        if last_end < PHYSICAL_MEMORY_SIZE:
            free_spaces.append((last_end, PHYSICAL_MEMORY_SIZE - last_end, "Free"))

        memory_usage.extend(free_spaces)
        memory_usage.sort(key=lambda x: x[0])

        return memory_usage

    def dump_hard_drive(self):
        print("Secondary Storage (Hard Drive) Dump:")
        if not self.secondary_storage.storage:
            print("  The secondary storage is empty.")
            return

        for page_id, data in self.secondary_storage.storage.items():
            pid, vpn = page_id
            print(f"  Page (PID: {pid}, VPN: {vpn}):")
            for i in range(0, len(data), 16):
                chunk = data[i : i + 16]
                hex_values = " ".join([f"{b:02x}" for b in chunk])
                ascii_values = "".join(
                    [chr(b) if 32 <= b < 127 else "." for b in chunk]
                )
                print(f"    {i:04x}: {hex_values:<48} {ascii_values}")


class JulieVirtualMemoryManager(BaseVirtualMemoryManager):
    def handle_page_fault(self, process, virtual_page_number):
        if not self.free_pages:
            evicted_page = self.evict_page(process, virtual_page_number)
            self.free_pages.add(evicted_page)

        physical_page = self.free_pages.pop()
        self.page_queue.append((process.pid, virtual_page_number, physical_page))

        page_table_entry = process.page_table.get_entry(virtual_page_number)
        page_table_entry.physical_page = physical_page
        page_table_entry.present = True
        page_table_entry.dirty = False

        # Load page from secondary storage
        page_data = self.secondary_storage.read_page((process.pid, virtual_page_number))
        self.physical_memory.write_page(physical_page, page_data)

        return physical_page

    def evict_page(self, process, virtual_page_number):
        evicted_pid, evicted_virtual_page, evicted_physical_page = self.page_queue.pop(
            0
        )
        evicted_process = process.os.processes[evicted_pid]
        evicted_entry = evicted_process.page_table.get_entry(evicted_virtual_page)

        if evicted_entry.dirty:
            # Write dirty page to secondary storage
            page_data = self.physical_memory.read_page(evicted_physical_page)
            self.secondary_storage.write_page(
                (evicted_pid, evicted_virtual_page), page_data
            )

        evicted_entry.present = False
        evicted_entry.dirty = False
        return evicted_physical_page


class JulieOS(BaseOS):
    def __init__(self):
        super().__init__()
        self.virtual_memory_manager = JulieVirtualMemoryManager(
            self.physical_memory, self.secondary_storage
        )
        self.free_list = [(0, PHYSICAL_MEMORY_SIZE)]
        self.next_virtual_address = defaultdict(int)

    def malloc(self, pid, size):
        process = self.processes[pid]

        # Round up size to the nearest page size
        pages_needed = (size + PAGE_SIZE - 1) // PAGE_SIZE
        size_to_allocate = pages_needed * PAGE_SIZE

        # Virtual memory allocation
        if self.virtual_memory_enabled:
            start_address = self.next_virtual_address[pid]
            self.next_virtual_address[pid] += size_to_allocate

            process.memory_regions[start_address] = size_to_allocate
            return start_address, size_to_allocate

        # Physical memory allocation
        for i, (start, free_size) in enumerate(self.free_list):
            if free_size >= size:
                del self.free_list[i]
                if free_size > size:
                    self.free_list.append((start + size, free_size - size))
                process.memory_regions[start] = size
                return start, size

        # If no suitable free region, raise an exception
        raise Exception("Out of memory")

    def free(self, pid, address):
        process = self.processes[pid]
        if address in process.memory_regions:
            size = process.memory_regions[address]
            del process.memory_regions[address]

            if not self.virtual_memory_enabled:
                self.free_list.append((address, size))
                self.free_list.sort(key=lambda x: x[0])
                # Merge adjacent free regions
                i = 0
                while i < len(self.free_list) - 1:
                    current_addr, current_size = self.free_list[i]
                    next_addr, next_size = self.free_list[i + 1]
                    if current_addr + current_size == next_addr:
                        self.free_list[i] = (current_addr, current_size + next_size)
                        del self.free_list[i + 1]
                    else:
                        i += 1

            if self.virtual_memory_enabled:
                start_page = address // PAGE_SIZE
                end_page = (address + size - 1) // PAGE_SIZE
                for virtual_page in range(start_page, end_page + 1):
                    entry = process.page_table.get_entry(virtual_page)
                    if entry.present:
                        self.virtual_memory_manager.free_pages.add(entry.physical_page)
                        if (
                            entry.physical_page
                            in self.virtual_memory_manager.page_queue
                        ):
                            self.virtual_memory_manager.page_queue.remove(
                                entry.physical_page
                            )
                        entry.present = False

    def read_memory(self, pid, address):
        if not self._address_belongs_to_process(pid, address):
            raise Exception(
                f"Memory access violation: Process {pid} cannot access address {address}"
            )
        physical_address = self.translate_address(pid, address)
        return self.physical_memory.read_byte(physical_address)

    def write_memory(self, pid, address, value):
        if not self._address_belongs_to_process(pid, address):
            raise Exception(
                f"Memory access violation: Process {pid} cannot access address {address}"
            )
        physical_address = self.translate_address(pid, address)
        self.physical_memory.write_byte(physical_address, value)
        if self.virtual_memory_enabled:
            process = self.processes[pid]
            virtual_page = address // PAGE_SIZE
            page_table_entry = process.page_table.get_entry(virtual_page)
            page_table_entry.dirty = True

    def _address_belongs_to_process(self, pid, address):
        process = self.processes[pid]
        for start_address, size in process.memory_regions.items():
            if start_address <= address < start_address + size:
                return True
        return False

    def handle_page_fault(self, pid, virtual_address):
        process = self.processes[pid]
        virtual_page = virtual_address // PAGE_SIZE
        return self.virtual_memory_manager.handle_page_fault(process, virtual_page)

    def translate_address(self, pid, virtual_address):
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

        return (physical_page * PAGE_SIZE) + offset

    def set_virtual_memory_enabled(self, enabled):
        self.virtual_memory_enabled = enabled
        if enabled:
            self.next_virtual_address = defaultdict(
                int
            )  # Reset virtual address space when enabling VM
        print(f"Virtual Memory {'Enabled' if enabled else 'Disabled'}")


# Classes that don't need student implementation
class PhysicalMemory:
    def __init__(self, size):
        self.memory = bytearray(size)

    def read_byte(self, address):
        return self.memory[address]

    def write_byte(self, address, value):
        self.memory[address] = value

    def read_page(self, page_number):
        start = page_number * PAGE_SIZE
        return self.memory[start : start + PAGE_SIZE]

    def write_page(self, page_number, data):
        start = page_number * PAGE_SIZE
        self.memory[start : start + PAGE_SIZE] = data


class PageTableEntry:
    def __init__(self):
        self.physical_page = None
        self.present = False
        self.dirty = False


class PageTable:
    def __init__(self):
        self.entries = {}  # virtual_page_number -> PageTableEntry

    def get_entry(self, virtual_page_number):
        if virtual_page_number not in self.entries:
            self.entries[virtual_page_number] = PageTableEntry()
        return self.entries[virtual_page_number]


class SecondaryStorage:
    def __init__(self):
        self.storage = {}  # page_number -> data

    def read_page(self, page_number):
        return self.storage.get(page_number, bytearray(PAGE_SIZE))

    def write_page(self, page_number, data):
        self.storage[page_number] = data


class Process:
    def __init__(self, pid, os):
        self.pid = pid
        self.os = os
        self.page_table = PageTable()
        self.memory_regions = (
            {}
        )  # start_address -> size. Note that this is set by the OS, we don't update it
        self.mallocs = (
            {}
        )  # start_address -> size for malloc'd regions within memory_regions

    def malloc(self, size):
        # First, try to find a free space in existing allocations
        for region_start, region_size in self.memory_regions.items():
            region_end = region_start + region_size
            allocated_spaces = sorted(
                [
                    (addr, addr + size)
                    for addr, size in self.mallocs.items()
                    if region_start <= addr < region_end
                ]
            )

            # Check for space at the beginning of the region
            if not allocated_spaces or allocated_spaces[0][0] - region_start >= size:
                new_addr = region_start
                self.mallocs[new_addr] = size
                return new_addr

            # Check for spaces between allocations
            for i in range(len(allocated_spaces) - 1):
                if allocated_spaces[i + 1][0] - allocated_spaces[i][1] >= size:
                    new_addr = allocated_spaces[i][1]
                    self.mallocs[new_addr] = size
                    return new_addr

            # Check for space at the end of the region
            if region_end - allocated_spaces[-1][1] >= size:
                new_addr = allocated_spaces[-1][1]
                self.mallocs[new_addr] = size
                return new_addr

        # If we don't have space, request a new memory region from the OS
        address, mmap_size = self.os.mmap(self.pid, size)
        self.mallocs[address] = size
        return address

    def free(self, address):
        if address in self.mallocs:
            del self.mallocs[address]
        else:
            self.os.free(self.pid, address)

    # def malloc(self, size):

    #     address, mmap_size = self.os.mmap(self.pid, size)
    #     return address

    # def free(self, address):
    #     self.os.free(self.pid, address)

    def read_memory(self, address):
        return self.os.read_memory(self.pid, address)

    def write_memory(self, address, value):
        self.os.write_memory(self.pid, address, value)


class BaseProgram:
    def __init__(self, process):
        self.process = process
        self.variables = {}

    def allocate_variable(self, name, size):
        address = self.process.malloc(size)
        self.variables[name] = {"address": address, "size": size}
        print(f"Allocated variable '{name}' of size {size} at address {address}")

    def set_variable(self, name, value):
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not allocated")
        address = self.variables[name]["address"]
        if isinstance(value, int):
            self.process.write_memory(address, value)
        elif isinstance(value, str):
            for i, char in enumerate(value):
                self.process.write_memory(address + i, ord(char))
        print(f"Set value of variable '{name}' to {value}")

    def get_variable(self, name):
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not allocated")
        address = self.variables[name]["address"]
        size = self.variables[name]["size"]
        values = [self.process.read_memory(address + i) for i in range(size)]
        print(f"Value of variable '{name}': {values}")
        return values

    def free_variable(self, name):
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not allocated")
        address = self.variables[name]["address"]
        self.process.free(address)
        del self.variables[name]
        print(f"Freed variable '{name}'")

    def dump_memory(self):
        print(f"Memory Dump for Program (PID: {self.process.pid}):")
        for name, info in self.variables.items():
            address, size = info["address"], info["size"]
            print(f"\nVariable: {name}")
            for i in range(0, size, 16):
                chunk = [
                    self.process.read_memory(address + j)
                    for j in range(i, min(i + 16, size))
                ]
                hex_values = " ".join([f"{b:02x}" for b in chunk])
                ascii_values = "".join(
                    [chr(b) if 32 <= b < 127 else "." for b in chunk]
                )
                print(f"{address+i:04x}: {hex_values:<48} {ascii_values}")

    def get_memory_usage(self):
        return [
            (name, info["size"], info["address"])
            for name, info in self.variables.items()
        ]

    def execute_step(self, step_number):
        method_name = f"step_{step_number}"
        if hasattr(self, method_name):
            getattr(self, method_name)()
        else:
            print(f"Step {step_number} not found")


# def visualize_memory(os):
#     # Create subplots: one for OS, one for each program
#     fig = make_subplots(
#         rows=1 + len(os.programs),
#         cols=1,
#         subplot_titles=["OS Memory"] + [f"Program {pid} Memory" for pid in os.programs],
#     )

#     # OS Memory
#     os_memory = os.get_memory_usage()
#     for start, size, label in os_memory:
#         fig.add_trace(
#             go.Bar(
#                 x=[size],
#                 y=[label],
#                 orientation="h",
#                 name=label,
#                 text=f"Start: {start}, Size: {size}",
#                 textposition="auto",
#             ),
#             row=1,
#             col=1,
#         )

#     # Program Memory
#     for i, (pid, program) in enumerate(os.programs.items(), start=2):
#         prog_memory = program.get_memory_usage()
#         for name, size, address in prog_memory:
#             fig.add_trace(
#                 go.Bar(
#                     x=[size],
#                     y=[name],
#                     orientation="h",
#                     name=name,
#                     text=f"Address: {address}, Size: {size}",
#                     textposition="auto",
#                 ),
#                 row=i,
#                 col=1,
#             )

#     fig.update_layout(height=300 * (1 + len(os.programs)), width=800, showlegend=False)
#     fig.show()
