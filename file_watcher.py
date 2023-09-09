from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileWatcherBinding:
    def __init__(self, sampling_frequency: float):
        """
        Initializes the FileWatcherBinding with a given sampling frequency.
        :param sampling_frequency: The frequency in seconds (or fraction of seconds) for sampling.
        :type sampling_frequency: float
        """
        self.sampling_frequency = sampling_frequency
        self.observer = Observer()

    def watch_file(self, file_name: str, file_event_handler) -> None:
        """
        Watches a specific file for changes.
        :param file_name: The path to the file to be watched.
        :type file_name: str
        :param file_event_handler: The handler function to be called on file change.
        """
        event_handler = CustomEventHandler(target_file=file_name, callback=file_event_handler)
        self.observer.schedule(event_handler, path=file_name, recursive=False)
        self.observer.start()

    def watch_dir(self, directory_name: str, dir_event_handler) -> None:
        """
        Watches a directory for changes.
        :param directory_name: The path to the directory to be watched.
        :type directory_name: str
        :param dir_event_handler: The handler function to be called on directory change.
        """
        event_handler = CustomEventHandler(target_directory=directory_name, callback=dir_event_handler)
        self.observer.schedule(event_handler, path=directory_name, recursive=True)
        self.observer.start()

    def file_event_handler(self, file_name: str) -> None:
        """
        Default event handler for file changes. Can be overridden.
        :param file_name: The path to the changed file.
        :type file_name: str
        """
        print(f"File {file_name} has changed.")

    def dir_event_handler(self, dir_name: str) -> None:
        """
        Default event handler for directory changes. Can be overridden.
        :param dir_name: The path to the changed directory.
        :type dir_name: str
        """
        print(f"Directory {dir_name} has changed.")

class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, target_file=None, target_directory=None, callback=None):
        super().__init__()
        self.target_file = target_file
        self.target_directory = target_directory
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and self.target_file and event.src_path == self.target_file:
            self.callback(event.src_path)
        elif event.is_directory and self.target_directory and event.src_path.startswith(self.target_directory):
            self.callback(event.src_path)


# Test cases
import unittest
import os
import tempfile

class TestFileWatcherBinding(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        os.unlink(self.temp_file.name)
        self.temp_dir.cleanup()

    def test_file_watcher(self):
        results = []

        def custom_handler(file_name: str) -> None:
            results.append(file_name)

        watcher = FileWatcherBinding(0.1)
        watcher.watch_file(self.temp_file.name, custom_handler)

        time.sleep(1)  # allow watcher to set up
        with open(self.temp_file.name, 'w') as f:
            f.write('test data')

        time.sleep(1)  # allow file changes to be detected
        self.assertIn(self.temp_file.name, results)

    def test_dir_watcher(self):
        results = []

        def custom_handler(dir_name: str) -> None:
            results.append(dir_name)

        watcher = FileWatcherBinding(0.1)
        watcher.watch_dir(self.temp_dir.name, custom_handler)

        time.sleep(1)  # allow watcher to set up
        temp_file_in_dir = os.path.join(self.temp_dir.name, 'test_file.txt')
        with open(temp_file_in_dir, 'w') as f:
            f.write('test data')

        time.sleep(1)  # allow directory changes to be detected
        self.assertIn(self.temp_dir.name, results)

if __name__ == '__main__':
    unittest.main()
