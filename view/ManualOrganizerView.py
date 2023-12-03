from PyQt5.QtWidgets import QWidget


class ManualOrganizerView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manual Window")
        self.setGeometry(100, 100, 400, 200)