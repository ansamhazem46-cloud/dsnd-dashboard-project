# python-package/employee_events/employee.py

import pandas as pd
import sqlite3
import os

# Path to database
DB_PATH = os.path.join(os.path.dirname(__file__), 'employee_events.db')


class Employee:
    """Class to handle employee-level queries and metrics."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.df = self.load_data()

    def load_data(self):
        """Load employee events data from the database and clean it."""
        query = "SELECT * FROM employee_events"
        df = pd.read_sql_query(query, self.conn)

        # Clean and process data
        df['event_date'] = pd.to_datetime(df['event_date'])
        df['employee_id'] = df['employee_id'].astype(str)
        df['team'] = df['team'].fillna('Unknown')
        df['event_type'] = df['event_type'].fillna('Unknown')

        return df

    def total_employees(self):
        """Return total numb
