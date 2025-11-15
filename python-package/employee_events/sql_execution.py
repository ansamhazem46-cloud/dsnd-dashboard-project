# python-package/employee_events/sql_execution.py

import pandas as pd
from .query_base import QueryBase

class SqlExecution(QueryBase):
    """Class for executing queries and returning results as pandas DataFrames."""

    def __init__(self):
        super().__init__()

    def to_df(self, sql: str, params: tuple = ()):
        """
        Execute a SQL query and convert the result into a pandas DataFrame.
        :param sql: SQL query string
        :param params: tuple of parameters
        :return: pandas.DataFrame
        """
        rows = self.execute(sql, params)
        if not rows:
            return pd.DataFrame()
        # Convert sqlite3.Row list to list of dicts
        data = [dict(row) for row in rows]
        return pd.DataFrame(data)

    def fetch_all_events(self):
        """Get all rows from employee_events table."""
        sql = "SELECT * FROM employee_events"
        return self.to_df(sql)

    def fetch_events_by_employee(self, employee_id: int):
        """Get all events for a given employee."""
        sql = "SELECT * FROM employee_events WHERE employee_id = ?"
        return self.to_df(sql, (employee_id,))

    def fetch_events_by_team(self, team_id: int):
        """Get all events for a given team."""
        sql = "SELECT * FROM employee_events WHERE team_id = ?"
        return self.to_df(sql, (team_id,))
