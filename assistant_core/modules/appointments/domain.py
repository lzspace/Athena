#!/usr/bin/env python3
"""
domain.py (for appointments)

Provides the low-level appointment logic:
- SQLite DB
- dateparser
- conflict checks
- CRUD operations

Used by handlers.py for higher-level logic in the assistant.
"""

import sqlite3
import sys
import datetime
import dateparser

# If you want consistent dateparser settings for "tomorrow", use this:
parser_settings = {
    'TIMEZONE': 'UTC',
    'RETURN_AS_TIMEZONE_AWARE': False,
    'RELATIVE_BASE': datetime.datetime.now(datetime.timezone.utc)
}

DB_PATH = "appointments.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    location TEXT,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Create the 'appointments' table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute(CREATE_TABLE_SQL)
    print(f"Database '{DB_PATH}' initialized with 'appointments' table.")

def parse_date(date_str: str) -> str:
    """
    Use dateparser to interpret date_str (e.g. 'tomorrow 9am').
    Convert to UTC-based naive string: 'YYYY-MM-DD HH:MM:SS'.
    """
    if not date_str:
        return ""
    dt = dateparser.parse(date_str, settings=parser_settings)
    if not dt:
        raise ValueError(f"Could not parse date/time from '{date_str}'.")
    # Convert to UTC
    utc_dt = dt.astimezone(datetime.timezone.utc)
    return utc_dt.strftime("%Y-%m-%d %H:%M:%S")

# -------------------
# Conflict Checking
# -------------------
def has_conflict(new_start, new_end, exclude_id=None) -> bool:
    """Return True if an existing appointment overlaps [new_start, new_end)."""
    with get_connection() as conn:
        cur = conn.cursor()
        sql = """
            SELECT COUNT(*) FROM appointments
            WHERE NOT (
                end_time <= :newStart
                OR
                start_time >= :newEnd
            )
        """
        params = {"newStart": new_start, "newEnd": new_end}
        if exclude_id:
            sql += " AND id != :excludeId"
            params["excludeId"] = exclude_id

        cur.execute(sql, params)
        (count,) = cur.fetchone()
        return count > 0

# -------------------
# CRUD
# -------------------
def create_appointment(title, start_time_str, end_time_str,
                       location=None, description=None,
                       ignore_conflict=False):
    """
    Insert a new appointment. Returns the new ID.
    """
    start_time = parse_date(start_time_str)
    end_time   = parse_date(end_time_str)

    if end_time and start_time and end_time <= start_time:
        raise ValueError("end_time must be after start_time")

    if not ignore_conflict and start_time and end_time:
        if has_conflict(start_time, end_time):
            raise ValueError(f"Conflict detected with existing appointments between {start_time} and {end_time}")

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO appointments (title, start_time, end_time, location, description)
            VALUES (?, ?, ?, ?, ?)
        """, (title, start_time, end_time, location, description))
        conn.commit()
        return cur.lastrowid

def list_appointments(upcoming_only=False):
    with get_connection() as conn:
        cur = conn.cursor()
        if upcoming_only:
            now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("""
                SELECT id, title, start_time, end_time, location, description, created_at, updated_at
                FROM appointments
                WHERE start_time >= ?
                ORDER BY start_time ASC
            """, (now_str,))
        else:
            cur.execute("""
                SELECT id, title, start_time, end_time, location, description, created_at, updated_at
                FROM appointments
                ORDER BY start_time ASC
            """)
        return cur.fetchall()

def get_appointment_by_id(appointment_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, start_time, end_time, location, description, created_at, updated_at
            FROM appointments
            WHERE id=?
        """, (appointment_id,))
        return cur.fetchone()

def update_appointment(appointment_id,
                       title=None,
                       start_time_str=None,
                       end_time_str=None,
                       location=None,
                       description=None,
                       ignore_conflict=False):
    """Update an existing appointment's fields. Returns True if updated."""
    existing = get_appointment_by_id(appointment_id)
    if not existing:
        raise ValueError(f"Appointment {appointment_id} not found")

    old_title, old_start, old_end = existing[1], existing[2], existing[3]

    new_title = title if title is not None else old_title
    new_start = parse_date(start_time_str) if start_time_str else old_start
    new_end   = parse_date(end_time_str)   if end_time_str   else old_end

    # check conflict
    if not ignore_conflict and new_start and new_end:
        if has_conflict(new_start, new_end, exclude_id=appointment_id):
            raise ValueError(f"Conflict detected updating appointment {appointment_id}")

    updated_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    fields = ["title=?", "start_time=?", "end_time=?", "updated_at=?"]
    params = [new_title, new_start, new_end, updated_at]

    if location is not None:
        fields.append("location=?")
        params.append(location)
    if description is not None:
        fields.append("description=?")
        params.append(description)

    sql = f"UPDATE appointments SET {', '.join(fields)} WHERE id=?"
    params.append(appointment_id)

    with get_connection() as conn:
        cur = conn.cursor()
        res = cur.execute(sql, params)
        conn.commit()
        return res.rowcount > 0

def delete_appointment(appointment_id):
    with get_connection() as conn:
        cur = conn.cursor()
        res = cur.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        conn.commit()
        return res.rowcount > 0

# ---------------------------------------
# CLI usage for direct domain testing
# ---------------------------------------
def usage():
    print("Usage:")
    print("  python3 domain.py init")
    print("  python3 domain.py list [--upcoming]")
    print('  python3 domain.py create "Title" "start" "end" [--ignore-conflict]')
    print("  python3 domain.py delete <id>")

if __name__ == "__main__":
    # optional CLI interface for quick testing
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "init":
        init_db()

    elif cmd == "list":
        upcoming = "--upcoming" in sys.argv
        rows = list_appointments(upcoming_only=upcoming)
        for row in rows:
            print(row)

    elif cmd == "create":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        title = sys.argv[2]
        start_str = sys.argv[3]
        end_str = sys.argv[4]
        ignore_conflict = "--ignore-conflict" in sys.argv
        try:
            appt_id = create_appointment(title, start_str, end_str, ignore_conflict=ignore_conflict)
            print(f"Created appointment id {appt_id}")
        except ValueError as e:
            print(f"Error: {e}")

    elif cmd == "delete":
        if len(sys.argv) < 3:
            usage()
            sys.exit(1)
        appt_id = sys.argv[2]
        ok = delete_appointment(appt_id)
        if ok:
            print(f"Appointment {appt_id} deleted.")
        else:
            print(f"Appointment {appt_id} not found or delete failed.")
    else:
        usage()
