#!/usr/bin/env python3
"""
handlers.py (for appointments)

Intent handler functions for:
- create_appointment
- list_appointments
- update_appointment

They call the domain logic from domain.py.
"""

from assistant_core.modules.appointments.domain import (
    create_appointment,
    list_appointments,
    update_appointment
)

def handle_create_appointment(parsed_data: dict) -> str:
    """
    Handler for 'create_appointment' intent.
    Expects parsed_data with:
    - title (str)
    - start_time_str (str)
    - end_time_str (str)
    """
    if parsed_data.get("needs_clarification"):
        return parsed_data["clarification_prompt"]
    title = parsed_data.get("title", "Untitled")
    start_str = parsed_data.get("start_time_str", "")
    end_str = parsed_data.get("end_time_str", "")

    try:
        appt_id = create_appointment(title, start_str, end_str)
        return (
            f"Created appointment ID {appt_id} for '{title}'\n"
            f"From {start_str} to {end_str}"
        )
    except ValueError as e:
        return f"Error creating appointment: {e}"

def handle_list_appointments(parsed_data: dict) -> str:
    """
    Handler for 'list_appointments' intent.
    Optionally checks if we only want upcoming appointments.
    """
    upcoming = parsed_data.get("upcoming_only", False)
    rows = list_appointments(upcoming_only=upcoming)
    if not rows:
        return "No appointments found."

    result = "Your appointments:\n"
    for row in rows:
        appt_id, title, start_time, end_time, location, desc, created_at, updated_at = row
        result += f"- ID {appt_id}: {title} from {start_time} to {end_time}\n"
    return result

def handle_update_appointment(parsed_data: dict) -> str:
    """
    Handler for 'update_appointment' intent.
    Expects:
    - appointment_id (int)
    - start_time_str (str), end_time_str (str)
    """
    appt_id = parsed_data.get("appointment_id")
    if not appt_id:
        return "Please specify an appointment ID to update."

    start_str = parsed_data.get("start_time_str", "")
    end_str = parsed_data.get("end_time_str", "")

    try:
        success = update_appointment(
            appointment_id=appt_id,
            start_time_str=start_str,
            end_time_str=end_str
        )
        if success:
            return f"Appointment {appt_id} updated to {start_str} - {end_str}."
        else:
            return f"Appointment {appt_id} not found or no changes made."
    except ValueError as e:
        return f"Error updating appointment: {e}"
