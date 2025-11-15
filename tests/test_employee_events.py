import pytest
from pathlib import Path
from sqlite3 import connect

# -------------------- Project Root --------------------
# Using pathlib, create a project_root variable set to the absolute path for the root of this project
project_root = Path(__file__).resolve().parent.parent

# -------------------- Fixtures --------------------
@pytest.fixture
def db_path():
    """
    Fixture that returns the absolute path to the employee_events.db file.
    """
    return project_root / "python_package" / "employee_events" / "employee_events.db"

@pytest.fixture
def db_conn(db_path):
    """
    Fixture that provides a database connection.
    """
    return connect(db_path)

@pytest.fixture
def table_names(db_conn):
    """
    Fixture that retrieves a list of table names from the database.
    """
    name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [x[0] for x in name_tuples]

# -------------------- Database Tests --------------------
def test_db_exists(db_path):
    """
    Test that the SQLite database file exists.
    """
    assert db_path.is_file(), f"Database file not found at {db_path}"

def test_employee_table_exists(table_names):
    """
    Test that the 'employee' table exists in the database.
    """
    assert 'employee' in table_names, "'employee' table does not exist in the database"

def test_team_table_exists(table_names):
    """
    Test that the 'team' table exists in the database.
    """
    assert 'team' in table_names, "'team' table does not exist in the database"

def test_employee_events_table_exists(table_names):
    """
    Test that the 'employee_events' table exists in the database.
    """
    assert 'employee_events' in table_names, "'employee_events' table does not exist in the database"
