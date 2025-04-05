import pytest
import os
import sqlite3
import datetime
from pathlib import Path


# Adjust import if your appointments.py is in scripts/appointments/:
# e.g. from scripts.appointments.appointments import ...
from assistant_core.modules.appointments.domain import (
    CREATE_TABLE_SQL,
    init_db,
    create_appointment,
    list_appointments,
    get_appointment_by_id,
    update_appointment,
    delete_appointment,
    has_conflict,
)

@pytest.fixture
def temp_db(monkeypatch):
    """
    A test fixture that:
    1. Points DB_PATH to 'test_appointments.db'
    2. Calls init_db() to create the appointments table
    3. Yields control to tests
    4. Removes the DB file after tests
    """
    temp_path = "test_appointments.db"

    # Patch the DB_PATH global variable to the temp file:
    monkeypatch.setattr("assistant_core.modules.appointments.domain.DB_PATH", temp_path)

    # Initialize the table:
    init_db()

    yield  # run the tests within this environment

    # Cleanup: remove the file
    if os.path.exists(temp_path):
        os.remove(temp_path)



def test_create_appointment_simple(temp_db):
    """
    Test a simple appointment creation with no conflict.
    """
    appt_id = create_appointment(
        title="Test Meeting",
        start_time_str="tomorrow 10am",
        end_time_str="tomorrow 11am",
    )
    assert appt_id > 0, "Should return a valid appointment ID"

    rows = list_appointments()
    assert len(rows) == 1, "Should have exactly one appointment in DB"
    row = rows[0]
    assert row[1] == "Test Meeting"
    assert "202" in row[2], "start_time should be parsed into an ISO format"


def test_conflict_detection(temp_db):
    """
    Test that conflict detection works by creating a second overlapping appointment.
    """
    # Create first appointment
    appt_id = create_appointment(
        title="First Appt",
        start_time_str="2025-04-29 09:00",
        end_time_str="2025-04-29 10:00",
    )
    assert appt_id > 0

    # Attempt overlap
    with pytest.raises(ValueError, match="Conflict detected"):
        create_appointment(
            title="Overlapping Appt",
            start_time_str="2025-04-29 09:30",
            end_time_str="2025-04-29 10:30",
        )

    # Confirm we still only have one appointment
    rows = list_appointments()
    assert len(rows) == 1


def test_ignore_conflict(temp_db):
    """
    Test that appointments can be forced with --ignore_conflict (pass ignore_conflict=True).
    """
    create_appointment("First Appt", "2025-04-29 09:00", "2025-04-29 10:00")
    # Overlap but ignoring conflict
    appt_id = create_appointment(
        "Overlap Appt",
        "2025-04-29 09:30",
        "2025-04-29 10:30",
        ignore_conflict=True
    )
    assert appt_id > 0
    rows = list_appointments()
    assert len(rows) == 2


def test_update_appointment(temp_db):
    """
    Create, then update an appointment's time, checking for conflicts.
    """
    # Create a valid appointment
    appt_id = create_appointment("Old Title", "April 30 10am", "April 30 11am")
    assert appt_id > 0

    # No conflict update
    success = update_appointment(appt_id, start_time_str="April 30 9am", end_time_str="April 30 9:30am")
    assert success, "Update should succeed"

    # Attempt an update that conflicts with itself? That might not happen
    # but let's create a second appointment that conflicts
    other_id = create_appointment("Second", "April 30 9:30am", "April 30 10am")
    assert other_id > 0

    # Now try to move first appt to overlap with second
    with pytest.raises(ValueError, match="Conflict detected updating appointment"):
        update_appointment(appt_id, start_time_str="April 30 9:15am", end_time_str="April 30 9:45am")


def test_delete_appointment(temp_db):
    """
    Create then delete an appointment.
    """
    appt_id = create_appointment("To delete", "tomorrow 8am", "tomorrow 9am")
    assert appt_id > 0

    # Verify it's there
    rows = list_appointments()
    assert len(rows) == 1

    ok = delete_appointment(appt_id)
    assert ok, "Delete should return True"

    # Verify it's gone
    rows = list_appointments()
    assert len(rows) == 0


def test_get_appointment_by_id(temp_db):
    """
    Create multiple appointments, fetch one by ID.
    """
    a1 = create_appointment("A1", "2025-05-01 9:00", "2025-05-01 10:00")
    a2 = create_appointment("A2", "2025-05-02 13:00", "2025-05-02 14:00")

    # fetch a1
    row = get_appointment_by_id(a1)
    assert row[1] == "A1"

    # fetch a2
    row2 = get_appointment_by_id(a2)
    assert row2[1] == "A2"
