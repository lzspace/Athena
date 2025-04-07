"""
Script: openai_interface.py
Category: Interfaces

Description:
Handles communication with the OpenAI API (e.g., GPT-4, GPT-3.5) to provide fallback capability when the local model has low confidence.
"""

import os
import openai
from difflib import SequenceMatcher

# Use an environment variable to load the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenAI Error] {e}"

def fallback_to_openai(prompt: str, known_intents: list) -> tuple:
    """
    Use OpenAI to classify the intent with fallback confidence scoring.
    """
    raw_response = generate_response(prompt)
    best_intent = None
    best_score = 0.0

    for intent in known_intents:
        score = SequenceMatcher(None, raw_response.lower(), intent.lower()).ratio()
        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent, best_score