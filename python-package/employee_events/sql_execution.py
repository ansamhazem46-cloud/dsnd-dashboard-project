# python-package/employee_events/sql_execution.py

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'employee_events.db')


class SqlExecution:
    """Helper class to execute SQL queries on the employee_events database."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return a Pandas DataFrame.
        :param query: SQL query string
        :param params: Optional parameters for query
        :return: Pandas DataFrame
        """
        if params is None:
            params = {}

        df = pd.read_sql_query(query, self.conn, params=params)
        return df

    def get_all_employees(self):
        """Return all employee data as DataFrame."""
        query = "SELECT * FROM employee_events"
        return self.execute_query(query)

    def get_events_by_employee(self, employee_id):
        """Return all events for a specific employee."""
        query = "SELECT * FROM employee_events WHERE employee_id = ?"
        return self.execute_query(query, params=(employee_id,))

    def get_events_by_team(self, team):
        """Return all events for a specific team."""
        query = "SELECT * FROM employee_events WHERE team = ?"
        return self.execute_query(query, params=(team,))

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()


# Example usage:
# sql_exec = SqlExecution()
# df_all = sql_exec.get_all_employees()
# df_team = sql_exec.get_events_by_team("Engineering")
# sql_exec.close_connection()
