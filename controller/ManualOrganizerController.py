from model.SharedFileOrganizerModel import SharedFileOrganizerModel
from model.FileOrganizerStateManager import FileOrganizerStateManager


class ManualFileOrganizerController:
    def __init__(self):
        self.shared_model = SharedFileOrganizerModel()
        self.state = FileOrganizerStateManager()

        self.state.is_automated = False
        self.state.is_browse_window = False

    def group_files_by_category(self, file_overview_tree, folders):
        self.shared_model.group_files_by_category(file_overview_tree,folders)

    def select_and_display_folder_contents(self, folder_selector_list, file_overview_tree):
        self.shared_model.select_and_display_folder_contents(folder_selector_list, file_overview_tree)


    def organize_chosen_files(self, file_overview_tree, remove_duplicates_checkbox):
        self.shared_model.organize_chosen_files(file_overview_tree,remove_duplicates_checkbox)

    def delete_selected_folder_and_contents(self, folder_selector_list, file_overview_tree):
        self.shared_model.delete_selected_folder_and_contents(folder_selector_list, file_overview_tree)
