#!/usr/bin/env python3
"""
intents.py

An expanded approach that:
1) Detects 'create', 'list', or 'update' appointments from user_text
2) Extracts date/time ranges like "tomorrow from 9 to 10"
"""

import re
import dateparser

def parse_intent(user_text: str) -> dict:
    text_lower = user_text.lower()

    # 1) Check if user wants to list appointments
    if any(kw in text_lower for kw in ["list appointments", "show appointments"]):
        return {"intent": "list_appointments"}

    # 2) Check if user wants to update appointment
    #    e.g., "Update appointment 3 from tomorrow 9 to 10"
    if "update" in text_lower and "appointment" in text_lower:
        # parse appointment ID with a naive approach: "update appointment 3 ..."
        match_id = re.search(r"appointment\s+(\d+)", text_lower)
        appt_id = int(match_id.group(1)) if match_id else None

        times = parse_time_range(user_text)
        return {
            "intent": "update_appointment",
            "appointment_id": appt_id,
            **times
        }

    # 3) Otherwise assume 'create' if "schedule" or "appointment" or "from" appears
    if any(kw in text_lower for kw in ["schedule", "appointment", "meeting"]):
        times = parse_time_range(user_text)
        return {
            "intent": "create_appointment",
            "title": extract_title(user_text, times),
            **times
        }

    # 4) Fallback
    return {
        "intent": "unknown",
        "message": "No known intent recognized."
    }

def parse_time_range(user_text: str) -> dict:
    """
    Attempt to parse a time range from user_text like "tomorrow from 9 to 10."
    Return a dict with start_time_str, end_time_str if found, or single time if not found.
    """
    # naive approach: look for "from X to Y"
    match = re.search(r"from\s+(.*?)\s+to\s+(\S+)", user_text.lower())
    if match:
        raw_start = match.group(1)
        raw_end = match.group(2)
        start_parsed = dateparser.parse(raw_start)
        end_parsed = dateparser.parse(raw_end)
        start_str = start_parsed.strftime("%Y-%m-%d %H:%M:%S") if start_parsed else ""
        end_str = end_parsed.strftime("%Y-%m-%d %H:%M:%S") if end_parsed else ""
        return {
            "start_time_str": start_str,
            "end_time_str": end_str,
        }

    # fallback: parse a single time from entire text
    dt = dateparser.parse(user_text)
    time_str = dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""
    return {
        "start_time_str": time_str,
        "end_time_str": "",  # no second time found
    }

def extract_title(user_text: str, times_dict: dict) -> str:
    """
    Attempt to guess a title by removing known time phrases from user_text.
    Very naive approach.
    """
    text_clean = user_text
    for k in ["from ", " to ", "tomorrow", "today", "schedule", "appointment", "meeting"]:
        text_clean = text_clean.replace(k, "")
    if times_dict.get("start_time_str"):
        text_clean = re.sub(times_dict["start_time_str"], "", text_clean, flags=re.IGNORECASE)
    if times_dict.get("end_time_str"):
        text_clean = re.sub(times_dict["end_time_str"], "", text_clean, flags=re.IGNORECASE)
    return text_clean.strip().title()