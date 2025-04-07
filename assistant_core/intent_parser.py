#!/usr/bin/env python3

import re
import dateparser 
import os
import yaml
from assistant_core.load_intents import load_all_intents
from datetime import datetime, timedelta, timezone



# Load the dictionary at module load, or you can do so in build_assistant()
INTENT_DEFINITIONS = load_all_intents()

def parse_intent(user_text: str) -> dict:
    text_lower = user_text.lower()

    # Try each known intent
    for intent_name, props in INTENT_DEFINITIONS.items():
        synonyms = props.get("synonyms", [])
        # If user_text matches any known synonyms, we classify as that intent
        if any(kw in text_lower for kw in synonyms):
            # For example, if 'create_appointment' is found
            if intent_name == "create_appointment":
                times = parse_time_range(user_text)
                fallback_title = props.get("fallback_title", "Untitled")
                if not times.get("title"):
                    times["title"] = fallback_title
                return {
                    "intent": "create_appointment",
                    **times
                }
            elif intent_name == "list_appointments":
                return {
                    "intent": "list_appointments",
                    "upcoming_only": False  # or parse if user says "upcoming"
                }
            elif intent_name == "update_appointment":
                # Attempt a naive parse for "appointment_id"
                match_id = re.search(r"appointment\s+(\d+)", text_lower)
                appt_id = int(match_id.group(1)) if match_id else None
                times = parse_time_range(user_text)
                return {
                    "intent": "update_appointment",
                    "appointment_id": appt_id,
                    **times
                }

    # If we get here, no synonyms matched any known intent
    return {
        "intent": "unknown"
    }


def parse_time_range(user_text: str) -> dict:
    """
    Attempt to parse a time range from user_text like:
      "tomorrow from 9 to 10"
    Return a dict with 'start_time_str' and 'end_time_str' if found,
    or a single time if no 'from ... to ...' match is found.
    """
    # Define dateparser settings for consistent handling of "tomorrow," etc.
    parser_settings = {
        "TIMEZONE": "UTC",
        "RETURN_AS_TIMEZONE_AWARE": False,
        # So "tomorrow" references actual 'today' in UTC
        "RELATIVE_BASE": datetime.now(timezone.utc)
    }

    # 1) Try to find "from X to Y" in user_text
    match = re.search(r"(?:from|at)\s+(.*?)\s+(?:to|till)\s+(\S+)", user_text.lower())
    if match:
        raw_start = match.group(1)
        raw_end = match.group(2)

        start_parsed = dateparser.parse(raw_start, settings=parser_settings)
        end_parsed = dateparser.parse(raw_end, settings=parser_settings)

        start_str = start_parsed.strftime("%Y-%m-%d %H:%M:%S") if start_parsed else ""
        end_str = end_parsed.strftime("%Y-%m-%d %H:%M:%S") if end_parsed else ""

        return {
            "start_time_str": start_str,
            "end_time_str": end_str
        }

    # 2) Fallback: parse a single time from entire text
    dt = dateparser.parse(user_text, settings=parser_settings)
    if dt:
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "start_time_str": time_str,
            "end_time_str": ""
        }
    else:
        # No valid time found
        return {
            "start_time_str": "",
            "end_time_str": ""
        }