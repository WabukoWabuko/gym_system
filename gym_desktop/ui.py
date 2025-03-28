from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTextEdit, QTableWidget, QTableWidgetItem, QProgressBar, QComboBox, QFrame, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette, QFont
from datetime import datetime
import requests
import sqlite3

class GymUI(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("NexFit 2030")
        self.setGeometry(100, 100, 900, 700)
        self.set_dark_theme()
        self.init_ui()
        self.setup_shortcuts()
        self.update_member_count()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(20, 20, 30))  # Deep space gray
        palette.setColor(QPalette.WindowText, QColor(200, 200, 220))  # Soft white
        palette.setColor(QPalette.Base, QColor(35, 35, 45))  # Slightly lighter gray
        palette.setColor(QPalette.AlternateBase, QColor(50, 50, 60))
        palette.setColor(QPalette.Text, QColor(200, 200, 220))
        palette.setColor(QPalette.Button, QColor(60, 60, 80))  # Muted purple-gray
        palette.setColor(QPalette.ButtonText, QColor(200, 200, 220))
        self.setPalette(palette)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with Gym Name
        header = QLabel("NexFit 2030")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 36px; font-family: 'Arial'; color: #66d9ef; text-shadow: 0 0 5px #66d9ef;")
        layout.addWidget(header)

        # Status Bar (Connectivity & Energy)
        status_layout = QHBoxLayout()
        self.connectivity_label = QLabel("Online")
        self.connectivity_label.setStyleSheet("color: #66d9ef; font-size: 14px;")  # Soft cyan
        status_layout.addWidget(self.connectivity_label)
        
        self.member_count_label = QLabel("Members Present: 0")
        self.member_count_label.setStyleSheet("color: #66d9ef; font-size: 14px;")
        status_layout.addWidget(self.member_count_label)
        
        self.energy_label = QLabel("Energy Saved: 5 kWh")
        self.energy_label.setStyleSheet("color: #66d9ef; font-size: 14px;")
        status_layout.addWidget(self.energy_label)
        
        layout.addLayout(status_layout)

        # Check-in Section
        checkin_frame = QFrame()
        checkin_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2a2a3a, stop:1 #1a1a2a); border-radius: 15px; border: 1px solid #66d9ef;")
        checkin_layout = QHBoxLayout(checkin_frame)
        
        self.member_id_input = QLineEdit()
        self.member_id_input.setPlaceholderText("Enter Member ID")
        self.member_id_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #66d9ef; background: #3a3a4a; color: #c8c8dc;")
        checkin_layout.addWidget(QLabel("Member ID:"))
        checkin_layout.addWidget(self.member_id_input)

        self.member_name_input = QLineEdit()
        self.member_name_input.setReadOnly(True)
        self.member_name_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #66d9ef; background: #3a3a4a; color: #c8c8dc;")
        checkin_layout.addWidget(QLabel("Name:"))
        checkin_layout.addWidget(self.member_name_input)

        checkin_btn = QPushButton("Check In")
        checkin_btn.setStyleSheet("background-color: #66d9ef; padding: 8px; border-radius: 5px; border: 1px solid #66d9ef; color: #1a1a2a;")
        checkin_btn.clicked.connect(self.check_in)
        checkin_layout.addWidget(checkin_btn)

        voice_btn = QPushButton("Voice Check-in (Future)")
        voice_btn.setStyleSheet("background-color: #4a4a5a; padding: 8px; border-radius: 5px; border: 1px solid #66d9ef; color: #c8c8dc;")
        voice_btn.setEnabled(False)
        checkin_layout.addWidget(voice_btn)

        layout.addWidget(checkin_frame)

        # Schedules Section
        schedules_frame = QFrame()
        schedules_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2a2a3a, stop:1 #1a1a2a); border-radius: 15px; border: 1px solid #66d9ef;")
        schedules_layout = QVBoxLayout(schedules_frame)
        
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(["Title", "Instructor", "Start Time", "End Time", "Action"])
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.setStyleSheet("border-radius: 5px; background: #3a3a4a; color: #c8c8dc; selection-background-color: #66d9ef;")
        schedules_layout.addWidget(QLabel("Schedules"))
        schedules_layout.addWidget(self.schedule_table)
        
        refresh_layout = QHBoxLayout()
        refresh_btn = QPushButton("Refresh Schedules")
        refresh_btn.setStyleSheet("background-color: #66d9ef; padding: 8px; border-radius: 5px; border: 1px solid #66d9ef; color: #1a1a2a;")
        refresh_btn.clicked.connect(self.refresh_schedules)
        refresh_layout.addWidget(refresh_btn)
        
        self.refresh_progress = QProgressBar()
        self.refresh_progress.setVisible(False)
        self.refresh_progress.setStyleSheet("QProgressBar { border: 1px solid #66d9ef; border-radius: 5px; background: #3a3a4a; } QProgressBar::chunk { background: #66d9ef; }")
        refresh_layout.addWidget(self.refresh_progress)
        
        schedules_layout.addLayout(refresh_layout)
        layout.addWidget(schedules_frame)

        # History Section
        history_frame = QFrame()
        history_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2a2a3a, stop:1 #1a1a2a); border-radius: 15px; border: 1px solid #66d9ef;")
        history_layout = QVBoxLayout(history_frame)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Member Name", "Check-in Time", "Checkout Time", "Status", "Action"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setStyleSheet("border-radius: 5px; background: #3a3a4a; color: #c8c8dc; selection-background-color: #66d9ef;")
        history_layout.addWidget(QLabel("Check-in History"))
        history_layout.addWidget(self.history_table)
        
        layout.addWidget(history_frame)

        # Sync & Settings
        controls_layout = QHBoxLayout()
        sync_btn = QPushButton("Sync with Server")
        sync_btn.setStyleSheet("background-color: #66d9ef; padding: 8px; border-radius: 5px; border: 1px solid #66d9ef; color: #1a1a2a;")
        sync_btn.clicked.connect(self.sync_data)
        controls_layout.addWidget(sync_btn)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        self.theme_combo.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid #66d9ef; background: #3a3a4a; color: #c8c8dc;")
        controls_layout.addWidget(self.theme_combo)
        
        layout.addLayout(controls_layout)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("border-radius: 5px; border: 1px solid #66d9ef; background: #3a3a4a; color: #c8c8dc;")
        layout.addWidget(self.status_text)

        self.update_schedules()
        self.update_history()

    def setup_shortcuts(self):
        self.member_id_input.returnPressed.connect(self.check_in)
        self.shortcut_sync = QTimer.singleShot(0, lambda: self.sync_data())
        self.shortcut_refresh = QTimer.singleShot(0, lambda: self.refresh_schedules())
        self.shortcut_theme = QTimer.singleShot(0, lambda: self.theme_combo.setCurrentIndex(1 - self.theme_combo.currentIndex()))

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_S:
                self.sync_data()
            elif event.key() == Qt.Key_R:
                self.refresh_schedules()
            elif event.key() == Qt.Key_T:
                self.theme_combo.setCurrentIndex(1 - self.theme_combo.currentIndex())

    def check_in(self):
        member_id = self.member_id_input.text()
        if member_id:
            try:
                response = requests.get(f"{self.app.sync_manager.api_base}members/lookup/?id={member_id}", timeout=2)
                self.connectivity_label.setText("Online")
                self.connectivity_label.setStyleSheet("color: #66d9ef; font-size: 14px;")
                if response.status_code == 200:
                    member_data = response.json()
                    member_name = member_data['name']
                    self.member_name_input.setText(member_name)
                    self.app.db.add_checkin(member_id, member_name)
                    self.status_text.append(f"Checked in: {member_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    self.status_text.append(f"DEBUG: Stored member_id={member_id}")
                    self.update_history()
                    self.update_member_count()
                else:
                    self.status_text.append(f"Lookup failed: {response.json().get('error', 'Unknown error')}")
                    self.offline_checkin(member_id)
            except requests.exceptions.RequestException:
                self.connectivity_label.setText("Offline")
                self.connectivity_label.setStyleSheet("color: #ff5555; font-size: 14px;")
                self.offline_checkin(member_id)
            self.member_id_input.clear()
        else:
            self.status_text.append("Error: Enter Member ID.")

    def offline_checkin(self, member_id):
        member_name = self.member_name_input.text() or "Unknown"
        self.app.db.add_checkin(member_id, member_name)
        self.status_text.append(f"Offline check-in: {member_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (sync later)")
        self.status_text.append(f"DEBUG: Stored member_id={member_id}")
        self.update_history()
        self.update_member_count()

    def sync_data(self):
        checkin_result = self.app.sync_manager.sync_checkins()
        schedule_result = self.app.sync_manager.fetch_schedules()
        self.status_text.append(checkin_result)
        self.status_text.append(schedule_result)
        self.update_schedules()
        self.update_history()
        self.update_member_count()

    def refresh_schedules(self):
        self.refresh_progress.setVisible(True)
        self.refresh_progress.setRange(0, 0)
        QTimer.singleShot(1000, self._finish_refresh)

    def _finish_refresh(self):
        schedule_result = self.app.sync_manager.fetch_schedules()
        self.status_text.append(schedule_result)
        self.update_schedules()
        self.refresh_progress.setVisible(False)

    def update_schedules(self):
        self.schedule_table.setRowCount(0)
        schedules = self.app.db.get_schedules()
        self.schedule_table.setRowCount(len(schedules))
        for row, schedule in enumerate(schedules):
            _, title, instructor, start_time, end_time = schedule
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            formatted_start = start_dt.strftime('%Y-%m-%d %H:%M')
            formatted_end = end_dt.strftime('%Y-%m-%d %H:%M')
            
            self.schedule_table.setItem(row, 0, QTableWidgetItem(title))
            self.schedule_table.setItem(row, 1, QTableWidgetItem(instructor))
            self.schedule_table.setItem(row, 2, QTableWidgetItem(formatted_start))
            self.schedule_table.setItem(row, 3, QTableWidgetItem(formatted_end))
            
            join_btn = QPushButton("Notify Me")
            join_btn.setStyleSheet("background-color: #66d9ef; padding: 5px; border-radius: 5px; border: 1px solid #66d9ef; color: #1a1a2a;")
            join_btn.clicked.connect(lambda _, t=title: self.notify_me(t))
            self.schedule_table.setCellWidget(row, 4, join_btn)

    def notify_me(self, title):
        self.status_text.append(f"Notification set for {title} (simulated).")

    def update_history(self):
        self.history_table.setRowCount(0)
        conn = sqlite3.connect("gym_local.db")
        c = conn.cursor()
        c.execute("SELECT member_id, member_name, timestamp, checkout_time, synced FROM checkins ORDER BY timestamp DESC LIMIT 50")
        checkins = c.fetchall()
        self.history_table.setRowCount(len(checkins))
        for row, (member_id, name, timestamp, checkout_time, synced) in enumerate(checkins):
            status = "Synced" if synced else "Pending"
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            checkout_display = checkout_time if checkout_time else "-"
            if checkout_time:
                checkout_dt = datetime.fromisoformat(checkout_time.replace('Z', '+00:00'))
                checkout_display = checkout_dt.strftime('%Y-%m-%d %H:%M:%S')
            
            self.history_table.setItem(row, 0, QTableWidgetItem(name))
            self.history_table.setItem(row, 1, QTableWidgetItem(formatted_time))
            self.history_table.setItem(row, 2, QTableWidgetItem(checkout_display))
            self.history_table.setItem(row, 3, QTableWidgetItem(status))
            
            if not checkout_time:
                checkout_btn = QPushButton("Checkout")
                checkout_btn.setStyleSheet("background-color: #ff5555; padding: 5px; border-radius: 5px; border: 1px solid #66d9ef; color: #1a1a2a;")
                checkout_btn.clicked.connect(lambda _, m=member_id, t=timestamp: self.checkout(m, t))
                self.history_table.setCellWidget(row, 4, checkout_btn)
            else:
                self.history_table.setItem(row, 4, QTableWidgetItem("Done"))

    def checkout(self, member_id, timestamp):
        checkout_time = self.app.db.add_checkout(member_id, timestamp)
        self.status_text.append(f"Checked out: {member_id} at {checkout_time}")
        self.update_history()
        self.update_member_count()

    def update_member_count(self):
        conn = sqlite3.connect("gym_local.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM checkins WHERE checkout_time IS NULL")
        count = c.fetchone()[0]
        self.member_count_label.setText(f"Members Present: {count}")
        conn.close()

    def change_theme(self, theme):
        if theme == "Light":
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(220, 220, 220))
            palette.setColor(QPalette.ButtonText, Qt.black)
            self.setPalette(palette)
        else:
            self.set_dark_theme()

    def closeEvent(self, event):
        self.app.db.close()
        event.accept()
