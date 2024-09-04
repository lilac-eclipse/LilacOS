# Python OS Tools/Demo Package

This package contains various tools and demos related to OS operations in Python.

## Setup

1. Clone the repository:
   ```
   git clone [your-repo-url]
   cd [your-repo-name]
   ```

2. Install Hatch (if not already installed):
   ```
   pip install hatch
   ```

3. Set up the development environment:
   ```
   hatch env create
   ```

## Usage

To enter the development environment:
```
hatch shell
```

Once in the Hatch shell:

- To run the app:
  ```
  hatch run app
  ```

## Development

Hatch provides several commands for development tasks:

- Quick development (format and run):
  ```
  hatch run dev
  ```
- Strict development (format, type check, and run):
  ```
  hatch run dev_strict
  ```
- Run tests (format and unit test):
  ```
  hatch run test
  ```
- Run strict tests (format, type check, and unit test):
  ```
  hatch run test_strict
  ```
- Pre-commit checks (format, type check, lint, and unit test):
  ```
  hatch run precommit
  ```

- To export the project to clipboard:
  ```
  hatch run export
  ```

## Additional Notes

- The `pyproject.toml` file contains all the configuration for the project, including dependencies and development tool settings.
- Hatch manages virtual environments for you, so there's no need to manually create or activate a venv.

