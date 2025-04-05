"""
<<<<<<< HEAD
You are an intent classification assistant. Based on what the user says, respond with **only** the intent name.

Available intents:
- add_appointment
- delete_appointment
- list_appointments
- run_script

Examples:
User: "Schedule a meeting tomorrow at 10"
Intent: add_appointment

User: "Remove my lunch reminder"
Intent: delete_appointment

User: "What appointments do I have today?"
Intent: list_appointments

User: "Run script schedule_study.py"
Intent: run_script

Now classify this:
User: "{user_input}"
Intent:
"""

def entity_extraction_prompt(user_input: str) -> str:
    return f"""
Extract the following fields from the user input:
- title
- start_time
- end_time (optional)
- location (optional)

If something is missing, return it as null.

User input: "{user_input}"

Return as JSON.
"""

INTENT_PROMPT_TEMPLATE = """ Du bist ein KI-Assistent. Deine Aufgabe ist es, die Absicht (Intent) der folgenden Benutzereingabe zu klassifizieren.
Bekannte Intents: {intents}

Benutzereingabe: "{input}"

Gib nur den Intent zurück, der am besten passt. Kein Kommentar, kein Satz, nur der Intent."""

def script_invocation_prompt(user_input: str, script_names: list[str]) -> str:
    scripts_list = "\\n".join(script_names)
    return f"""
You are helping the user run a script from their private script collection.

Available scripts:
{scripts_list}

User input: "{user_input}"

Which script should be run? Respond with only the file name (e.g., schedule_study.py).
=======
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
>>>>>>> 7efa79d (cleaned and refactored, added more tests)
"""