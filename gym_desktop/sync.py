import requests
import sqlite3
from datetime import datetime

class SyncManager:
    def __init__(self, db):
        self.db = db
        self.api_base = "http://localhost:8000/api/"

    def sync_checkins(self):
        conn = sqlite3.connect("gym_local.db")
        c = conn.cursor()
        c.execute("SELECT member_id, member_name, timestamp, checkout_time FROM checkins WHERE synced = 0")
        unsynced_checkins = c.fetchall()
        
        if not unsynced_checkins:
            return "No check-ins to sync."

        result = ""
        for member_id, member_name, timestamp, checkout_time in unsynced_checkins:
            data = {
                "member_id": member_id,
                "timestamp": timestamp,
                "checkout_time": checkout_time,  # Added
                "synced": True
            }
            try:
                response = requests.post(f"{self.api_base}checkins/", json=data)
                response.raise_for_status()
                c.execute(
                    "UPDATE checkins SET synced = 1 WHERE member_id = ? AND timestamp = ?",
                    (member_id, timestamp),
                )
                result += f"Check-in synced successfully for {member_name}!\n"
            except requests.exceptions.RequestException as e:
                error_message = e.response.text if e.response is not None else str(e)
                result += f"Sync failed for {member_name}: {error_message} (Status: {e.response.status_code if e.response else 'No response'})\n"
        
        conn.commit()
        conn.close()
        return result.strip()

    def fetch_schedules(self):
        try:
            response = requests.get(f"{self.api_base}schedules/")
            response.raise_for_status()
            schedules = response.json()
            conn = sqlite3.connect("gym_local.db")
            c = conn.cursor()
            c.execute("DELETE FROM schedules")
            for schedule in schedules:
                c.execute(
                    "INSERT OR REPLACE INTO schedules (id, title, instructor, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
                    (
                        schedule["id"],
                        schedule["title"],
                        schedule["instructor"],
                        schedule["start_time"],
                        schedule["end_time"],
                    ),
                )
            conn.commit()
            conn.close()
            return "Schedules updated!"
        except requests.exceptions.RequestException as e:
            return f"Failed to sync schedules: {e}"
