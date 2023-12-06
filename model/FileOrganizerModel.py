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
from constants import FILE_CATEGORIES


class FileOrganizerModel:

    # VARIABLES
    is_automated = None
    is_toggled = False

    included_tree = None
    excluded_tree = None

    selected_days = []

    checked_items = {}

    final_checked_items = {}

    categorized_files = {}
    tester = {}
    excluded_files = {}

    exclusion_status = {}

    checkboxes = {}

    selected_folder_paths_manual = []

    selected_folder_paths_automated = []

    day_checkboxes_dict = {}

    # AUTOMATED
    def post_excluded_tree(self,tree):
        global excluded_tree
        excluded_tree = tree

    def post_included_tree(self,tree):
        global included_tree
        included_tree = tree

    def select_and_display_folder_contents(self, listWidget, treeWidget, excluded_tree):
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
                        self.refresh_list_widget(listWidget, self.selected_folder_paths_automated)


                        self.update_and_group_files_by_category_helper(treeWidget, excluded_tree)

                    else:
                        self.selected_folder_paths_manual.append(folder_path)

                        # Update and add the selected folder to the list widget
                        self.refresh_list_widget(listWidget, self.selected_folder_paths_manual)

                        # Categorize the files
                        self.group_files_by_category(treeWidget, self.selected_folder_paths_manual)

    def delete_selected_folder_and_contents(self,listWidget, treeWidget, excluded_tree):
        global selected_folder_paths_automated, selected_folder_paths_manual
        selected_items = listWidget.selectedItems()

        if self.is_automated:
            selected_folder_paths = self.selected_folder_paths_automated
        else:
            selected_folder_paths = self.selected_folder_paths_manual

        if selected_items:
            selected_item = selected_items[0].text()

            if selected_item in selected_folder_paths:
                selected_folder_paths.remove(selected_item)  # Remove the selected folder path
                print("Deleted folder:", selected_item)

                # Update the QListWidget with the modified folder paths
                listWidget.clear()  # Clear the existing items
                listWidget.addItems(selected_folder_paths)  # Add the modified folder paths

                # Delete the folder from the categorized_files dictionary
                for source_folder in list(self.categorized_files.keys()):
                    if source_folder == selected_item:
                        del self.categorized_files[source_folder]

        self.update_and_group_files_by_category_helper(treeWidget, excluded_tree)

    def include_files(self,included_tree, excluded_tree):
        global categorized_files, excluded_files

        selected_item = excluded_tree.selectedItems()[0]
        depth = self.get_item_depth(selected_item)

        # Initialize a reference to the current level of the nested dictionary
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
        self.update_and_group_files_by_category_helper(included_tree, excluded_tree)

    def exclude_files(self,included_tree, excluded_tree):
        global categorized_files, excluded_files
        excluded_tree.clear()

        selected_item = included_tree.selectedItems()[0]

        depth = self.get_item_depth(selected_item)

        # Initialize a reference to the current level of the nested dictionary
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
        self.update_and_group_files_by_category_helper(included_tree, excluded_tree)

    def refresh_list_widget(self,listWidget, selected_folder_paths):
        # Clear the existing items in the list widget
        listWidget.clear()
        # Add the selected folder paths to the list widget
        listWidget.addItems(selected_folder_paths)

    def update_and_group_files_by_category_helper(self,included_tree, excluded_tree):
        global excluded_files, categorized_files

        excluded_tree.clear()
        self.fill_tree_with_data(excluded_tree, self.excluded_files)

        self.group_files_by_category(included_tree, self.selected_folder_paths_automated)

        if len(self.categorized_files) != 0:
            self.delete_items_from_dict(self.categorized_files, self.excluded_files)

        included_tree.clear()
        self.fill_tree_with_data(included_tree, self.categorized_files)

        print(self.categorized_files)

    def fill_tree_with_data(self, treeWidget, categorized_files_dictionary, is_browse_window=None, item=None):
        # Loop through keys and values in the categorized_files_dictionary
        for category_or_extension_name, values in categorized_files_dictionary.items():
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
                self.fill_tree_with_data(treeWidget, values, None, tree_view_item)

            elif isinstance(values, list):
                if is_browse_window or not self.is_automated:

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

    def delete_items_from_dict(self,target_dict, items_to_delete):

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

    def group_files_by_category(self,treeWidget, selected_folder_paths):

        # Loop through each selected folder path
        for source_folder in selected_folder_paths:
            # Loop through files in the source folder
            for filename in os.listdir(source_folder):
                file_extension = os.path.splitext(filename)[1]
                if file_extension:
                    # Look for the file extension in the dictionary file_categories
                    for category, extensions in FILE_CATEGORIES.items():
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

        treeWidget.clear()

        # Populate the tree widget with the categorized files and folders stored in the categorized_files dictionary
        self.fill_tree_with_data(treeWidget, self.categorized_files)

    def get_item_depth(self,tree_item):
        depth = 0
        parent = tree_item.parent()
        while parent is not None:
            depth += 1
            parent = parent.parent()
        return depth

    def organize_chosen_files(self,treeWidget, remove_duplicates_checkbox, selected_folder_paths, excluded_tree):
        global categorized_files, checked_items

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

        for folder_path, folders in categorized_files.items():
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
        self.update_and_group_files_by_category_helper(treeWidget, excluded_tree)

    def check_current_day(self,selected_days, duplicates_checkbox, tree_widget, excluded_tree):
        # Get the current day (e.g., "Mon", "Tue")
        current_day = QtCore.QDate.currentDate().toString("ddd")
        print(current_day)

        # Check if the current day is in the selected days
        if current_day in selected_days:
            print("yes today needs to be organized")

            if len(categorized_files) != 0:
                self.organize_chosen_files(tree_widget, duplicates_checkbox, selected_folder_paths_automated, excluded_tree)


        else:
            print("nothing needs to be organized today")

    def get_selected_folder_paths_automated(self):
        return self.selected_folder_paths_automated

    # EXTENSION BROWSER
    def toggle_select_all_items(self, list_widget):
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setSelected(True)
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def combine_items_into_single_list(self, folder_list, items_tree):
        global categorized_files, excluded_files

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


        self.update_and_group_files_by_category_helper(included_tree, excluded_tree)

        print(self.excluded_files)

    def check_saved_items(self,treeWidget):
        global checked_items

        # Iterate through the treeWidget items and check those not in checked_items
        for tree_item in treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
            tree_item.setCheckState(0, QtCore.Qt.Unchecked)

        # Iterate through checked_items and set check state to Checked
        for folder_path, folders in tester.items():
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

    # JSON
    # Function to save the state of the "Remove Duplicates" checkbox
    def save_remove_duplicates_state(self, state):
        with open('remove_duplicates_state.pickle', 'wb') as file:
            pickle.dump(state, file)

    # Function to load the state of the "Remove Duplicates" checkbox
    def load_remove_duplicates_state(self):
        try:
            with open('remove_duplicates_state.pickle', 'rb') as file:
                state = pickle.load(file)
                return state
        except FileNotFoundError:
            return False  # Default to False if the file doesn't exist or hasn't been saved yet

    # Function to save the dictionary to a file
    def save_excluded_files(self):
        global excluded_files
        # Check if the dictionary is not empty before saving
        if self.excluded_files:
            with open("excluded_files.json", 'w') as file:
                json.dump(self.excluded_files, file)

    # Function to load the dictionary from a file
    def load_excluded_files(self, included_tree, excluded_tree):
        global excluded_files

        try:
            with open("excluded_files.json", 'r') as file:
                # Check if the file is not empty before loading
                if os.path.getsize("excluded_files.json") > 0:
                    self.excluded_files = json.load(file)
                    self.update_and_group_files_by_category_helper(included_tree, excluded_tree)
                else:
                    print("excluded_files.json is empty.")
        except FileNotFoundError:
            print("excluded_files.json not found.")

    def save_selected_folders(self):
        if self.is_automated:
            self.folders = self.selected_folder_paths_automated
            json_string = "selected_folders_automated.json"
        else:
            self.folders = self.selected_folder_paths_manual
            json_string = "selected_folders_manual.json"

        # Check if the list is not empty before saving
        if self.folders:
            with open(json_string, "w") as json_file:
                json.dump(self.folders, json_file)

    def load_selected_folders(self, listWidget, treeWidget):
        if self.is_automated:
            json_string = "selected_folders_automated.json"
        else:
            json_string = "selected_folders_manual.json"

        if os.path.exists(json_string):
            # Check if the file is not empty before loading
            if os.path.getsize(json_string) > 0:
                with open(json_string, "r") as json_file:
                    global selected_folder_paths_manual, selected_folder_paths_automated
                    folders = json.load(json_file)
                    if self.is_automated:
                        self.selected_folder_paths_automated = folders
                    else:
                        self.selected_folder_paths_manual = folders

                    self.refresh_list_widget(listWidget, folders)  # Update the list widget with the loaded folder paths
                    self.group_files_by_category(treeWidget, folders)
            else:
                print(f"{json_string} is empty.")

    def load_checked_items(self, treeWidget):
        if self.is_automated:
            global tester
            # Check if the JSON file with checked item state exists
            if os.path.exists("checked_items.json"):
                # Check if the file is not empty before loading
                if os.path.getsize("checked_items.json") > 0:
                    with open("checked_items.json", "r") as json_file:
                        tester = json.load(json_file)
                        self.check_saved_items(treeWidget)
                else:
                    print("checked_items.json is empty.")

    def save_checked_items(self):
        if self.is_automated:
            global tester
            # Check if the dictionary is not empty before saving
            if tester:
                with open("checked_items.json", "w") as json_file:
                    json.dump(tester, json_file)

    checkbox_states = {}

    def save_selected_days(self, day_checkboxes_dict):
        # Check if the dictionary is not empty before saving
        if day_checkboxes_dict:
            with open('checkbox_states.json', 'w') as f:
                json.dump({day: checkbox.isChecked() for day, checkbox in day_checkboxes_dict.items()}, f)

    def load_selected_days(self):
        try:
            with open('checkbox_states.json', 'r') as f:
                data = json.load(f)
                return data

        except FileNotFoundError:
            pass

    def save_toggle_state(self,is_toggled):
        config_data = {"is_toggled": is_toggled}
        with open("toggle_state.json", "w") as file:
            json.dump(config_data, file)

    def load_toggle_state(self):
        global is_toggled
        # Check if the configuration file exists
        if os.path.isfile("toggle_state.json"):
            # Check if the file is not empty before loading
            if os.path.getsize("toggle_state.json") > 0:
                with open("toggle_state.json", "r") as file:
                    config_data = json.load(file)
                    is_toggled = config_data.get("is_toggled")
                    return is_toggled
            else:
                print("toggle_state.json is empty.")
        else:
            is_toggled = False
            return is_toggled







