# src/logger.py

import csv
import os
from datetime import datetime


class SessionLogger:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(log_dir, f"session_{timestamp}.csv")

        with open(self.log_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "event", "ear", "mar", "duration_frames"])

    def log_event(self, event, ear, mar, duration_frames):
        """Log a drowsiness or yawn event."""
        with open(self.log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                event,
                round(ear, 3),
                round(mar, 3),
                duration_frames
            ])

    def get_log_path(self):
        return self.log_path