# utils.py
import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def build_messages(system_prompt: str, history: List[Dict], user_text: str) -> List[Dict]:
    msgs = [{"role": "system", "content": system_prompt}]
    msgs.extend(history)
    msgs.append({"role": "user", "content": user_text})
    return msgs