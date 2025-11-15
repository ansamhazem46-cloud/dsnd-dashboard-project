# python-package/employee_events/employee.py

import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'employee_events.db')

class Employee:
    """Handles employee-level data and metrics."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.df = self.load_data()

    def load_data(self):
        df = pd.read_sql_query("SELECT * FROM employee_events", self.conn)
        df['event_date'] = pd.to_datetime(df['event_date'])
        df['employee_id'] = df['employee_id'].astype(str)
        df['team'] = df['team'].fillna('Unknown')
        df['event_type'] = df['event_type'].fillna('Unknown')
        return df

    def filter_data(self, start_date=None, end_date=None, event_types=None, teams=None):
        filtered = self.df.copy()
        if start_date:
            filtered = filtered[filtered['event_date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[filtered['event_date'] <= pd.to_datetime(end_date)]
        if event_types:
            filtered = filtered[filtered['event_type'].isin(event_types)]
        if teams:
            filtered = filtered[filtered['team'].isin(teams)]
        return filtered

    def total_employees(self, df=None):
        df = df if df is not None else self.df
        return df['employee_id'].nunique()

    def total_events(self, df=None):
        df = df if df is not None else self.df
        return len(df)

    def avg_events_per_employee(self, df=None):
        df = df if df is not None else self.df
        total_emp = self.total_employees(df)
        return self.total_events(df) / total_emp if total_emp else 0

    def top_employees(self, df=None, top_n=10):
        df = df if df is not None else self.df
        top_emp = df.groupby('employee_id').size().sort_values(ascending=False).head(top_n)
        return top_emp.reset_index().rename(columns={'index': 'employee_id', 0: 'event_count'})

    def recent_activity_trend(self, df=None, freq='M'):
        df = df if df is not None else self.df
        trend = df.set_index('event_date').groupby(pd.Grouper(freq=freq)).size()
        return trend.reset_index().rename(columns={'event_date': 'date', 0: 'event_count'})

    def close_connection(self):
        self.conn.close()
