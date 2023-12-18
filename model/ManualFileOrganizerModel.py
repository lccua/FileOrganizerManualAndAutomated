# model.py

# third party imports
from PyQt5 import QtCore

# system imports

# local imports
from model.FileOrganizerStateManager import FileOrganizerStateManager

class ManualFileOrganizerModel:
    def __init__(self):
        self.state = FileOrganizerStateManager()


    """---- MANUAL METHODS ----"""

    def get_unchecked_items(self, treeWidget):
        """
        Collects and stores the identifiers of unchecked items from a tree widget.

        This method iterates through the items in the tree widget to find and store
        the text of all unchecked items at the fourth level of the tree.

        :param treeWidget: The tree widget to be inspected for unchecked items.
        """
        self.state.unchecked_items = []

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
                            # Assuming the item's text is the identifier
                            self.state.unchecked_items.append(fourth_level_item.text(0))

    def remove_unchecked_items_from_categorized_files(self, treeWidget):
        """
        Removes unchecked items from the categorized files.

        This method first retrieves the unchecked items from the tree widget and then
        filters out these items from the state's categorized files.

        :param treeWidget: The tree widget from which to identify unchecked items.
        """
        self.get_unchecked_items(treeWidget)

        for category, subcategories in list(self.state.categorized_files.items()):
            for subcategory, filetypes in list(subcategories.items()):
                for filetype, files in list(filetypes.items()):
                    # Filter out unchecked items from the fourth level
                    self.state.categorized_files[category][subcategory][filetype] = [
                        file for file in files if file not in self.state.unchecked_items
                    ]

                    # Remove empty file types
                    if not self.state.categorized_files[category][subcategory][filetype]:
                        del self.state.categorized_files[category][subcategory][filetype]

                # Remove empty subcategories
                if not self.state.categorized_files[category][subcategory]:
                    del self.state.categorized_files[category][subcategory]

            # Remove empty categories
            if not self.state.categorized_files[category]:
                del self.state.categorized_files[category]