# pylint: disable=wildcard-import,unused-import,unused-wildcard-import,broad-exception-caught
# pyright: reportWildcardImportFromLibrary=false, reportUnusedImport=false

import inspect
from types import ModuleType
from typing import List

from sandbox.qp_quipples_and_ideas import (
    python_tutorial,
    qp_list_and_loop_practice,
)

# List of modules to run.
modules_to_run: List[ModuleType] = [
    # python_tutorial,
    qp_list_and_loop_practice,
]


def print_header(text: str, char: str = "=", width: int = 80):
    print(f"\n{char * width}")
    print(f"{text:^{width}}")
    print(f"{char * width}")


def print_subheader(text: str, width: int = 80):
    print(f"\n╔{'═' * (width - 2)}╗")
    print(f"║ {text:<{width - 4}} ║")
    print(f"╚{'═' * (width - 2)}╝")


def discover_and_execute_quipples():

    for module in modules_to_run:
        module_name = module.__name__.rsplit(".", maxsplit=1)[-1]
        print_header(f"Executing functions from {module_name}")

        for func_name, func in inspect.getmembers(module, inspect.isfunction):
            print_subheader(f"Executing {func_name}")
            try:
                func()
            except Exception as e:
                print(f"Error executing {func_name}: {str(e)}")

        print("\n" + "-" * 80)  # Separator between modules


def main():
    discover_and_execute_quipples()


if __name__ == "__main__":
    main()
