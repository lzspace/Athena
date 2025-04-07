"""
Script: intent_router.py
Category: NLU

Description:
Routes classified intent to the appropriate assistant module or tool.
"""

from assistant_core.interfaces import personal_data
from assistant_core.modules.appointments.handlers import handle_create_appointment
from assistant_core.modules.nlu.nlu_utils import extract_entities
from assistant_core.modules.scripts.handlers import handle_run_script


def route_intent(intent: str, user_input: str, user_id: str = "default") -> str:
    if intent == "add_appointment":
        from assistant_core.modules.appointments.handlers import handle_create_appointment
        parsed_data = extract_entities(user_input)
        return handle_create_appointment(parsed_data)
    elif intent == "update_appointment":
        from assistant_core.modules.appointments.handlers import handle_update_appointment
        return handle_update_appointment({"text": user_input})
    elif intent == "list_appointments":
        from assistant_core.modules.appointments.handlers import handle_list_appointments
        return handle_list_appointments()
    elif intent == "run_script":
        script_name = extract_script_name(user_input)
        return handle_run_script(script_name)
    else:
        return f"🚧 Sorry, I don’t know how to handle intent: {intent}"


def extract_script_name(user_input: str) -> str:
    # Simple heuristic — assumes format like: "run script 'schedule_study.py'"
    import re
    match = re.search(r"(?:run|execute)\s+(?:script\s+)?['\"]?([\w\-]+\.py)['\"]?", user_input)
    return match.group(1) if match else None