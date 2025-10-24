# safety.py
from __future__ import annotations
import re
from typing import Tuple

# Very lightweight input checks (extend if needed)
PROHIBITED_PATTERNS = [
    r"\bmake\s+(a\s+)?weapon\b",
    r"\bexplosive(s)?\b",
    r"\bcredit\s*card\s*numbers?\b",
    r"\bhate\s*speech\b",
]

DISALLOWED_TOPICS = [
    "instructions to create weapons, explosives, or malware",
    "direct medical or legal advice",
    "personal data exfiltration or deanonymization",
    "targeted harassment or hateful content",
]

REFUSAL_MESSAGE = (
    "I can’t help with that request. Here’s a safer direction we could take instead: "
    "discuss the ethical impacts, risk mitigations, or high-level safety principles."
)

def basic_screen(text: str) -> Tuple[bool, str]:
    """
    Returns (is_safe, message_if_blocked).
    This is a simple static filter to catch obviously unsafe queries.
    """
    lowered = text.lower()
    for pat in PROHIBITED_PATTERNS:
        if re.search(pat, lowered):
            return False, REFUSAL_MESSAGE
    return True, ""