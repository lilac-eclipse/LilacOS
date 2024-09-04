# Python OS Tools/Demo Package

This package contains various tools and demos related to OS operations in Python.

## Setup

1. Clone the repository:
   ```
   git clone [your-repo-url]
   cd [your-repo-name]
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package and development dependencies:
   ```
   pip install -e ".[dev]"
   ```

## Usage

To export the project to clipboard for use with AI, run:
```
python tools/export_project_to_clip.py
```


To run the "Hello World" demo:

```
python -m python_os.main
```

This should print "Hello, World!" to the console.

## Development

- Run tests: `pytest`
- Format code: `black .`
- Run linter: `pylint python_os tests`

