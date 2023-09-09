# File and Directory Watcher

The File and Directory Watcher is a utility designed to monitor changes in specific files or directories. When a change is detected, it triggers a designated event handler. This is especially useful for applications that need to react to file system changes in real-time.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Defining Event Handlers](#defining-event-handlers)
  - [Monitoring Files and Directories](#monitoring-files-and-directories)
- [Testing](#testing)
- [License](#license)

## Installation

Before you can use the File and Directory Watcher, you need to ensure that all necessary libraries are installed.

Firstly, ensure you have Python installed on your machine.

Next, install the required library using pip:

```bash
pip install watchdog
```

## Usage

### Initialization

To begin, create an instance of the `FileWatcherBinding` class. The constructor takes one parameter: `sampling_frequency`, which defines the interval (in seconds) at which the utility checks for changes.

```python
from your_script_name import FileWatcherBinding

watcher = FileWatcherBinding(sampling_frequency=0.1)  # checks every 100ms
```

Replace `your_script_name` with the name of the script containing the utility.

### Defining Event Handlers

Event handlers are functions that are triggered when a change is detected in the watched file or directory.

Define custom event handlers for files and directories:

```python
def my_file_handler(file_name: str) -> None:
    print(f"File {file_name} has changed!")

def my_dir_handler(dir_name: str) -> None:
    print(f"Directory {dir_name} has changed!")
```

You can customize these handlers to execute any code in response to a change.

### Monitoring Files and Directories

Once you've defined your event handlers, you can start monitoring specific files and directories:

```python
watcher.watch_file('path/to/your/file.txt', my_file_handler)
watcher.watch_dir('path/to/your/directory', my_dir_handler)
```

With these lines in place, the utility will print messages (or execute your custom code) whenever the watched file or directory undergoes changes.

## Testing

The utility comes with a test suite built with `unittest`. It ensures the basic functionality of file and directory watching works as expected.

To run the tests, execute:

```bash
python -m unittest your_script_name.py
```

Replace `your_script_name.py` with the name of the script containing the utility and tests.

## License

This utility is provided under the MIT License. This means you're free to modify, distribute, and use it in both personal and commercial projects, but you must provide the necessary attributions.

For more information on the MIT License, refer to [this link](https://opensource.org/licenses/MIT).
