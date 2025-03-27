import sqlite3
from datetime import datetime

class GymDatabase:
    def __init__(self, db_name="gym_desktop.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT NOT NULL,
                member_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                synced INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                instructor TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_checkin(self, member_id, member_name):
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('INSERT INTO checkins (member_id, member_name, timestamp) VALUES (?, ?, ?)',
                       (member_id, member_name, timestamp))
        self.conn.commit()

    def get_unsynced_checkins(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, member_id, member_name, timestamp FROM checkins WHERE synced = 0')
        return cursor.fetchall()

    def mark_checkin_synced(self, checkin_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE checkins SET synced = 1 WHERE id = ?', (checkin_id,))
        self.conn.commit()

    def update_schedules(self, schedules):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM schedules')  # Clear old data
        for schedule in schedules:
            cursor.execute('INSERT OR REPLACE INTO schedules (id, title, instructor, start_time, end_time) VALUES (?, ?, ?, ?, ?)',
                           (schedule['id'], schedule['title'], schedule['instructor'], schedule['start_time'], schedule['end_time']))
        self.conn.commit()

    def get_schedules(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, instructor, start_time, end_time FROM schedules')
        return cursor.fetchall()

    def close(self):
        self.conn.close()
