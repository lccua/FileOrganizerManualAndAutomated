
# third party imports

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
        selected_folders = folder_list.selectedItems()

        selected_item = items_tree.selectedItems()[0]

        depth = self.shared_model.get_item_depth(selected_item)

        for folder in selected_folders:
            selected_folder_name = folder.text()

            # Initialize a reference to the current level of the nested dictionary

            current_level = self.state.excluded_files




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


        self.shared_model.update_tree_views(self.state.included_tree, self.state.excluded_tree)

        print(self.state.excluded_files)
