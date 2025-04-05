#!/usr/bin/env python3
"""
handlers/appointments.py

Intent handler functions for appointment management.
"""

from scripts.appointments.appointments import (
    create_appointment, list_appointments, update_appointment
)

def handle_create_appointment(parsed_data: dict) -> str:
    title = parsed_data.get("title", "Untitled")
    start_str = parsed_data.get("start_time_str", "")
    end_str = parsed_data.get("end_time_str", "")
    try:
        appt_id = create_appointment(title, start_str, end_str)
        return f"Created appointment ID {appt_id} for '{title}' from {start_str} to {end_str}"
    except ValueError as e:
        # handle conflict or parse error
        return f"Error creating appointment: {e}"

def handle_list_appointments(parsed_data: dict) -> str:
    upcoming = parsed_data.get("upcoming_only", False)
    rows = list_appointments(upcoming_only=upcoming)
    if not rows:
        return "No appointments found."
    result = "Your appointments:\n"
    for row in rows:
        appt_id, title, start_time, end_time, *_ = row
        result += f"- ID {appt_id}: {title} from {start_time} to {end_time}\n"
    return result

def handle_update_appointment(parsed_data: dict) -> str:
    appt_id = parsed_data.get("appointment_id")
    start_str = parsed_data.get("start_time_str", "")
    end_str = parsed_data.get("end_time_str", "")
    if not appt_id:
        return "Please specify an appointment ID to update."

    try:
        success = update_appointment(appt_id, start_time_str=start_str, end_time_str=end_str)
        if success:
            return f"Appointment {appt_id} updated to {start_str} - {end_str}."
        else:
            return f"Appointment {appt_id} not found."
    except ValueError as e:
        return f"Error updating appointment: {e}"
