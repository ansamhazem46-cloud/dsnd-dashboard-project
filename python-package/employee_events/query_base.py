# python-package/employee_events/query_base.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'employee_events.db')

class QueryBase:
    """Base class for constructing and executing queries against the employee_events DB."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def execute(self, sql: str, params: tuple = ()):
        """
        Execute a SQL statement and return raw rows.
        
        :param sql: SQL query string
        :param params: tuple of parameters
        :return: list of sqlite3.Row
        """
        cur = self.conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return rows

    def close(self):
        """Close the DB connection."""
        self.conn.close()
