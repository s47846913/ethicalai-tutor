# logging_utils.py
import csv
import os
import time
from typing import Optional

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "sessions.csv")

def log_event(role: str, content: str, explain: bool, topic: Optional[str]):
    """Append a chat event to the session log CSV file."""
    row = {
        "timestamp": int(time.time()),
        "role": role,
        "content": content[:800],  # limit long text for neat logs
        "explain_mode": explain,
        "topic": topic or "",
    }
    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)