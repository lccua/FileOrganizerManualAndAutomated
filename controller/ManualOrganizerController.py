from model.FileOrganizerModel import FileOrganizerModel


class ManualFileOrganizerController:
    def __init__(self):
        self.model = FileOrganizerModel()

        self.model.is_automated = False
        self.model.is_browse_window = False


    def load_selected_folders(self, folder_selector_list, file_overview_tree ):
        self.model.load_selected_folders(folder_selector_list, file_overview_tree)

    def group_files_by_category(self, file_overview_tree, folders):
        self.model.group_files_by_category(file_overview_tree,folders)

    def select_and_display_folder_contents(self, folder_selector_list, file_overview_tree):
        self.model.select_and_display_folder_contents(folder_selector_list, file_overview_tree)

    def toggle_select_all_items(self, file_overview_tree):
        self.model.toggle_select_all_items(file_overview_tree)

    def organize_chosen_files(self, file_overview_tree, remove_duplicates_checkbox):
        self.model.organize_chosen_files(file_overview_tree,remove_duplicates_checkbox)

    def delete_selected_folder_and_contents(self, folder_selector_list, file_overview_tree):
        self.model.delete_selected_folder_and_contents(folder_selector_list, file_overview_tree)
