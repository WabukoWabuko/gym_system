import sys
from PyQt5.QtWidgets import QApplication
from database import GymDatabase
from sync import SyncManager
from ui import GymUI

class GymApp:
    def __init__(self):
        self.db = GymDatabase()
        self.sync_manager = SyncManager(self.db)
        self.app = QApplication(sys.argv)
        self.ui = GymUI(self)
        self.ui.show()
    
    def run(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    app = GymApp()
    app.run()
