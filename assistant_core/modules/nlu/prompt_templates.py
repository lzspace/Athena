"""
Script: prompt_templates.py
Category: NLU

Description:
Provides reusable prompt templates for intent classification and entity extraction.
"""

def intent_classification_prompt(user_input: str) -> str:
    return f"""
You are a helpful assistant. Classify the user's intent.

User: "{user_input}"
Available intents: [add_appointment, delete_appointment, query_appointment, run_script]

Respond only with the intent name.
"""