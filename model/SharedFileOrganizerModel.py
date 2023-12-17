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
from model.ManualFileOrganizerModel import ManualFileOrganizerModel
from model.FileOrganizerStateManager import FileOrganizerStateManager

class SharedFileOrganizerModel:
    def __init__(self):
        self.manual_model = ManualFileOrganizerModel()
        self.state = FileOrganizerStateManager()


    """---- SHARED METHODS ----"""

    def select_and_display_folder_contents(self, listWidget, treeWidget, excluded_tree=None):
        # Create options for the file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Add the ReadOnly option

        # Open the folder dialog and get the selected folder path
        folder_path = QFileDialog.getExistingDirectory(None, "Select a folder", options=options)

        if self.state.is_automated:
            self.selected_folders = self.state.selected_folder_paths_automated
        else:
            self.selected_folders = self.state.selected_folder_paths_manual

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
                    if self.state.is_automated:
                        self.state.selected_folder_paths_automated.append(folder_path)

                        # Update and add the selected folder to the list widget
                        self.refresh_list_widget(listWidget)

                        self.update_tree_views(treeWidget, excluded_tree)

                    else:
                        self.state.selected_folder_paths_manual.append(folder_path)

                        # Update and add the selected folder to the list widget
                        self.refresh_list_widget(listWidget)

                        # Categorize the files
                        self.group_files_by_category(treeWidget, self.state.selected_folder_paths_manual)

    def toggle_select_all_items(self, list_widget):
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setSelected(True)
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def organize_chosen_files(self, treeWidget, remove_duplicates_checkbox, excluded_tree=None):

        if self.state.is_automated == False:
            unchecked_items = self.manual_model.get_unchecked_items(treeWidget)
            self.manual_model.remove_unchecked_items_from_categorized_files(self.categorized_files, unchecked_items)

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
        self.categorized_files = {}  # Clear the categorized_files dictionary

        self.update_tree_views(treeWidget, excluded_tree)

    def fill_tree_with_data(self, treeWidget, file_categories=None, item=None):
        # Loop through keys and values in the categorized_files_dictionary

        if file_categories == None:
            file_categories = self.state.config

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

            if not self.state.is_automated:
                # Only add checkboxes if is_automated is False
                tree_view_item.setFlags(tree_view_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                tree_view_item.setCheckState(0, Qt.Unchecked)

            if isinstance(values, dict):
                # When it encounters a dictionary as a value, there are nested items or subcategories to be added.
                self.fill_tree_with_data(treeWidget, values, tree_view_item)

            elif isinstance(values, list):
                if self.state.is_browse_window or not self.state.is_automated:

                    # Loop through each filename in the list
                    for filename in values:
                        # Create a new child item under the current item
                        child = QtWidgets.QTreeWidgetItem(tree_view_item)
                        # Set the text of the child item to the filename
                        child.setText(0, filename)

                        if not self.state.is_automated:
                            # Add special attributes for user interaction to the child item
                            child.setFlags(child.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsTristate)
                            # Set the initial check state of the child item to unchecked
                            child.setCheckState(0, Qt.Unchecked)

        # After populating the tree with categorized_files, sort the items alphabetically
        treeWidget.sortItems(0, Qt.AscendingOrder)

    def group_files_by_category(self, treeWidget, selected_folder_paths):
        self.categorized_files = {}

        for source_folder in selected_folder_paths:
            # Loop through files in the source folder
            for filename in os.listdir(source_folder):
                file_extension = os.path.splitext(filename)[1]
                if file_extension:
                    # Look for the file extension in the dictionary file_categories
                    for category, extensions in self.state.config.items():
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

        if self.state.is_browse_window == False:
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
            if self.state.excluded_files:
                self.fill_tree_with_data(excluded_tree, self.state.excluded_files)

    def group_files_by_category_helper(self, included_tree):
        folder_paths = self.state.selected_folder_paths_automated if self.state.is_automated else self.state.selected_folder_paths_manual
        self.group_files_by_category(included_tree, folder_paths)

    def remove_excluded_from_categorized(self):
        if self.categorized_files:
            self.delete_items_from_dict(self.categorized_files, self.state.excluded_files)

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
        if not self.state.is_browse_window:
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
        selected_folder_paths = self.state.selected_folder_paths_automated if self.state.is_automated else self.state.selected_folder_paths_manual
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
        selected_folder_paths = self.state.selected_folder_paths_automated if self.state.is_automated else self.state.selected_folder_paths_manual
        listWidget.addItems(selected_folder_paths)

    def remove_folder_from_categorized_files(self, selected_item):
        """
        Removes the selected folder from the categorized files dictionary.

        Parameters:
        selected_item (str): The folder path to be removed.
        """
        if selected_item in self.categorized_files:
            del self.categorized_files[selected_item]

    def refresh_list_widget(self, listWidget):
        # Clear the existing items in the list widget
        listWidget.clear()
        # Add the selected folder paths to the list widget

        if self.state.is_automated == True:
            selected_folder_paths = self.state.selected_folder_paths_automated
        else:
            selected_folder_paths = self.state.selected_folder_paths_manual

        listWidget.addItems(selected_folder_paths)

    def get_item_depth(self, tree_item):
        depth = 0
        parent = tree_item.parent()
        while parent is not None:
            depth += 1
            parent = parent.parent()
        return depth



