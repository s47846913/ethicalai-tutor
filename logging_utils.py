# logging_utils.py
import csv  # CSV module for structured, traceable data logs (traceability)
import os  # OS module to handle file and directory operations (accountability)
import time  # Time module to timestamp events for traceability
from typing import Optional  # Typing for clarity and transparency in function signatures

LOG_DIR = "logs"  # Directory for logs, centralizing records for accountability
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure log directory exists, supporting reliable traceability
LOG_PATH = os.path.join(LOG_DIR, "sessions.csv")  # Path for session logs, keeping data organized for transparency

def log_event(role: str, content: str, explain: bool, topic: Optional[str]):
    """Append a chat event to the session log CSV file."""
        # Compose a log entry as a dictionary for structured, transparent storage
    row = {
        "timestamp": int(time.time()),  # Record current time for traceability
        "role": role,  # Log user/AI role for accountability
        "content": content[:800],  # Store message content, limit length for clarity and privacy
        "explain_mode": explain,  # Track if explain mode is active (transparency)
        "topic": topic or "",  # Log topic for context and traceability
    }
    file_exists = os.path.exists(LOG_PATH)  # Check if log file exists to manage headers (traceability)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:  # Open log file in append mode (accountability)
        writer = csv.DictWriter(f, fieldnames=row.keys())  # Use DictWriter for structured, transparent logs
        if not file_exists:
            writer.writeheader()  # Add headers if file is new, supporting transparency
        writer.writerow(row)  # Write the log entry, ensuring traceable records