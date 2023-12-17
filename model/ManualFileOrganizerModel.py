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
from model.FileOrganizerStateManager import FileOrganizerStateManager


class ManualFileOrganizerModel:
    def __init__(self):
        self.state = FileOrganizerStateManager()



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

    def remove_unchecked_items_from_categorized_files(self, categorized_files, unchecked_items):
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