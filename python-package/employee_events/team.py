# python-package/employee_events/team.py

import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'employee_events.db')

class Team:
    """Handles team-level data and metrics."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.df = self.load_data()

    def load_data(self):
        df = pd.read_sql_query("SELECT * FROM employee_events", self.conn)
        df['event_date'] = pd.to_datetime(df['event_date'])
        df['team'] = df['team'].fillna('Unknown')
        df['event_type'] = df['event_type'].fillna('Unknown')
        df['employee_id'] = df['employee_id'].astype(str)
        return df

    def filter_data(self, start_date=None, end_date=None, teams=None, event_types=None):
        filtered = self.df.copy()
        if start_date:
            filtered = filtered[filtered['event_date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[filtered['event_date'] <= pd.to_datetime(end_date)]
        if teams:
            filtered = filtered[filtered['team'].isin(teams)]
        if event_types:
            filtered = filtered[filtered['event_type'].isin(event_types)]
        return filtered

    def total_teams(self, df=None):
        df = df if df is not None else self.df
        return df['team'].nunique()

    def total_events_by_team(self, df=None):
        df = df if df is not None else self.df
        team_counts = df.groupby('team').size().reset_index(name='event_count')
        return team_counts

    def most_active_team(self, df=None):
        df = df if df is not None else self.df
        team_counts = self.total_events_by_team(df)
        top = team_counts.sort_values(by='event_count', ascending=False).iloc[0]
        return top['team'], top['event_count']

    def events_by_team_over_time(self, df=None, freq='M'):
        df = df if df is not None else self.df
        trend = df.set_index('event_date').groupby(['team', pd.Grouper(freq=freq)]).size()
        trend_df = trend.reset_index().rename(columns={0: 'event_count'})
        return trend_df

    def close_connection(self):
        self.conn.close()
