# to run -> python -m unittest test_file_organizer_model.py
import unittest
from model.FileOrganizerModel import FileOrganizerModel
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class TestFileOrganizerModel(unittest.TestCase):

    def setUp(self):
        self.model = FileOrganizerModel()
        # Setup for any other dependencies like mock file system, etc.

    def test_toggle_select_all_items(self):
        # Assuming toggle_select_all_items method toggles the selection state of all items
        list_widget = QListWidget()
        for i in range(5):  # Add 5 items
            list_widget.addItem(QListWidgetItem(f"Item {i}"))

        # Test Select All
        self.model.toggle_select_all_items(list_widget)
        for i in range(list_widget.count()):
            self.assertTrue(list_widget.item(i).isSelected(), "Item should be selected")

        # Test Deselect All
        self.model.toggle_select_all_items(list_widget)
        for i in range(list_widget.count()):
            self.assertFalse(list_widget.item(i).isSelected(), "Item should be deselected")
