# utils.py
# This module provides utility functions for interacting with OpenAI and managing prompt messages, supporting modularity and transparency.
import os  # Provides access to environment variables for secure configuration (accountability, modularity).
from typing import List, Dict  # Enables type hints for clarity and maintainability (transparency).
from dotenv import load_dotenv  # Loads environment variables from a .env file for secure config management (accountability).
from openai import OpenAI  # Imports the OpenAI client library for API access (modularity).

load_dotenv()  # Loads environment variables from a .env file, keeping sensitive info out of code (security, accountability).

def get_client() -> OpenAI | None:
    # Retrieves the OpenAI API key from environment variables for secure authentication (accountability, transparency).
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Returns None if the API key is missing, helping to prevent unauthorized access (accountability).
        return None
    # Returns an OpenAI client instance initialized with the API key (modularity, transparency).
    return OpenAI(api_key=api_key)

def get_model() -> str:
    # Retrieves the OpenAI model name from environment variables, defaulting to 'gpt-4o-mini' for fallback (transparency, modularity).
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def build_messages(system_prompt: str, history: List[Dict], user_text: str) -> List[Dict]:
    # Constructs a list of message dicts for the OpenAI API, starting with the system prompt (clarity, transparency).
    msgs = [{"role": "system", "content": system_prompt}]
    # Adds previous conversation history to provide context for the AI (context preservation, transparency).
    msgs.extend(history)
    # Appends the latest user message to complete the prompt sequence (modularity, clarity).
    msgs.append({"role": "user", "content": user_text})
    # Returns the full message list for use with the OpenAI API (modularity, transparency).
    return msgs