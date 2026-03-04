import time
import subprocess
from pathlib import Path

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "data/raw"


class VideoHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() == ".mp4":
            print(f"New video detected: {file_path}")

            subprocess.run(
                ["python", "scripts/run_pipeline.py", str(file_path)],
                check=True
            )


if __name__ == "__main__":

    observer = PollingObserver(timeout=5)  # checks folder every 5 seconds
    handler = VideoHandler()

    observer.schedule(handler, WATCH_FOLDER, recursive=False)
    observer.start()

    print(f"Watching folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()