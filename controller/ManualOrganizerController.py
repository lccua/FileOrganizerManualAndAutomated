from model.FileOrganizerModel import FileOrganizerModel


class ManualFileOrganizerController:
    def __init__(self):
        self.model = FileOrganizerModel()



    def load_selected_folders(self, folder_selector_list):
        self.model.load_selected_folders(folder_selector_list)

    def categorize_files(self, file_overview_tree, folders):
        self.model.categorize_files(file_overview_tree,folders)

    def open_and_select_folder(self, folder_selector_list, file_overview_tree):
        self.model.open_and_select_folder(folder_selector_list, file_overview_tree)

    def toggle_select_all(self, file_overview_tree):
        self.model.toggle_select_all(file_overview_tree)

    def organize_chosen_files(self, file_overview_tree, remove_duplicates_checkbox, folders):
        self.model.organize_chosen_files(file_overview_tree,remove_duplicates_checkbox, folders)

    def delete_selected_folder(self, folder_selector_list, file_overview_tree):
        self.model.delete_selected_folder(folder_selector_list, file_overview_tree)
