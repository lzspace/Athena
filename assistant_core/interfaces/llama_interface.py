"""
Script: llama_interface.py
Category: Interfaces

Description:
Handles prompt exchange with a locally hosted LLaMA model using Ollama's HTTP API.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def send_prompt(prompt: str, model: str = "llama2") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json().get("response", "")