import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess

class Watcher:
    DIRECTORY_TO_WATCH = "/Users/chamanlal/Desktop/Projects/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        if event.src_path.endswith("Corporates MIS Report.xlsx"):
            print(f"Modification detected in {event.src_path}. Running report script...")
            subprocess.call(["/usr/local/bin/python3", "/Users/chamanlal/Desktop/Projects/generate_report.py"])

if __name__ == '__main__':
    w = Watcher()
    w.run()
