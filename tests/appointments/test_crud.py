#!/usr/bin/env python3
# Category: Test
# Description: Tests core CRUD operations for the appointment module.
# Details:
# - Verifies appointment creation, listing, updating, and deletion.
# - Uses an in-memory SQLite DB for isolation.
# - Ensures no conflicts occur during testing.

import pytest
import sqlite3
import os
from assistant_core.modules.appointments import domain


# Shared in-memory connection
_shared_conn = sqlite3.connect(":memory:")

def setup_function():
    # Patch the domain's connection function to always return our test conn
    domain.get_connection = lambda: _shared_conn
    domain.init_db()

def teardown_function():
    cur = _shared_conn.cursor()
    cur.execute("DELETE FROM appointments")
    _shared_conn.commit()

# Override the default DB path for testing
TEST_DB = ":memory:"

@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    monkeypatch.setattr(domain, "DB_PATH", TEST_DB)
    domain.init_db()
    # Ensure the appointments table is created
    with domain.get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            )
        """)
    yield
    # No explicit cleanup needed for :memory:

def test_create_appointment():
    appt_id = domain.create_appointment("Test Appt", "2025-05-01 10:00", "2025-05-01 11:00")
    assert isinstance(appt_id, int)

def test_list_appointments():
    domain.create_appointment("A1", "2025-05-01 12:00", "2025-05-01 13:00")
    results = domain.list_appointments()
    assert len(results) == 1
    assert results[0][1] == "A1"

def test_update_appointment():
    appt_id = domain.create_appointment("Old Title", "2025-05-02 09:00", "2025-05-02 10:00")
    success = domain.update_appointment(appt_id, title="New Title", start_time_str="2025-05-02 10:00", end_time_str="2025-05-02 11:00")
    assert success
    updated = domain.get_appointment_by_id(appt_id)
    assert updated[1] == "New Title"

def test_delete_appointment():
    appt_id = domain.create_appointment("To Delete", "2025-05-03 08:00", "2025-05-03 09:00")
    deleted = domain.delete_appointment(appt_id)
    assert deleted
    assert domain.get_appointment_by_id(appt_id) is None

def test_conflict_detection():
    domain.create_appointment("Primary", "2025-05-04 10:00", "2025-05-04 11:00")
    with pytest.raises(ValueError):
        domain.create_appointment("Conflict", "2025-05-04 10:30", "2025-05-04 11:30")
