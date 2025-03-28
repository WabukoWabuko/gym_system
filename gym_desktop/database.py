import sqlite3
from datetime import datetime

class GymDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("gym_local.db")
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS checkins
                     (member_id TEXT, member_name TEXT, timestamp TEXT, checkout_time TEXT, synced INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS schedules
                     (id INTEGER PRIMARY KEY, title TEXT, instructor TEXT, start_time TEXT, end_time TEXT)''')
        self.conn.commit()

    def add_checkin(self, member_id, member_name):
        timestamp = datetime.now().isoformat()
        c = self.conn.cursor()
        c.execute("INSERT INTO checkins (member_id, member_name, timestamp, checkout_time, synced) VALUES (?, ?, ?, ?, 0)",
                  (member_id, member_name, timestamp, None))
        self.conn.commit()

    def add_checkout(self, member_id, timestamp):
        checkout_time = datetime.now().isoformat()
        c = self.conn.cursor()
        c.execute("UPDATE checkins SET checkout_time = ? WHERE member_id = ? AND timestamp = ? AND checkout_time IS NULL",
                  (checkout_time, member_id, timestamp))
        self.conn.commit()
        return checkout_time

    def get_schedules(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM schedules")
        return c.fetchall()

    def close(self):
        self.conn.close()
