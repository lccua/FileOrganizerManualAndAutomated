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

class FileOrganizerModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileOrganizerModel, cls).__new__(cls)

            # Initialize class variables here
            cls._instance.is_automated = None
            cls._instance.is_toggled = False
            cls._instance.is_browse_window = None

            cls._instance.included_tree = None
            cls._instance.excluded_tree = None

            cls._instance.selected_days = []

            cls._instance.checked_items = {}

            cls._instance.final_checked_items = {}

            cls._instance.categorized_files = {}
            cls._instance.tester = {}
            cls._instance.excluded_files = {}

            cls._instance.exclusion_status = {}

            cls._instance.checkboxes = {}

            cls._instance.selected_folder_paths_manual = []
            cls._instance.selected_folder_paths_automated = []

            cls._instance.day_checkboxes_dict = {}

            cls._instance.checkbox_states = {}

            cls._instance.config = {}
            cls._instance.load_config()

        return cls._instance

    def __init__(self):
        # Ensure initialization happens only once
        if not hasattr(self, '_initialized'):
            # Call any setup methods or any additional initialization here if needed
            self._initialized = True


    """---- SHARED METHODS ----"""

    def select_and_display_folder_contents(self, listWidget, treeWidget, excluded_tree=None):
        # Create options for the file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Add the ReadOnly option

        # Open the folder dialog and get the selected folder path
        folder_path = QFileDialog.getExistingDirectory(None, "Select a folder", options=options)

        if self.is_automated:
            self.selected_folders = self.selected_folder_paths_automated
        else:
            self.selected_folders = self.selected_folder_paths_manual

        if folder_path:
            if folder_path in self.selected_folders:
                # Display a warning message if the folder path is already selected
                QMessageBox.warning(None, "Folder Already Selected", "This folder has already been selected.")
            else:
                # Check if there are any files (not directories) in the selected folder.
                files_with_extensions = any(
                    os.path.isfile(os.path.join(folder_path, filename)) for filename in os.listdir(folder_path))
                if not files_with_extensions:
                    # Display a warning message if there are no files with extensions
                    QMessageBox.warning(None, "No Files with Extensions", "There are no files in this folder.")
                else:
                    # Add the folder path to the list
                    if self.is_automated:
                        self.selected_folder_paths_automated.append(folder_path)

                        # Update and add the selected folder to the list widget
                        self.refresh_list_widget(listWidget)


                        self.update_tree_views(treeWidget, excluded_tree)

                    else:
                        self.selected_folder_paths_manual.append(folder_path)

                        # Update and add the selected folder to the list widget
                        self.refresh_list_widget(listWidget)

                        # Categorize the files
                        self.group_files_by_category(treeWidget, self.selected_folder_paths_manual)

    def toggle_select_all_items(self, list_widget):
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setSelected(True)
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def organize_chosen_files(self,treeWidget, remove_duplicates_checkbox, excluded_tree=None):

        if self.is_automated == False:
            unchecked_items = self.get_unchecked_items(treeWidget)
            self.remove_unchecked_items_from_categorized_files(self.categorized_files,unchecked_items)

        def calculate_file_hash(file_path, hash_function=hashlib.md5, buffer_size=65536):
            hash_obj = hash_function()
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(buffer_size)
                    if not data:
                        break
                    hash_obj.update(data)
            return hash_obj.hexdigest()

        def find_and_delete_duplicate_files(directory):
            # Create a dictionary to store file hashes and their paths
            file_hashes = {}

            for root, dirs, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_hash = calculate_file_hash(file_path)

                    if file_hash in file_hashes:
                        # We found a duplicate file
                        print(f'Duplicate file found: {file_path} and {file_hashes[file_hash]}')
                        # Delete the duplicate file
                        os.remove(file_path)
                        print(f'Deleted duplicate file: {file_path}')
                    else:
                        # Add the file hash to the dictionary
                        file_hashes[file_hash] = file_path

        for folder_path, folders in self.categorized_files.items():
            print(folder_path)
            for category, categories in folders.items():
                print(category)
                for file_type, file_types in categories.items():
                    print(file_type)
                    for file in file_types:
                        print(file)

                        new_folder_path = os.path.join(folder_path, category, file_type[1:])
                        os.makedirs(new_folder_path, exist_ok=True)

                        source_file = os.path.join(folder_path, file)
                        destination_file = os.path.join(new_folder_path, file)

                        # if the file doesnt exist in the directiory
                        if remove_duplicates_checkbox.isChecked():
                            print("Checking for duplicates and removing them...")
                            find_and_delete_duplicate_files(new_folder_path)

                        try:
                            shutil.move(source_file, destination_file)
                            print(f"Moved '{file}' to '{destination_file}'")
                        except Exception as e:
                            print(f"Error moving '{file}' to '{destination_file}': {e}")

        # After organizing files, refresh the QTreeWidget and re-categorize the files
        treeWidget.clear()  # Clear the existing items in the QTreeWidget
        categorized_files = {}  # Clear the categorized_files dictionary

        self.update_tree_views(treeWidget, excluded_tree)

    def fill_tree_with_data(self, treeWidget, file_categories=None, item=None):
        # Loop through keys and values in the categorized_files_dictionary

        if file_categories == None:
            file_categories = self.config

        for category_or_extension_name, values in file_categories.items():
            # If there's no parent item (top-level item):
            if item is None:
                # Create a new top-level item in the tree_view
                tree_view_item = QtWidgets.QTreeWidgetItem(treeWidget)
                # Set the text of the item to the current key
                tree_view_item.setText(0, category_or_extension_name)
            else:
                # Create a new child item under the parent item
                tree_view_item = QtWidgets.QTreeWidgetItem(item)
                # Set the text of the item to the current key
                tree_view_item.setText(0, category_or_extension_name)

            if not self.is_automated:
                # Only add checkboxes if is_automated is False
                tree_view_item.setFlags(tree_view_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                tree_view_item.setCheckState(0, Qt.Unchecked)

            if isinstance(values, dict):
                # When it encounters a dictionary as a value, there are nested items or subcategories to be added.
                self.fill_tree_with_data(treeWidget, values, tree_view_item)

            elif isinstance(values, list):
                if self.is_browse_window or not self.is_automated:

                    # Loop through each filename in the list
                    for filename in values:
                        # Create a new child item under the current item
                        child = QtWidgets.QTreeWidgetItem(tree_view_item)
                        # Set the text of the child item to the filename
                        child.setText(0, filename)

                        if not self.is_automated:
                            # Add special attributes for user interaction to the child item
                            child.setFlags(child.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsTristate)
                            # Set the initial check state of the child item to unchecked
                            child.setCheckState(0, Qt.Unchecked)

        # After populating the tree with categorized_files, sort the items alphabetically
        treeWidget.sortItems(0, Qt.AscendingOrder)

    def group_files_by_category(self,treeWidget, selected_folder_paths):
        # Loop through each selected folder path
        for source_folder in selected_folder_paths:
            # Loop through files in the source folder
            for filename in os.listdir(source_folder):
                file_extension = os.path.splitext(filename)[1]
                if file_extension:
                    # Look for the file extension in the dictionary file_categories
                    for category, extensions in self.config.items():
                        if file_extension in extensions:
                            if source_folder not in self.categorized_files:
                                # Create an entry for the source folder in the categorized files dictionary
                                # with an empty dictionary as its value
                                self.categorized_files[source_folder] = {}
                            if category not in self.categorized_files[source_folder]:
                                # Create an entry for the category within the source folder in the categorized files dictionary
                                # with an empty dictionary as its value
                                self.categorized_files[source_folder][category] = {}
                            if file_extension not in self.categorized_files[source_folder][category]:
                                # Create an empty list with the file extension as the key
                                self.categorized_files[source_folder][category][file_extension] = []
                            # Add the file to the file extension list
                            self.categorized_files[source_folder][category][file_extension].append(filename)

        if self.is_browse_window == False:
            treeWidget.clear()

            # Populate the tree widget with the categorized files and folders stored in the categorized_files dictionary
            self.fill_tree_with_data(treeWidget, self.categorized_files)

    def update_tree_views(self, included_tree, excluded_tree=None):
        """
        Updates the tree views with categorized and excluded files.

        Parameters:
        included_tree (QTreeWidget): Tree widget for included files.
        excluded_tree (QTreeWidget): Optional tree widget for excluded files.
        """
        self.clear_and_fill_excluded_tree(excluded_tree)
        self.group_files_by_category_helper(included_tree)
        self.remove_excluded_from_categorized()
        self.fill_included_tree(included_tree)

    def clear_and_fill_excluded_tree(self, excluded_tree):
        if excluded_tree:
            excluded_tree.clear()
            if self.excluded_files:
                self.fill_tree_with_data(excluded_tree, self.excluded_files)

    def group_files_by_category_helper(self, included_tree):
        folder_paths = self.selected_folder_paths_automated if self.is_automated else self.selected_folder_paths_manual
        self.group_files_by_category(included_tree, folder_paths)

    def remove_excluded_from_categorized(self):
        if self.categorized_files:
            self.delete_items_from_dict(self.categorized_files, self.excluded_files)

    def delete_items_from_dict(self, target_dict, items_to_delete):

        for key, value in items_to_delete.items():

            if isinstance(value, dict):
                # Recursively call the function to process nested dictionaries
                if key in target_dict:
                    self.delete_items_from_dict(target_dict[key], value)
                else:
                    print("lol")
                    continue
                # Check if the category is empty after processing
                if not target_dict[key]:
                    del target_dict[key]
            elif key in target_dict:
                # If the key exists in the target_dict, delete it
                del target_dict[key]

    def fill_included_tree(self, included_tree):
        if not self.is_browse_window:
            included_tree.clear()
            self.fill_tree_with_data(included_tree, self.categorized_files)

    def delete_selected_folder_and_contents(self, listWidget, treeWidget, excluded_tree=None):
        """
        Deletes the selected folder and updates the UI accordingly.

        Parameters:
        listWidget (QListWidget): The widget listing the folders.
        treeWidget (QTreeWidget): The tree widget displaying folder structure.
        excluded_tree (QTreeWidget): Optional tree widget for excluded items.
        """
        selected_item = self.get_selected_folder(listWidget)
        if not selected_item:
            return

        if self.remove_folder_from_paths(selected_item):
            print("Deleted folder:", selected_item)
            self.update_folder_list_ui(listWidget)
            self.remove_folder_from_categorized_files(selected_item)
            self.update_tree_views(treeWidget, excluded_tree)

    def get_selected_folder(self, listWidget):
        """
        Gets the text of the currently selected item in the list widget.

        Parameters:
        listWidget (QListWidget): The widget listing the folders.

        Returns:
        str: The text of the selected item or None if no item is selected.
        """
        selected_items = listWidget.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

    def remove_folder_from_paths(self, selected_item):
        """
        Removes the selected folder path from the appropriate list based on mode.

        Parameters:
        selected_item (str): The folder path to be removed.

        Returns:
        bool: True if the folder was successfully removed, False otherwise.
        """
        selected_folder_paths = self.selected_folder_paths_automated if self.is_automated else self.selected_folder_paths_manual
        if selected_item in selected_folder_paths:
            selected_folder_paths.remove(selected_item)
            return True
        return False

    def update_folder_list_ui(self, listWidget):
        """
        Updates the folder list in the UI.

        Parameters:
        listWidget (QListWidget): The widget listing the folders.
        """
        listWidget.clear()
        selected_folder_paths = self.selected_folder_paths_automated if self.is_automated else self.selected_folder_paths_manual
        listWidget.addItems(selected_folder_paths)

    def remove_folder_from_categorized_files(self, selected_item):
        """
        Removes the selected folder from the categorized files dictionary.

        Parameters:
        selected_item (str): The folder path to be removed.
        """
        if selected_item in self.categorized_files:
            del self.categorized_files[selected_item]

    def refresh_list_widget(self,listWidget):
        # Clear the existing items in the list widget
        listWidget.clear()
        # Add the selected folder paths to the list widget

        if self.is_automated == True:
            selected_folder_paths = self.selected_folder_paths_automated
        else:
            selected_folder_paths = self.selected_folder_paths_manual

        listWidget.addItems(selected_folder_paths)

    def get_item_depth(self,tree_item):
        depth = 0
        parent = tree_item.parent()
        while parent is not None:
            depth += 1
            parent = parent.parent()
        return depth



    """---- AUTOMATED METHODS ----"""

    def check_saved_items(self,treeWidget):

        # Iterate through the treeWidget items and check those not in checked_items
        for tree_item in treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            tree_item.setCheckState(0, QtCore.Qt.Unchecked)

        # Iterate through checked_items and set check state to Checked
        for folder_path, folders in self.tester.items():
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

    def check_current_day(self,selected_days, duplicates_checkbox, tree_widget, excluded_tree):
        # Get the current day (e.g., "Mon", "Tue")
        current_day = QtCore.QDate.currentDate().toString("ddd")
        print(current_day)

        # Check if the current day is in the selected days
        if current_day in selected_days:
            print("yes today needs to be organized")

            if len(self.categorized_files) != 0:
                self.organize_chosen_files(tree_widget, duplicates_checkbox, excluded_tree)


        else:
            print("nothing needs to be organized today")

    def include_files(self, included_tree, excluded_tree):

        selected_item = excluded_tree.selectedItems()[0]
        depth = self.get_item_depth(selected_item)

        if len(self.excluded_files) == 0:
            current_level = self.excluded_files
        else:
            current_level = self.excluded_files

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

        print(self.excluded_files)
        excluded_tree.clear()
        self.update_tree_views(included_tree, excluded_tree)

    def exclude_files(self, included_tree, excluded_tree):
        excluded_tree.clear()

        selected_item = included_tree.selectedItems()[0]

        depth = self.get_item_depth(selected_item)

        current_level = self.excluded_files

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

        print(self.excluded_files)
        self.update_tree_views(included_tree, excluded_tree)

    def get_excluded_tree(self, tree):
        self.excluded_tree = tree

    def get_included_tree(self, tree):
        self.included_tree = tree



    """---- MANUAL METHODS ----"""

    def get_unchecked_items(self, treeWidget):
        unchecked_items = []

        # Iterating over each top-level item in the tree
        for i in range(treeWidget.topLevelItemCount()):
            top_item = treeWidget.topLevelItem(i)

            # Iterating over second-level child items
            for j in range(top_item.childCount()):
                second_level_item = top_item.child(j)

                # Iterating over third-level child items
                for k in range(second_level_item.childCount()):
                    third_level_item = second_level_item.child(k)

                    # Iterating over fourth-level child items
                    for l in range(third_level_item.childCount()):
                        fourth_level_item = third_level_item.child(l)

                        # Check if the fourth-level item is unchecked
                        if fourth_level_item.checkState(0) != QtCore.Qt.Checked:
                            unchecked_items.append(
                                fourth_level_item.text(0))  # Assuming the item's text is the identifier

        return unchecked_items

    def remove_unchecked_items_from_categorized_files(self,categorized_files, unchecked_items):
        for category, subcategories in list(categorized_files.items()):
            for subcategory, filetypes in list(subcategories.items()):
                for filetype, files in list(filetypes.items()):
                    # Filter out unchecked items from the fourth level
                    categorized_files[category][subcategory][filetype] = [
                        file for file in files if file not in unchecked_items
                    ]

                    # Remove empty file types
                    if not categorized_files[category][subcategory][filetype]:
                        del categorized_files[category][subcategory][filetype]

                # Remove empty subcategories
                if not categorized_files[category][subcategory]:
                    del categorized_files[category][subcategory]

            # Remove empty categories
            if not categorized_files[category]:
                del categorized_files[category]

        return categorized_files



    """---- BROWSE METHODS ----"""

    def add_files_types_to_excluded_files(self, folder_list, items_tree):
        selected_folders = folder_list.selectedItems()

        selected_item = items_tree.selectedItems()[0]

        depth = self.get_item_depth(selected_item)

        for folder in selected_folders:
            selected_folder_name = folder.text()

            # Initialize a reference to the current level of the nested dictionary

            current_level = self.excluded_files




            if depth == 0:
                folder_path = selected_folder_name
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


            elif depth == 1:
                folder_path = selected_folder_name
                category = selected_item.parent().text(0)
                file_type = selected_item.text(0)

                if folder_path not in current_level:
                    current_level[folder_path] = {}
                if category not in current_level[folder_path]:
                    current_level[folder_path][category] = {}
                if file_type not in current_level[folder_path][category]:
                    current_level[folder_path][category][file_type] = []


        self.update_tree_views(self.included_tree, self.excluded_tree)

        print(self.excluded_files)



    """---- JSON ----"""

    def load_config(self):
        with open('file_categories.json', 'r') as file:
            self.config = json.load(file)

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
        if self.excluded_files:
            with open("excluded_files.json", 'w') as file:
                json.dump(self.excluded_files, file)

    def load_excluded_files(self, included_tree, excluded_tree):
        try:
            with open("excluded_files.json", 'r') as file:
                # Check if the file is not empty before loading
                if os.path.getsize("excluded_files.json") > 0:
                    self.excluded_files = json.load(file)
                    self.update_tree_views(included_tree, excluded_tree)
                else:
                    print("excluded_files.json is empty.")
        except FileNotFoundError:
            print("excluded_files.json not found.")

    def save_selected_folders(self):
        if self.is_automated:
            self.folders = self.selected_folder_paths_automated
            json_string = "selected_folders_automated.json"

        # Check if the list is not empty before saving
        if self.folders:
            with open(json_string, "w") as json_file:
                json.dump(self.folders, json_file)

    def load_selected_folders(self, listWidget, treeWidget):
        if self.is_automated:
            json_string = "selected_folders_automated.json"

        if os.path.exists(json_string):
            # Check if the file is not empty before loading
            if os.path.getsize(json_string) > 0:
                with open(json_string, "r") as json_file:
                    folders = json.load(json_file)
                    if self.is_automated:
                        self.selected_folder_paths_automated = folders


                    self.refresh_list_widget(listWidget)  # Update the list widget with the loaded folder paths
                    self.group_files_by_category(treeWidget, folders)
            else:
                print(f"{json_string} is empty.")

    def save_checked_items(self):
        if self.is_automated:
            # Check if the dictionary is not empty before saving
            if self.tester:
                with open("checked_items.json", "w") as json_file:
                    json.dump(self.tester, json_file)

    def load_checked_items(self, treeWidget):
        if self.is_automated:
            # Check if the JSON file with checked item state exists
            if os.path.exists("checked_items.json"):
                # Check if the file is not empty before loading
                if os.path.getsize("checked_items.json") > 0:
                    with open("checked_items.json", "r") as json_file:
                        self.tester = json.load(json_file)
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
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_toggle_state(self,is_toggled):
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
                    self.is_toggled = config_data.get("is_toggled")
                    return self.is_toggled
            else:
                print("toggle_state.json is empty.")
        else:
            self.is_toggled = False
            return self.is_toggled