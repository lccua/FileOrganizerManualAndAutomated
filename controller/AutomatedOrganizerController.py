from view.ExtensionBrowseView import ExtensionBrowseView
from model.FileOrganizerModel import FileOrganizerModel

class AutomatedFileOrganizerController:
    def __init__(self):
        self.model = FileOrganizerModel()

        self.model.is_automated = True


    def delete_selected_folder(self, folder_selector_list, file_overview_tree, excluded_items_tree):
        self.model.delete_selected_folder(folder_selector_list, file_overview_tree, excluded_items_tree)

    def open_and_select_folder(self, folder_selector_list, file_overview_tree, excluded_items_tree):
        self.model.open_and_select_folder(folder_selector_list, file_overview_tree, excluded_items_tree)

    def include_files(self, file_overview_tree, excluded_items_tree):
        self.model.include_files(file_overview_tree, excluded_items_tree)

    def exclude_files(self, file_overview_tree, excluded_items_tree):
        self.model.exclude_files(file_overview_tree, excluded_items_tree)

    def check_current_day(self, selected_days, remove_duplicates_checkbox, file_overview_tree, excluded_items_tree):
        self.model.check_current_day(selected_days, remove_duplicates_checkbox, file_overview_tree, excluded_items_tree)

    def open_browse_view(self):
        self.browse_view = ExtensionBrowseView()
        self.browse_view.show()

    def post_excluded_tree(self, excluded_items_tree):
        self.model.post_excluded_tree(excluded_items_tree)

    def post_included_tree(self, file_overview_tree):
        self.model.post_included_tree(file_overview_tree)
        
        

    def load_toggle_state(self):
        return self.model.load_toggle_state()

    def load_selected_days(self):
        return self.model.load_selected_days()

    def load_selected_folders(self, folder_selector_list, file_overview_tree):
        self.model.load_selected_folders(folder_selector_list,file_overview_tree)

    def load_excluded_files(self, file_overview_tree, excluded_items_tree):
        self.model.load_excluded_files(file_overview_tree, excluded_items_tree)

    def load_remove_duplicates_state(self):
        return self.model.load_remove_duplicates_state()

    # SAVE JSON

    def save_remove_duplicates_state(self, remove_duplicates_state):
        self.model.save_remove_duplicates_state(remove_duplicates_state)

    def save_selected_folders(self):
        self.model.save_selected_folders()

    def save_selected_days(self):
        self.model.save_selected_days()

    def save_toggle_state(self):
        self.model.save_toggle_state()

    def save_excluded_files(self):
        self.model.save_excluded_files()






















