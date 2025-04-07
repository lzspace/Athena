"""
Script: intent_router.py
Category: NLU

Description:
Routes classified intent to the appropriate assistant module or tool.
"""

from assistant_core.interfaces import personal_data
from assistant_core.modules.nlu.context_memory import get_context, set_context, clear_context
import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from dateparser import parse as parse_date

def extract_entities(user_input: str) -> dict:
    data = {"title": "Untitled", "start": "", "end": ""}

    # Extract something resembling a title
    title_match = re.search(r"(?:einen\\s+)?([A-ZÄÖÜ][a-zäöüß]+termin)", user_input, re.IGNORECASE)
    if title_match:
        data["title"] = title_match.group(1).capitalize()

    # Try to extract a start time from the text using dateparser (German)
    parsed = parse_date(user_input, languages=["de"])
    if parsed:
        data["start"] = parsed.strftime("%Y-%m-%d %H:%M")
        end_time = parsed + timedelta(minutes=30)
        data["end"] = end_time.strftime("%Y-%m-%d %H:%M")
    else:
        print("⚠️  Kein gültiger Zeitpunkt erkannt in:", user_input)
        data["needs_clarification"] = True
        data["clarification_prompt"] = "Ich konnte keine genaue Uhrzeit oder Dauer erkennen. Wie lange soll der Termin dauern?"

    return data

def route_intent(intent: str, user_input: str, user_id: str = "default") -> str:
    if intent == "add_appointment":
        from assistant_core.modules.appointments.handlers import handle_create_appointment

        parsed_data = extract_entities(user_input)
        if parsed_data.get("needs_clarification"):
            set_context("appointments", user_id, {"pending_intent": "add_appointment", "data": parsed_data})
            return parsed_data["clarification_prompt"]

        return handle_create_appointment(parsed_data)

    elif intent == "update_appointment":
        from assistant_core.modules.appointments.handlers import handle_update_appointment
        parsed_data = extract_entities(user_input)
        return handle_update_appointment(parsed_data)

    elif intent == "list_appointments":
        from assistant_core.modules.appointments.handlers import handle_list_appointments
        return handle_list_appointments()

    elif intent == "run_script":
        script_name = extract_script_name(user_input)
        return personal_data.run_script(script_name)

    # Fallback: resume previous context
    previous_context = get_context("appointments", user_id)
    if previous_context.get("pending_intent") == "add_appointment":
        from assistant_core.modules.appointments.handlers import handle_create_appointment
        merged_data = {**previous_context.get("data", {}), "duration": user_input}
        clear_context("appointments", user_id)
        return handle_create_appointment(merged_data)

    return f"🚧 Sorry, I don’t know how to handle intent: {intent}"

def extract_script_name(user_input: str) -> str:
    # Simple heuristic — assumes format like: "run script 'schedule_study.py'"
    import re
    match = re.search(r"(?:run|execute)\s+(?:script\s+)?['\"]?([\w\-]+\.py)['\"]?", user_input)
    return match.group(1) if match else "unknown.py"

def extract_intents() -> list:
    from assistant_core.config.intents_config import load_intents
    intents_dict = load_intents()
    return list(intents_dict.keys())