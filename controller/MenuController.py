# MenuController.py

from view.ManualOrganizerView import ManualOrganizerView
from view.AutomatedOrganizerView import AutomatedOrganizerView
from model.FileOrganizerModel import FileOrganizerModel


class MenuController:
    def __init__(self):

        self.model = FileOrganizerModel()


    def open_automated_window(self):
        automated_view = AutomatedOrganizerView()
        automated_view.show()

    def open_manual_window(self):
        manual_view = ManualOrganizerView()
        manual_view.show()



