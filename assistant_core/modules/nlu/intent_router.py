"""
Script: intent_router.py
Category: NLU

Description:
Routes classified intent to the appropriate assistant module or tool.
"""

from assistant_core.interfaces import personal_data


def route_intent(intent: str, user_input: str) -> str:
    if intent == "add_appointment":
        from assistant_core.modules.appointments import add
        return add.handle(user_input)

    elif intent == "run_script":
        script_name = extract_script_name(user_input)
        return personal_data.run_script(script_name)

    return "Intent not recognized or not implemented."


def extract_script_name(user_input: str) -> str:
    # Simple heuristic — assumes format like: "run script 'schedule_study.py'"
    import re
    match = re.search(r"(?:run|execute)\s+(?:script\s+)?['\"]?([\w\-]+\.py)['\"]?", user_input)
    return match.group(1) if match else "unknown.py"