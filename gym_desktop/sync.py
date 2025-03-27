import requests
from datetime import datetime

class SyncManager:
    def __init__(self, db):
        self.db = db
        self.api_base = "http://localhost:8000/api/"

    def sync_checkins(self):
        unsynced = self.db.get_unsynced_checkins()
        if not unsynced:
            return "No check-ins to sync."

        try:
            for checkin in unsynced:
                checkin_id, member_id, member_name, timestamp = checkin
                payload = {
                    "member": member_id,
                    "timestamp": timestamp,
                    "synced": True
                }
                response = requests.post(f"{self.api_base}checkins/", json=payload)
                if response.status_code == 201:
                    self.db.mark_checkin_synced(checkin_id)
            return "Check-ins synced successfully!"
        except requests.RequestException as e:
            return f"Sync failed: {str(e)}"

    def fetch_schedules(self):
        try:
            response = requests.get(f"{self.api_base}schedules/")
            if response.status_code == 200:
                schedules = response.json()
                self.db.update_schedules(schedules)
                return "Schedules updated!"
            return "Failed to fetch schedules."
        except requests.RequestException as e:
            return f"Fetch failed: {str(e)}"
