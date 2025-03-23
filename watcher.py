import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Ο φάκελος που θέλεις να παρακολουθείς
WATCH_DIRECTORY = "."


class RuffFormatter(FileSystemEventHandler):
    def on_modified(self, event):
        # Ελέγχουμε αν το αρχείο που άλλαξε είναι .py
        if event.src_path.endswith(".py"):
            print(f"Αλλαγή εντοπίστηκε στο: {event.src_path}")
            self.run_ruff_format(event.src_path)

    def run_ruff_format(self, file_path):
        print(f"Εκτέλεση ruff format στο: {file_path}")
        try:
            # Εκτέλεση του ruff format
            subprocess.run(["ruff", "format", file_path], check=True)
            print("ruff format ολοκληρώθηκε με επιτυχία!")
        except subprocess.CalledProcessError as e:
            print(f"Σφάλμα κατά την εκτέλεση του ruff format: {e}")


if __name__ == "__main__":
    event_handler = RuffFormatter()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIRECTORY, recursive=True)
    observer.start()

    print(f"Παρακολούθηση του φακέλου '{WATCH_DIRECTORY}' για αλλαγές...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
