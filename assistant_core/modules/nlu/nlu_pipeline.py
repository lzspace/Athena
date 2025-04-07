"""
Script: nlu_pipeline.py
Category: NLU

Description:
Processes user input, classifies intents, and routes to appropriate modules.
"""

from assistant_core.interfaces import llama_interface
from assistant_core.modules.nlu import intent_router
from assistant_core.modules.nlu.nlu_utils import extract_intents, extract_entities
from assistant_core.modules.nlu.context_memory import get_context, clear_context, set_context
from assistant_core.modules.nlu.prompt_templates import INTENT_PROMPT_TEMPLATE
from assistant_core.interfaces.openai_interface import fallback_to_openai
from pathlib import Path
from difflib import SequenceMatcher

def log_low_confidence(input_text: str, predicted: str, score: float):
    if score < 0.75:
        log_file = Path("logs/low_confidence.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write(f"{input_text} → {predicted} (score: {score:.2f})\\n")


def process_user_input(user_input: str, user_id: str = "default") -> str:
    known_intents = extract_intents()
    prompt = INTENT_PROMPT_TEMPLATE.format(input=user_input, intents=", ".join(known_intents))
    raw_response = llama_interface.send_prompt(prompt)

    predicted_intent, confidence = compute_confidence(raw_response, known_intents)
    log_low_confidence(user_input, predicted_intent, confidence)

    # Fallback to OpenAI if LLaMA isn't confident
    if confidence < 0.75:
        print("⚠️  LLaMA not confident. Falling back to OpenAI...")
        predicted_intent, confidence = fallback_to_openai(prompt, known_intents)
        log_low_confidence(user_input, predicted_intent, confidence)

    return intent_router.route_intent(predicted_intent, user_input, user_id)

def compute_confidence(output: str, known_intents: list[str]) -> tuple[str, float]:
    output = output.strip().lower()
    best_match = max(known_intents, key=lambda intent: SequenceMatcher(None, intent, output).ratio())
    score = SequenceMatcher(None, best_match, output).ratio()
    return best_match, score