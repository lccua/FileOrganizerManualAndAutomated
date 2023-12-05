# MenuView.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout

from controller.MenuController import MenuController


class MenuView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.controller = MenuController


        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 200)

        self.greeting_label = QLabel("Welcome to the File Organizer App!")
        self.automated_window_button = QPushButton("Open Automated Organizer Window")
        self.manual_window_button = QPushButton("Open Manual Organizer Window")

        self._create_layout()

        self.connect_signals()

    def connect_signals(self):
        self.automated_window_button.clicked.connect(self.controller.open_automated_window)
        self.manual_window_button.clicked.connect(self.controller.open_manual_window)

    def _create_layout(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.greeting_label)
        layout.addWidget(self.automated_window_button)
        layout.addWidget(self.manual_window_button)

        self.setCentralWidget(central_widget)

