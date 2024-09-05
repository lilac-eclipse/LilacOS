from typing import Dict, List, Tuple, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .os_core import OSCore


PAGE_SIZE: int = 16  # bytes
TOTAL_PAGES: int = 16  # 256 bytes total memory


class PageTableEntry:
    def __init__(self) -> None:
        self.physical_page: Optional[int] = None
        self.present: bool = False
        self.dirty: bool = False


class PageTable:
    def __init__(self) -> None:
        self.entries: Dict[int, PageTableEntry] = {}

    def get_entry(self, virtual_page_number: int) -> PageTableEntry:
        if virtual_page_number not in self.entries:
            self.entries[virtual_page_number] = PageTableEntry()
        return self.entries[virtual_page_number]


class MemoryManager:
    def __init__(self, os_core: "OSCore") -> None:
        self.os_core: "OSCore" = os_core
        self.free_pages: List[int] = list(range(TOTAL_PAGES))
        self.page_queue: List[Tuple[int, int, int]] = []  # (pid, vpn, ppn)
        self.virtual_memory_enabled: bool = False

    def malloc(self, pid: int, size: int) -> int:
        process = self.os_core.processes[pid]
        pages_needed = (size + PAGE_SIZE - 1) // PAGE_SIZE
        start_page = len(process.memory_regions)
        for i in range(pages_needed):
            process.memory_regions[start_page + i] = PAGE_SIZE
        return start_page * PAGE_SIZE

    def free(self, pid: int, address: int) -> None:
        process = self.os_core.processes[pid]
        page = address // PAGE_SIZE
        if page in process.memory_regions:
            del process.memory_regions[page]
            if self.virtual_memory_enabled:
                entry = process.page_table.get_entry(page)
                if entry.present and entry.physical_page is not None:
                    self.free_pages.append(entry.physical_page)
                    entry.present = False

    def read_memory(self, pid: int, address: int) -> int:
        physical_address = self.translate_address(pid, address)
        return self.os_core.hal.read_memory(physical_address)

    def write_memory(self, pid: int, address: int, value: int) -> None:
        physical_address = self.translate_address(pid, address)
        self.os_core.hal.write_memory(physical_address, value)
        if self.virtual_memory_enabled:
            process = self.os_core.processes[pid]
            virtual_page = address // PAGE_SIZE
            page_table_entry = process.page_table.get_entry(virtual_page)
            page_table_entry.dirty = True
        if self.os_core.memory_viewer:
            self.os_core.memory_viewer.update()

    def translate_address(self, pid: int, virtual_address: int) -> int:
        if not self.virtual_memory_enabled:
            return virtual_address

        process = self.os_core.processes[pid]
        virtual_page = virtual_address // PAGE_SIZE
        offset = virtual_address % PAGE_SIZE

        page_table_entry = process.page_table.get_entry(virtual_page)
        if not page_table_entry.present:
            physical_page = self.handle_page_fault(pid, virtual_address)
        else:
            physical_page = page_table_entry.physical_page

        if physical_page is None:
            raise ValueError("Physical page is None after translation")

        return (physical_page * PAGE_SIZE) + offset

    def handle_page_fault(self, pid: int, virtual_address: int) -> int:
        process = self.os_core.processes[pid]
        virtual_page = virtual_address // PAGE_SIZE

        if not self.free_pages:
            evicted_page = self.evict_page()
            self.free_pages.append(evicted_page)

        physical_page = self.free_pages.pop(0)
        self.page_queue.append((pid, virtual_page, physical_page))

        page_table_entry = process.page_table.get_entry(virtual_page)
        page_table_entry.physical_page = physical_page
        page_table_entry.present = True
        page_table_entry.dirty = False

        return physical_page

    def evict_page(self) -> int:
        evicted_pid, evicted_virtual_page, evicted_physical_page = self.page_queue.pop(
            0
        )
        evicted_process = self.os_core.processes[evicted_pid]
        evicted_entry = evicted_process.page_table.get_entry(evicted_virtual_page)

        if evicted_entry.dirty:
            # Write dirty page to disk (not implemented in this simplified version)
            pass

        evicted_entry.present = False
        evicted_entry.dirty = False
        return evicted_physical_page

    def set_virtual_memory_enabled(self, enabled: bool) -> None:
        self.virtual_memory_enabled = enabled
        print(f"Virtual Memory {'Enabled' if enabled else 'Disabled'}")
