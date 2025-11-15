# python-package/employee_events/team.py

import pandas as pd
import sqlite3
import os

# Path to database
DB_PATH = os.path.join(os.path.dirname(__file__), 'employee_events.db')


class Team:
    """Class to handle team-level queries and metrics."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.df = self.load_data()

    def load_data(self):
        """Load employee events data and clean it."""
        query = "SELECT * FROM employee_events"
        df = pd.read_sql_query(query, self.conn)

        # Clean data
        df['event_date'] = pd.to_datetime(df['event_date'])
        df['team'] = df['team'].fillna('Unknown')
        df['event_type'] = df['event_type'].fillna('Unknown')
        df['employee_id'] = df['employee_id'].astype(str)

        return df

    def total_teams(self):
        """Return total number of unique teams."""
        return self.df['team'].nunique()

    def total_events_by_team(self):
        """Return total number of events per team."""
        team_counts = self.df.groupby('team').size().reset_index()
        team_counts.columns = ['team', 'event_count']
        return team_counts

    def most_active_team(self):
        """Return the team with the most events and the count."""
        team_counts = self.total_events_by_team()
        top_team = team_counts.sort_values(by='event_count', ascending=False).iloc[0]
        return top_team['team'], top_team['event_count']

    def events_by_team_over_time(self, freq='M'):
        """
        Return event counts per team over time.
        freq: 'D' (day), 'M' (month), 'Y' (year)
        """
        df_grouped = self.df.set_index('event_date').groupby(['team', pd.Grouper(freq=freq)]).size()
        df_grouped = df_grouped.reset_index()
        df_grouped.columns = ['team', 'date', 'event_count']
        return df_grouped

    def filter_data(self, start_date=None, end_date=None, teams=None, event_types=None):
        """Filter data based on dates, teams, and event types."""
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

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()


# Example usage:
# team = Team()
# print(team.total_teams())
# print(team.most_active_team())
# team.close_connection()
