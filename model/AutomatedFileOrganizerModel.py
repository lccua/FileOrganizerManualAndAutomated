# model.py
import hashlib
import pickle
import shutil

# third party imports
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox


# system imports
import os
import json

# local imports
from model.SharedFileOrganizerModel import SharedFileOrganizerModel
from model.ManualFileOrganizerModel import ManualFileOrganizerModel
from model.FileOrganizerStateManager import FileOrganizerStateManager


class AutomatedFileOrganizerModel:
    def __init__(self):
        self.shared_model = SharedFileOrganizerModel()
        self.manual_model = ManualFileOrganizerModel()
        self.state = FileOrganizerStateManager()



    """---- AUTOMATED METHODS ----"""

    def check_saved_items(self, treeWidget):

        # Iterate through the treeWidget items and check those not in checked_items
        for tree_item in treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            tree_item.setCheckState(0, QtCore.Qt.Unchecked)

        # Iterate through checked_items and set check state to Checked
        for folder_path, folders in self.state.checked_items.items():
            for category, categories in folders.items():

                for file_type, file_types in categories.items():

                    file_type_items = treeWidget.findItems(file_type,
                                                           QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)

                    # Check the lower-level tree view items (depth 2)
                    for item in file_type_items:
                        itemlol = item.text(0)
                        file_type_item = item
                        category_item = file_type_item.parent()
                        folder_item = category_item.parent()

                        # Get the name of the top-level item from the first column
                        top_level_name = folder_item.text(0)

                        if top_level_name == folder_path:
                            item.setCheckState(0, QtCore.Qt.Checked)  # Set the check state to Checked

                            # Check the children of the item
                            for child_index in range(item.childCount()):
                                if child_index == 0:
                                    break
                                else:
                                    child_item = item.child(child_index)
                                    child_item.setCheckState(0, QtCore.Qt.Checked)

                    for file in file_types:
                        # Find the item in the tree widget
                        file_items = treeWidget.findItems(file, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)

                        # Check the lower-level tree view items (depth 3)
                        for item in file_items:
                            itemlol = item.text(0)
                            file_type_item = item.parent()
                            category_item = file_type_item.parent()
                            folder_item = category_item.parent()

                            # Get the name of the top-level item from the first column
                            top_level_name = folder_item.text(0)

                            if top_level_name == folder_path:
                                item.setCheckState(0, QtCore.Qt.Checked)  # Set the check state to Checked

    def check_current_day(self, file_overview_tree, remove_duplicates_checkbox, excluded_items_tree):
        # Get the current day (e.g., "Mon", "Tue")
        current_day = QtCore.QDate.currentDate().toString("ddd")
        print(current_day)

        # Check if the current day is in the selected days
        if self.state.day_checkboxes_dict.get(current_day, False):
            print("starting automation")

            if len(self.state.categorized_files) != 0:
                self.shared_model.organize_chosen_files(file_overview_tree, remove_duplicates_checkbox, excluded_items_tree)


        else:
            print("nothing needs to be organized today")

    def include_files(self, included_tree, excluded_tree):

        selected_item = excluded_tree.selectedItems()[0]
        depth = self.shared_model.get_item_depth(selected_item)

        if len(self.state.excluded_files) == 0:
            current_level = self.state.excluded_files
        else:
            current_level = self.state.excluded_files

        if depth == 0:
            folder_path = selected_item.text(0)

            if folder_path in current_level:
                current_level.pop(folder_path)

        elif depth == 1:
            folder_path = selected_item.parent().text(0)
            category = selected_item.text(0)

            if folder_path in current_level and category in current_level[folder_path]:
                current_level[folder_path].pop(category)

                # Check if the folder is empty, and if so, remove it
                if not current_level[folder_path]:
                    current_level.pop(folder_path)

        elif depth == 2:
            folder_path = selected_item.parent().parent().text(0)
            category = selected_item.parent().text(0)
            file_type = selected_item.text(0)

            if folder_path in current_level and category in current_level[folder_path] and file_type in \
                    current_level[folder_path][category]:
                current_level[folder_path][category].pop(file_type)

                # Check if the category is empty, and if so, remove it
                if not current_level[folder_path][category]:
                    current_level[folder_path].pop(category)

                # Check if the folder is empty, and if so, remove it
                if not current_level[folder_path]:
                    current_level.pop(folder_path)

        print(self.state.excluded_files)
        excluded_tree.clear()
        self.shared_model.update_tree_views(included_tree, excluded_tree)

    def exclude_files(self, included_tree, excluded_tree):
        excluded_tree.clear()

        selected_item = included_tree.selectedItems()[0]

        depth = self.shared_model.get_item_depth(selected_item)

        current_level = self.state.excluded_files

        if depth == 0:
            folder_path = selected_item.text(0)

            if folder_path not in current_level:
                current_level[folder_path] = {}

            for i in range(selected_item.childCount()):
                child_item = selected_item.child(i)
                category = child_item.text(0)

                if category not in current_level[folder_path]:
                    current_level[folder_path][category] = {}

                for j in range(child_item.childCount()):  # Use a different variable here
                    grand_child_item = child_item.child(j)
                    file_type = grand_child_item.text(0)

                    if file_type not in current_level[folder_path][category]:
                        current_level[folder_path][category][file_type] = []


        elif depth == 1:
            folder_path = selected_item.parent().text(0)
            category = selected_item.text(0)

            if folder_path not in current_level:
                current_level[folder_path] = {}

            if category not in current_level[folder_path]:
                current_level[folder_path][category] = {}

            for i in range(selected_item.childCount()):
                child_item = selected_item.child(i)
                file_type = child_item.text(0)

                if file_type not in current_level[folder_path][category]:
                    current_level[folder_path][category][file_type] = []


        elif depth == 2:
            folder_path = selected_item.parent().parent().text(0)
            category = selected_item.parent().text(0)
            file_type = selected_item.text(0)

            if folder_path not in current_level:
                current_level[folder_path] = {}
            if category not in current_level[folder_path]:
                current_level[folder_path][category] = {}
            if file_type not in current_level[folder_path][category]:
                current_level[folder_path][category][file_type] = []

        print(self.state.excluded_files)
        self.shared_model.update_tree_views(included_tree, excluded_tree)

    def get_excluded_tree(self, tree):
        self.state.excluded_tree = tree

    def get_included_tree(self, tree):
        self.state.included_tree = tree

    """---- JSON ----"""

    def save_remove_duplicates_state(self, state):
        with open('remove_duplicates_state.pickle', 'wb') as file:
            pickle.dump(state, file)

    def load_remove_duplicates_state(self):
        try:
            with open('remove_duplicates_state.pickle', 'rb') as file:
                state = pickle.load(file)
                return state
        except FileNotFoundError:
            return False  # Default to False if the file doesn't exist or hasn't been saved yet

    def save_excluded_files(self):
        # Check if the dictionary is not empty before saving
        if self.state.excluded_files:
            with open("excluded_files.json", 'w') as file:
                json.dump(self.state.excluded_files, file)

    def load_excluded_files(self, included_tree, excluded_tree):
        try:
            with open("excluded_files.json", 'r') as file:
                # Check if the file is not empty before loading
                if os.path.getsize("excluded_files.json") > 0:
                    self.state.excluded_files = json.load(file)
                    self.shared_model.update_tree_views(included_tree, excluded_tree)
                else:
                    print("excluded_files.json is empty.")
        except FileNotFoundError:
            print("excluded_files.json not found.")

    def save_selected_folders(self):
        self.folders = self.state.selected_folder_paths_automated
        json_string = "selected_folders_automated.json"

        # Check if the list is not empty before saving
        if self.folders:
            with open(json_string, "w") as json_file:
                json.dump(self.folders, json_file)

    def load_selected_folders(self, listWidget):
        json_string = "selected_folders_automated.json"

        if os.path.exists(json_string):
            # Check if the file is not empty before loading
            if os.path.getsize(json_string) > 0:
                with open(json_string, "r") as json_file:
                    folders = json.load(json_file)

                    # Filter out non-existing folder paths
                    existing_folders = [folder for folder in folders if os.path.exists(folder)]

                    self.state.selected_folder_paths_automated = existing_folders

                    # Update the JSON file with the filtered list
                    with open(json_string, "w") as json_file:
                        json.dump(existing_folders, json_file)

                    self.shared_model.refresh_list_widget(listWidget)  # Update the list widget with the loaded folder paths
            else:
                print(f"{json_string} is empty.")

    def save_checked_items(self):
        # Check if the dictionary is not empty before saving
        if self.state.checked_items:
            with open("checked_items.json", "w") as json_file:
                json.dump(self.state.checked_items, json_file)

    def load_checked_items(self, treeWidget):
            # Check if the JSON file with checked item state exists
            if os.path.exists("checked_items.json"):
                # Check if the file is not empty before loading
                if os.path.getsize("checked_items.json") > 0:
                    with open("checked_items.json", "r") as json_file:
                        self.state.checked_items = json.load(json_file)
                        self.check_saved_items(treeWidget)
                else:
                    print("checked_items.json is empty.")

    def save_selected_days(self, day_checkboxes_dict):
        if day_checkboxes_dict:
            day_states = {day: checkbox.isChecked() for day, checkbox in day_checkboxes_dict.items()}
            with open('checkbox_states.json', 'w') as f:
                json.dump(day_states, f)

    def load_selected_days(self):
        try:
            with open('checkbox_states.json', 'r') as f:
                self.state.day_checkboxes_dict = json.load(f)
                return self.state.day_checkboxes_dict
        except FileNotFoundError:
            return {}

    def save_toggle_state(self, is_toggled):
        config_data = {"is_toggled": is_toggled}
        with open("toggle_state.json", "w") as file:
            json.dump(config_data, file)

    def load_toggle_state(self):
        # Check if the configuration file exists
        if os.path.isfile("toggle_state.json"):
            # Check if the file is not empty before loading
            if os.path.getsize("toggle_state.json") > 0:
                with open("toggle_state.json", "r") as file:
                    config_data = json.load(file)
                    self.state.is_toggled = config_data.get("is_toggled")
                    return self.state.is_toggled
            else:
                print("toggle_state.json is empty.")
        else:
            self.state.is_toggled = False
            return self.state.is_toggled