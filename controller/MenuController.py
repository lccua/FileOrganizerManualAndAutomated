# MenuController.py
from view.MenuView import MenuView
from view.ManualOrganizerView import ManualOrganizerView
from view.AutomatedOrganizerView import AutomatedOrganizerView
from model.FileOrganizerModel import FileOrganizerModel
from controller.AutomatedOrganizerController import AutomatedFileOrganizerController
from controller.ManualOrganizerController import ManualFileOrganizerController

class MenuController:
    def __init__(self):
        self.menu_view = MenuView()
        self.menu_view.show()
        self.model = FileOrganizerModel()


        self.connect_signals()

    def connect_signals(self):
        self.menu_view.automated_window_button.clicked.connect(self.open_automated_window)
        self.menu_view.manual_window_button.clicked.connect(self.open_manual_window)


    def open_automated_window(self):
        AutomatedFileOrganizerController()

    def open_manual_window(self):
        ManualFileOrganizerController()

