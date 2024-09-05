import os
import pyperclip

# Directories to exclude
EXCLUDE_DIRS = {
    "venv",
    "venv-win",
    ".git",
    "tools",
    ".pytest_cache",
    "lilac_os.egg-info",
    "__pycache__",
    ".mypy_cache",
    "sandbox",
}


def get_directory_structure(startpath):
    output = []
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * level
        output.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            output.append(f"{sub_indent}{f}")
    return "\n".join(output)


def get_file_contents(startpath):
    output = []
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(
                (".py", ".txt", ".md", ".json", ".yaml", ".yml", ".toml")
            ):  # Add or remove extensions as needed
                file_path = os.path.join(root, file)
                output.append(f"\n\n--- Contents of {file_path} ---\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        output.append(f.read())
                except Exception as e:  # pylint: disable=broad-exception-caught
                    output.append(f"Error reading file: {str(e)}")
    return "\n".join(output)


def main():
    project_dir = "."  # Current directory

    # Get directory structure
    dir_structure = get_directory_structure(project_dir)

    # Get file contents
    file_contents = get_file_contents(project_dir)

    # Combine the output
    full_output = (
        f"Directory Structure:\n\n{dir_structure}\n\nFile Contents:{file_contents}"
    )

    # Print to console
    print(full_output)

    # Copy to clipboard
    pyperclip.copy(full_output)
    print("\nFull project summary has been copied to the clipboard.")


if __name__ == "__main__":
    main()
