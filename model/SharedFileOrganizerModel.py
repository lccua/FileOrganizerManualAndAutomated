# SharedFileOrganizerModel.py

# third party imports
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# system imports
import os
import hashlib
import shutil

# local imports
from model.ManualFileOrganizerModel import ManualFileOrganizerModel
from model.FileOrganizerStateManager import FileOrganizerStateManager

class SharedFileOrganizerModel:
    def __init__(self):
        self.manual_model = ManualFileOrganizerModel()
        self.state = FileOrganizerStateManager()


    """---- SHARED METHODS ----"""

    def select_and_display_folder_contents(self, listWidget, treeWidget, excluded_tree=None):
        """
        Opens a folder dialog, validates the selected folder, and updates UI components.

        :param listWidget: The list widget to be updated.
        :param treeWidget: The tree widget to be updated.
        :param excluded_tree: The tree widget for excluded items (optional).
        """
        folder_path = self._open_folder_dialog()

        if not folder_path:
            return

        if self._is_folder_already_selected(folder_path):
            self.show_warning("Folder Already Selected", "This folder has already been selected.")
            return

        if not self._has_files_with_extensions(folder_path):
            self.show_warning("No Files with Extensions", "There are no files in this folder.")
            return

        self._add_folder_to_selected(folder_path)
        self._update_ui(listWidget, treeWidget, excluded_tree)

    def _open_folder_dialog(self):
        """
        Opens a dialog for the user to select a folder and returns the selected folder path.

        :return: The path of the selected folder.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        return QFileDialog.getExistingDirectory(None, "Select a folder", options=options)

    def _is_folder_already_selected(self, folder_path):
        """
        Checks if the selected folder is already in the list of selected folders.

        :param folder_path: The path of the folder to check.
        :return: True if the folder is already selected, False otherwise.
        """
        self.selected_folders = self.state.selected_folder_paths_automated if self.state.is_automated else self.state.selected_folder_paths_manual
        return folder_path in self.selected_folders

    def _has_files_with_extensions(self, folder_path):
        """
        Checks if the selected folder contains files with extensions.

        :param folder_path: The path of the folder to check.
        :return: True if there are files with extensions, False otherwise.
        """
        return any(os.path.isfile(os.path.join(folder_path, filename)) for filename in os.listdir(folder_path))

    def _add_folder_to_selected(self, folder_path):
        """
        Adds the selected folder to the list of selected folders.

        :param folder_path: The path of the folder to add.
        """
        selected_folders = self.state.selected_folder_paths_automated if self.state.is_automated else self.state.selected_folder_paths_manual
        selected_folders.append(folder_path)

    def _update_ui(self, listWidget, treeWidget, excluded_tree):
        """
        Refreshes the UI components with the updated list of selected folders.

        :param listWidget: The list widget to refresh.
        :param treeWidget: The tree widget to refresh.
        :param excluded_tree: The tree widget for excluded items (optional).
        """
        self.refresh_list_widget(listWidget)
        if self.state.is_automated:
            self.update_tree_views_helper(treeWidget, excluded_tree)
        else:
            self.group_files_by_category(treeWidget, self.state.selected_folder_paths_manual)





    def show_warning(self, title, message):
        """
        Displays a warning message box.

        :param title: The title of the message box.
        :param message: The warning message to display.
        """
        QMessageBox.warning(None, title, message)




    def fill_tree_with_data(self, treeWidget, file_categories=None, item=None):
        """
        Populates a tree widget with data from file categories.

        :param treeWidget: The tree widget to fill.
        :param file_categories: Dictionary of file categories and their values.
        :param item: The parent item under which to add new items (None for top-level).
        """
        if file_categories is None:
            file_categories = self.state.config

        for category_or_extension_name, values in file_categories.items():
            tree_view_item = self._create_tree_item(treeWidget, category_or_extension_name, item)

            if isinstance(values, dict):
                # Recursive call for nested items or subcategories
                self.fill_tree_with_data(treeWidget, values, tree_view_item)
            elif isinstance(values, list) and (self.state.is_browse_window or not self.state.is_automated):
                self._add_file_names_as_children(tree_view_item, values)

        treeWidget.sortItems(0, Qt.AscendingOrder)

    def _create_tree_item(self, treeWidget, text, parent_item=None):
        """
        Creates a new item in the tree widget.

        :param treeWidget: The tree widget where the item is to be created.
        :param text: Text for the tree item.
        :param parent_item: The parent item under which the new item will be created (None for top-level).
        :return: The created tree item.
        """
        tree_view_item = QtWidgets.QTreeWidgetItem(parent_item if parent_item else treeWidget)
        tree_view_item.setText(0, text)

        if not self.state.is_automated:
            tree_view_item.setFlags(tree_view_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            tree_view_item.setCheckState(0, Qt.Unchecked)

        return tree_view_item

    def _add_file_names_as_children(self, parent_item, file_names):
        """
        Adds file names as child items to a parent item in the tree widget.

        :param parent_item: The parent tree item under which to add child items.
        :param file_names: List of file names to add as child items.
        """
        for filename in file_names:
            child = QtWidgets.QTreeWidgetItem(parent_item)
            child.setText(0, filename)

            if not self.state.is_automated:
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsTristate)
                child.setCheckState(0, Qt.Unchecked)




    def group_files_by_category(self, treeWidget, selected_folder_paths):
        """
        Groups files by their category based on file extensions and updates the tree widget.

        :param treeWidget: The tree widget to be updated with categorized files.
        :param selected_folder_paths: List of paths to folders whose files are to be categorized.
        """
        self.state.categorized_files = self._categorize_files(selected_folder_paths)

        if not self.state.is_browse_window:
            treeWidget.clear()
            self.fill_tree_with_data(treeWidget, self.state.categorized_files)

    def _categorize_files(self, folder_paths):
        """
        Categorizes files in the given folders into a nested dictionary based on their extensions.

        :param folder_paths: List of folder paths to categorize files from.
        :return: A nested dictionary categorizing files by their folder, category, and extension.
        """
        categorized_files = {}
        for folder in folder_paths:
            for filename in os.listdir(folder):
                category, file_extension = self._find_file_category_and_extension(filename)
                if category:
                    self._add_file_to_category(categorized_files, folder, category, file_extension, filename)
        return categorized_files

    def _find_file_category_and_extension(self, filename):
        """
        Finds the category and file extension for a given filename.

        :param filename: The filename to categorize.
        :return: A tuple of (category, file_extension). Returns (None, None) if no category is found.
        """
        file_extension = os.path.splitext(filename)[1]
        if file_extension:
            for category, extensions in self.state.config.items():
                if file_extension in extensions:
                    return category, file_extension
        return None, None

    def _add_file_to_category(self, categorized_files, folder, category, file_extension, filename):
        """
        Adds a file to the categorized_files dictionary under the appropriate category and file extension.

        :param categorized_files: The dictionary to add the file to.
        :param folder: The source folder of the file.
        :param category: The category of the file.
        :param file_extension: The file extension.
        :param filename: The filename to add.
        """
        if folder not in categorized_files:
            categorized_files[folder] = {}
        if category not in categorized_files[folder]:
            categorized_files[folder][category] = {}
        if file_extension not in categorized_files[folder][category]:
            categorized_files[folder][category][file_extension] = []

        categorized_files[folder][category][file_extension].append(filename)




    def organize_chosen_files(self, treeWidget, remove_duplicates_checkbox, excluded_tree=None):
        """
        Organizes selected files based on their categories and optionally removes duplicates.

        :param treeWidget: The tree widget containing file information.
        :param remove_duplicates_checkbox: Checkbox indicating whether to remove duplicates.
        :param excluded_tree: Tree widget containing excluded items (optional).
        """
        if not self.state.is_automated:
            self.manual_model.remove_unchecked_items_from_categorized_files(treeWidget)

        for folder_path, folders in self.state.categorized_files.items():
            for category, categories in folders.items():
                for file_type, file_types in categories.items():
                    self._organize_files_in_category(folder_path, category, file_type, file_types,
                                                     remove_duplicates_checkbox)

        self._refresh_ui(treeWidget, excluded_tree)

    def _organize_files_in_category(self, folder_path, category, file_type, file_types, remove_duplicates_checkbox):
        """
        Organizes files within a specific category and file type.

        :param folder_path: Base folder path.
        :param category: The category of the files.
        :param file_type: The type of the files.
        :param file_types: List of file types.
        :param remove_duplicates_checkbox: Checkbox indicating whether to remove duplicates.
        """
        new_folder_path = os.path.join(folder_path, category, file_type[1:])
        os.makedirs(new_folder_path, exist_ok=True)

        for file in file_types:
            source_file = os.path.join(folder_path, file)
            destination_file = os.path.join(new_folder_path, file)

            if remove_duplicates_checkbox.isChecked():
                self._find_and_delete_duplicate_files(new_folder_path)

            try:
                shutil.move(source_file, destination_file)
                print(f"Moved '{file}' to '{destination_file}'")
            except Exception as e:
                print(f"Error moving '{file}' to '{destination_file}': {e}")

    def _find_and_delete_duplicate_files(self, directory):
        """
        Finds and deletes duplicate files in a given directory.

        :param directory: The directory to search for duplicate files.
        """
        file_hashes = {}
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_hash = self._calculate_file_hash(file_path)

                if file_hash in file_hashes:
                    print(f'Duplicate file found: {file_path} and {file_hashes[file_hash]}')
                    os.remove(file_path)
                    print(f'Deleted duplicate file: {file_path}')
                else:
                    file_hashes[file_hash] = file_path

    @staticmethod
    def _calculate_file_hash(file_path, hash_function=hashlib.md5, buffer_size=65536):
        """
        Calculates the hash of a file.

        :param file_path: Path of the file to hash.
        :param hash_function: Hash function to use (default: hashlib.md5).
        :param buffer_size: Buffer size for reading the file (default: 65536).
        :return: Hexadecimal hash of the file.
        """
        hash_obj = hash_function()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(buffer_size), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    def _refresh_ui(self, treeWidget, excluded_tree):
        """
        Refreshes the UI components after file organization.

        :param treeWidget: The tree widget to clear.
        :param excluded_tree: Tree widget containing excluded items (optional).
        """
        treeWidget.clear()
        self.state.categorized_files = {}
        self.update_tree_views_helper(treeWidget, excluded_tree)




    def update_tree_views_helper(self, included_tree, excluded_tree=None):
        """
        Updates the tree views with categorized and excluded files.

        Parameters:
        included_tree (QTreeWidget): Tree widget for included files.
        excluded_tree (QTreeWidget): Optional tree widget for excluded files.
        """
        self._clear_and_fill_excluded_tree(excluded_tree)
        self._group_files_by_category_helper(included_tree)
        self._remove_excluded_from_categorized()
        self._fill_included_tree(included_tree)

    def _clear_and_fill_excluded_tree(self, excluded_tree):
        if excluded_tree:
            excluded_tree.clear()
            if self.state.excluded_files:
                self.fill_tree_with_data(excluded_tree, self.state.excluded_files)

    def _group_files_by_category_helper(self, included_tree):
        folder_paths = self.state.selected_folder_paths_automated if self.state.is_automated else self.state.selected_folder_paths_manual
        self.group_files_by_category(included_tree, folder_paths)

    def _remove_excluded_from_categorized(self):
        if self.state.categorized_files:
            self._delete_items_from_dict(self.state.categorized_files, self.state.excluded_files)

    def _delete_items_from_dict(self, target_dict, items_to_delete):

        for key, value in items_to_delete.items():

            if isinstance(value, dict):
                # Recursively call the function to process nested dictionaries
                if key in target_dict:
                    self._delete_items_from_dict(target_dict[key], value)
                else:
                    print("lol")
                    continue
                # Check if the category is empty after processing
                if not target_dict[key]:
                    del target_dict[key]
            elif key in target_dict:
                # If the key exists in the target_dict, delete it
                del target_dict[key]

    def _fill_included_tree(self, included_tree):
        if not self.state.is_browse_window:
            included_tree.clear()
            self.fill_tree_with_data(included_tree, self.state.categorized_files)



    def delete_selected_folder_and_contents(self, listWidget, treeWidget, excluded_tree=None):
        """
        Deletes the selected folder and updates the UI accordingly.

        Parameters:
        listWidget (QListWidget): The widget listing the folders.
        treeWidget (QTreeWidget): The tree widget displaying folder structure.
        excluded_tree (QTreeWidget): Optional tree widget for excluded items.
        """
        selected_item = self._get_selected_folder(listWidget)
        if not selected_item:
            return

        if self._remove_folder_from_paths(selected_item):
            print("Deleted folder:", selected_item)
            self._update_folder_list_ui(listWidget)
            self._remove_folder_from_categorized_files(selected_item)
            self.update_tree_views_helper(treeWidget, excluded_tree)

    def _get_selected_folder(self, listWidget):
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

    def _remove_folder_from_paths(self, selected_item):
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

    def _update_folder_list_ui(self, listWidget):
        """
        Updates the folder list in the UI.

        Parameters:
        listWidget (QListWidget): The widget listing the folders.
        """
        listWidget.clear()
        selected_folder_paths = self.state.selected_folder_paths_automated if self.state.is_automated else self.state.selected_folder_paths_manual
        listWidget.addItems(selected_folder_paths)

    def _remove_folder_from_categorized_files(self, selected_item):
        """
        Removes the selected folder from the categorized files dictionary.

        Parameters:
        selected_item (str): The folder path to be removed.
        """
        if selected_item in self.state.categorized_files:
            del self.state.categorized_files[selected_item]




    def refresh_list_widget(self, listWidget):
        """
        Refreshes the list widget with the currently selected folder paths.

        This method clears the existing items in the list widget and adds the new selected folder paths,
        which are determined based on whether the operation mode is automated or manual.

        :param listWidget: The list widget to be refreshed.
        """
        listWidget.clear()
        selected_folder_paths = self._get_selected_folder_paths()
        listWidget.addItems(selected_folder_paths)

    def _get_selected_folder_paths(self):
        """
        Retrieves the selected folder paths based on the current operation mode.

        :return: A list of selected folder paths.
        """
        if self.state.is_automated:
            return self.state.selected_folder_paths_automated
        else:
            return self.state.selected_folder_paths_manual




    def get_item_depth(self, tree_item):
        """
        Calculates the depth of a given item in a tree.

        The depth is determined by counting the number of ancestors the item has.
        A top-level item (with no parent) has a depth of 0.

        :param tree_item: The tree item for which to calculate the depth.
        :return: The depth of the tree item.
        """
        depth = 0
        parent = tree_item.parent()
        while parent is not None:
            depth += 1
            parent = parent.parent()
        return depth