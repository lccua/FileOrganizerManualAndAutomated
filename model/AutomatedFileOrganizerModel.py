# model.py


# third party imports
from PyQt5 import QtCore


# system imports
import os
import json
import pickle


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

    def include_files(self, included_tree, excluded_tree):
        """
        Includes files based on the selected items in the included tree.

        :param included_tree: tree widget containing included items
        :param excluded_tree: tree widget containing excluded items
        """

        # Check if any item is selected
        if not excluded_tree.selectedItems():
            # Display warning and exit the function
            self.shared_model.show_warning("No Item Selected", "There is no item selected.")
            return

        selected_item = excluded_tree.selectedItems()[0]
        depth = self.shared_model.get_item_depth(selected_item)

        if depth == 0:
            folder_path = selected_item.text(0)
            self._include_folder(folder_path)

        elif depth == 1:
            folder_path = selected_item.parent().text(0)
            category = selected_item.text(0)
            self._include_category(folder_path, category)

        elif depth == 2:
            folder_path = selected_item.parent().parent().text(0)
            category = selected_item.parent().text(0)
            file_type = selected_item.text(0)
            self._include_file_type(folder_path, category, file_type)

        print(self.state.excluded_files)
        excluded_tree.clear()
        self.shared_model.update_tree_views_helper(included_tree, excluded_tree)

    def _include_folder(self, folder_path):
        """
        Excludes a folder path.

        :param folder_path: The path of the folder to exclude.
        """
        current_level = self.state.excluded_files

        if folder_path in current_level:
            current_level.pop(folder_path)

    def _include_category(self, folder_path, category):
        """
        Excludes a category.

        :param folder_path: The path of the folder containing the category.
        :param category: The category to exclude.
        """
        current_level = self.state.excluded_files

        if folder_path in current_level and category in current_level[folder_path]:
            current_level[folder_path].pop(category)

            # Check if the folder is empty, and if so, remove it
            if not current_level[folder_path]:
                current_level.pop(folder_path)

    def _include_file_type(self, folder_path, category, file_type):
        """
        Excludes a file type.

        :param folder_path: The path of the folder containing the category.
        :param category: The category containing the file type.
        :param file_type: The file type to exclude.
        """
        current_level = self.state.excluded_files

        if folder_path in current_level and category in current_level[folder_path] and file_type in \
                current_level[folder_path][category]:
            current_level[folder_path][category].pop(file_type)

            # Check if the category is empty, and if so, remove it
            if not current_level[folder_path][category]:
                current_level[folder_path].pop(category)

            # Check if the folder is empty, and if so, remove it
            if not current_level[folder_path]:
                current_level.pop(folder_path)




    def exclude_files(self, included_tree, excluded_tree):
        """
        Excludes files based on the selected items in the included tree.

        :param included_tree: tree widget containing included items
        :param excluded_tree: tree widget containing excluded items
        """

        # Check if any item is selected
        if not included_tree.selectedItems():
            # Display warning and exit the function
            self.shared_model.show_warning("No Item Selected", "There is no item selected.")
            return

        excluded_tree.clear()

        selected_item = included_tree.selectedItems()[0]


        depth = self.shared_model.get_item_depth(selected_item)

        if depth == 0:
            folder_path = selected_item.text(0)
            self._exclude_folder(folder_path, selected_item)

        elif depth == 1:
            folder_path = selected_item.parent().text(0)
            category = selected_item.text(0)
            self._exclude_category(folder_path, category, selected_item)

        elif depth == 2:
            folder_path = selected_item.parent().parent().text(0)
            category = selected_item.parent().text(0)
            file_type = selected_item.text(0)
            self._exclude_file_type(folder_path, category, file_type)

        print(self.state.excluded_files)
        self.shared_model.update_tree_views_helper(included_tree, excluded_tree)

    def _exclude_folder(self, folder_path, selected_item):
        """
        Excludes a folder path.

        :param folder_path: The path of the folder to exclude.
        """
        current_level = self.state.excluded_files

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

    def _exclude_category(self, folder_path, category, selected_item):
        """
        Excludes a category.

        :param folder_path: The path of the folder containing the category.
        :param category: The category to exclude.
        """
        current_level = self.state.excluded_files

        if folder_path not in current_level:
            current_level[folder_path] = {}

        if category not in current_level[folder_path]:
            current_level[folder_path][category] = {}

        for i in range(selected_item.childCount()):
            child_item = selected_item.child(i)
            file_type = child_item.text(0)

            if file_type not in current_level[folder_path][category]:
                current_level[folder_path][category][file_type] = []

    def _exclude_file_type(self, folder_path, category, file_type):
        """
        Excludes a file type.

        :param folder_path: The path of the folder containing the category.
        :param category: The category containing the file type.
        :param file_type: The file type to exclude.
        """
        current_level = self.state.excluded_files

        if folder_path not in current_level:
            current_level[folder_path] = {}
        if category not in current_level[folder_path]:
            current_level[folder_path][category] = {}
        if file_type not in current_level[folder_path][category]:
            current_level[folder_path][category][file_type] = []






    def check_saved_items(self, treeWidget):
        """
        Updates the check state of items in a tree widget based on previously saved states.

        It first unchecks all items and then checks those according to the saved state.

        :param treeWidget: The tree widget to update.
        """
        # Uncheck all items
        for tree_item in treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            tree_item.setCheckState(0, QtCore.Qt.Unchecked)

        # Check items as per the saved state
        for folder_path, categories in self.state.checked_items.items():
            for category, file_types_dict in categories.items():
                for file_type in file_types_dict.keys():
                    # Find and check the specific items based on folder path, category, and file type
                    file_type_items = treeWidget.findItems(file_type,
                                                           QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)
                    for item in file_type_items:
                        if self._item_matches_folder_and_category(item, folder_path, category):
                            item.setCheckState(0, QtCore.Qt.Checked)

    def _item_matches_folder_and_category(self, item, folder_path, category):
        """
        Checks if the tree item matches the given folder path and category.

        :param item: The item to check.
        :param folder_path: The folder path to match against.
        :param category: The category to match against.
        :return: True if the item matches, False otherwise.
        """
        category_item = item.parent()
        folder_item = category_item.parent() if category_item else None
        return folder_item and folder_item.text(0) == folder_path and category_item.text(0) == category




    def check_current_day(self, file_overview_tree, remove_duplicates_checkbox, excluded_items_tree):
        """
        Checks if the current day matches any of the selected days for automation
        and performs file organization if it does.

        :param file_overview_tree: The tree widget showing an overview of files.
        :param remove_duplicates_checkbox: Checkbox indicating whether to remove duplicates.
        :param excluded_items_tree: Tree widget showing excluded items.
        """
        current_day = QtCore.QDate.currentDate().toString("ddd")
        print(current_day)

        # Automate file organization if the current day is selected for automation
        if self.state.day_checkboxes_dict.get(current_day, False):
            print("starting automation")
            if self.state.categorized_files:
                self.shared_model.organize_chosen_files(file_overview_tree, remove_duplicates_checkbox,
                                                        excluded_items_tree)
        else:
            print("nothing needs to be organized today")




    def get_excluded_tree(self, tree):
        self.excluded_tree = tree

    def get_included_tree(self, tree):
        self.included_tree = tree


    """---- JSON ----"""

    """ READ / WRITE """

    def _read_json_file(self, file_path):
        """ Read a JSON file and return its content. """
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            print(f"{file_path} is empty or does not exist.")
            return None

    def _write_json_file(self, data, file_path):
        """ Write data to a JSON file. """
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def _read_pickle_file(self, file_path):
        """ Read a pickle file and return its content. """
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return False

    def _write_pickle_file(self, data, file_path):
        """ Write data to a pickle file. """
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)




    """ SAVE / LOAD """

    def save_remove_duplicates_state(self, state):
        self._write_pickle_file(state, 'remove_duplicates_state.pickle')

    def load_remove_duplicates_state(self):
        return self._read_pickle_file('remove_duplicates_state.pickle')

    def save_excluded_files(self):
        if self.state.excluded_files:
            self._write_json_file(self.state.excluded_files, "excluded_files.json")

    def load_excluded_files(self, included_tree, excluded_tree):
        excluded_files = self._read_json_file("excluded_files.json")
        if excluded_files:
            self.state.excluded_files = excluded_files
            self.shared_model.update_tree_views_helper(included_tree, excluded_tree)

    def save_selected_folders(self):
        json_string = "selected_folders_automated.json"
        self._write_json_file(self.state.selected_folder_paths_automated, json_string)

    def load_selected_folders(self, listWidget):
        json_string = "selected_folders_automated.json"
        folders = self._read_json_file(json_string)
        if folders:
            existing_folders = [folder for folder in folders if os.path.exists(folder)]
            self.state.selected_folder_paths_automated = existing_folders
            self._write_json_file(existing_folders, json_string)
            self.shared_model.refresh_list_widget(listWidget)

    def save_checked_items(self):
        if self.state.checked_items:
            self._write_json_file(self.state.checked_items, "checked_items.json")

    def load_checked_items(self, treeWidget):
        checked_items = self._read_json_file("checked_items.json")
        if checked_items:
            self.state.checked_items = checked_items
            self.check_saved_items(treeWidget)

    def save_selected_days(self, day_checkboxes_dict):
        if day_checkboxes_dict:
            day_states = {day: checkbox.isChecked() for day, checkbox in day_checkboxes_dict.items()}
            self._write_json_file(day_states, 'checkbox_states.json')

    def load_selected_days(self):
        return self._read_json_file('checkbox_states.json') or {}

    def save_toggle_state(self, is_toggled):
        self._write_json_file({"is_toggled": is_toggled}, "toggle_state.json")

    def load_toggle_state(self):
        config_data = self._read_json_file("toggle_state.json")
        if config_data:
            self.state.is_toggled = config_data.get("is_toggled")
        else:
            self.state.is_toggled = False
        return self.state.is_toggled