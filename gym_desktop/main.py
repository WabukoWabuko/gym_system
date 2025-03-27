import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget
from PyQt5.QtCore import Qt
from database import GymDatabase
from sync import SyncManager
from datetime import datetime  # Added this import

class GymApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gym Desktop App")
        self.setGeometry(100, 100, 600, 400)

        self.db = GymDatabase()
        self.sync_manager = SyncManager(self.db)
        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Check-in section
        checkin_layout = QHBoxLayout()
        layout.addLayout(checkin_layout)

        checkin_layout.addWidget(QLabel("Member ID:"))
        self.member_id_input = QLineEdit()
        checkin_layout.addWidget(self.member_id_input)

        checkin_layout.addWidget(QLabel("Name:"))
        self.member_name_input = QLineEdit()
        checkin_layout.addWidget(self.member_name_input)

        checkin_btn = QPushButton("Check In")
        checkin_btn.clicked.connect(self.check_in)
        checkin_layout.addWidget(checkin_btn)

        # Schedules list
        self.schedule_list = QListWidget()
        layout.addWidget(QLabel("Schedules"))
        layout.addWidget(self.schedule_list)
        self.update_schedules()

        # Sync button and status
        sync_btn = QPushButton("Sync with Server")
        sync_btn.clicked.connect(self.sync_data)
        layout.addWidget(sync_btn)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)

    def check_in(self):
        member_id = self.member_id_input.text()
        member_name = self.member_name_input.text()
        if member_id and member_name:
            self.db.add_checkin(member_id, member_name)
            self.status_text.append(f"Checked in: {member_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.member_id_input.clear()
            self.member_name_input.clear()
        else:
            self.status_text.append("Error: Enter both Member ID and Name.")

    def sync_data(self):
        checkin_result = self.sync_manager.sync_checkins()
        schedule_result = self.sync_manager.fetch_schedules()
        self.status_text.append(checkin_result)
        self.status_text.append(schedule_result)
        self.update_schedules()

    def update_schedules(self):
        self.schedule_list.clear()
        schedules = self.db.get_schedules()
        for schedule in schedules:
            _, title, instructor, start_time, end_time = schedule
            self.schedule_list.addItem(f"{title} - {instructor} ({start_time} to {end_time})")

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GymApp()
    window.show()
    sys.exit(app.exec_())
