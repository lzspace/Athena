"""
Script: nlu_pipeline.py
Category: NLU

Description:
Entry point for the assistant's NLU: runs prompt generation, sends to LLaMA,
extracts intent, and routes to the right module.
"""

from assistant_core.modules.nlu import prompt_templates, intent_router
from assistant_core.interfaces import llama_interface

def process_user_input(user_input: str) -> str:
    prompt = prompt_templates.intent_classification_prompt(user_input)
    raw_response = llama_interface.send_prompt(prompt)
    intent = raw_response.strip().lower()
    return intent_router.route_intent(intent, user_input)