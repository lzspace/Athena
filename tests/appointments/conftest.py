import pytest
import sqlite3
from assistant_core.modules.appointments.domain import init_db
from assistant_core.modules.appointments.domain import DB_PATH

@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    """
    Automatically replaces the DB path with a temporary test DB for each test.
    Ensures test isolation and prevents data leaks across tests.
    """
    test_db_path = tmp_path / "test_appointments.db"

    # Patch the global DB path used by the module
    monkeypatch.setattr("assistant_core.modules.appointments.domain.DB_PATH", str(test_db_path))

    # Create a clean DB schema
    init_db()

    yield  # test runs here