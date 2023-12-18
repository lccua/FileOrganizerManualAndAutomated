
# third party imports
from PyQt5 import QtWidgets

# system imports

# local imports
from model.SharedFileOrganizerModel import SharedFileOrganizerModel
from model.FileOrganizerStateManager import FileOrganizerStateManager



class FileBrowserModel:
    def __init__(self):
        self.shared_model = SharedFileOrganizerModel()
        self.state = FileOrganizerStateManager()


    """---- BROWSE METHODS ----"""

    def add_files_types_to_excluded_files(self, folder_list, items_tree):
        """
        Adds file types to the excluded files based on the selected items in the folder list and items tree.

        Excludes file types based on the depth of the selected item.
        If the depth is 0, all file types under the category are excluded.
        If the depth is 1, only the specific file type is excluded.

        :param folder_list: The list widget containing folders.
        :param items_tree: The tree widget containing file categories and types.
        """
        selected_folders = folder_list.selectedItems()
        selected_item = items_tree.selectedItems()[0]
        depth = self.shared_model.get_item_depth(selected_item)

        for folder in selected_folders:
            folder_path = folder.text()
            if folder_path not in self.state.excluded_files:
                self.state.excluded_files[folder_path] = {}

            if depth == 0:
                category = selected_item.text(0)
                self.state.excluded_files[folder_path][category] = {}
                for i in range(selected_item.childCount()):
                    file_type = selected_item.child(i).text(0)
                    self.state.excluded_files[folder_path][category][file_type] = []
            elif depth == 1:
                category = selected_item.parent().text(0)
                file_type = selected_item.text(0)
                if category not in self.state.excluded_files[folder_path]:
                    self.state.excluded_files[folder_path][category] = {}
                self.state.excluded_files[folder_path][category][file_type] = []
        self.shared_model.update_tree_views_helper(self.state.included_tree, self.state.excluded_tree)




    def toggle_select_all_items(self, list_widget):
        """
        Toggles the selection state of all items in the provided list widget.

        This method selects all items if none are selected, and deselects all if some are selected.

        :param list_widget: The list widget whose items are to be toggled.
        """
        self._set_selection_mode(list_widget, QtWidgets.QAbstractItemView.MultiSelection)
        self._toggle_items(list_widget)
        self._set_selection_mode(list_widget, QtWidgets.QAbstractItemView.SingleSelection)

    def _set_selection_mode(self, list_widget, mode):
        """
        Sets the selection mode for the list widget.

        :param list_widget: The list widget to modify.
        :param mode: The selection mode to set (e.g., MultiSelection, SingleSelection).
        """
        list_widget.setSelectionMode(mode)

    def _toggle_items(self, list_widget):
        """
        Toggles the selection state of all items in the list widget.

        If no items are selected, all will be selected. If any are selected, all will be deselected.

        :param list_widget: The list widget whose items are to be toggled.
        """
        all_selected = all(list_widget.item(index).isSelected() for index in range(list_widget.count()))
        new_state = not all_selected
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setSelected(new_state)
