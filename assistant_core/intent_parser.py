#!/usr/bin/env python3

import re
import dateparser

def parse_intent(user_text: str) -> dict:
    text_lower = user_text.lower()

    # Example logic:
    if "create appointment" in text_lower or "schedule" in text_lower:
        # parse times, title, etc.
        return {
            "intent": "create_appointment",
            "title": "some title from user text",
            "start_time_str": "2025-05-01 09:00:00",
            "end_time_str": "2025-05-01 10:00:00"
        }

    if "list appointments" in text_lower:
        return {
            "intent": "list_appointments",
            "upcoming_only": False
        }

    if "update appointment" in text_lower:
        # parse ID, new times, etc.
        return {
            "intent": "update_appointment",
            "appointment_id": 1,  # extract from user_text
            "start_time_str": "2025-05-02 11:00:00",
            "end_time_str": "2025-05-02 12:00:00"
        }

    return {
        "intent": "unknown"
    }