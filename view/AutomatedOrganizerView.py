from PyQt5.QtWidgets import QWidget


class AutomatedOrganizerView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automated Window")
        self.setGeometry(100, 100, 400, 200)