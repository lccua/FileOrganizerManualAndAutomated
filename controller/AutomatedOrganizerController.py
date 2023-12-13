from view.ExtensionBrowseView import ExtensionBrowseView
from model.FileOrganizerModel import FileOrganizerModel

class AutomatedFileOrganizerController:
    def __init__(self):
        self.model = FileOrganizerModel()

        self.model.is_automated = True
        self.model.is_browse_window = False


    def delete_selected_folder_and_contents(self, folder_selector_list, file_overview_tree, excluded_items_tree):
        self.model.delete_selected_folder_and_contents(folder_selector_list, file_overview_tree, excluded_items_tree)

    def select_and_display_folder_contents(self, folder_selector_list, file_overview_tree, excluded_items_tree):
        self.model.select_and_display_folder_contents(folder_selector_list, file_overview_tree, excluded_items_tree)

    def include_files(self, file_overview_tree, excluded_items_tree):
        self.model.include_files(file_overview_tree, excluded_items_tree)

    def exclude_files(self, file_overview_tree, excluded_items_tree):
        self.model.exclude_files(file_overview_tree, excluded_items_tree)

    def check_current_day(self, selected_days, remove_duplicates_checkbox, file_overview_tree, excluded_items_tree):
        self.model.check_current_day(selected_days, remove_duplicates_checkbox, file_overview_tree, excluded_items_tree)

    def open_browse_view(self):
        folders = self.get_selected_folder_paths_automated()
        excluded_files = self.get_excluded_files()
        self.browse_view = ExtensionBrowseView(folders,excluded_files )
        self.browse_view.show()

    def get_excluded_tree(self, excluded_items_tree):
        self.model.get_excluded_tree(excluded_items_tree)

    def get_included_tree(self, file_overview_tree):
        self.model.get_included_tree(file_overview_tree)

    def get_selected_folder_paths_automated(self):
        return self.model.get_selected_folder_paths_automated()

    def get_excluded_files(self):
        return self.model.get_excluded_files()

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

    def save_selected_days(self,day_checkboxes_dict):
        self.model.save_selected_days(day_checkboxes_dict)

    def save_toggle_state(self, is_toggled):
        self.model.save_toggle_state(is_toggled)

    def save_excluded_files(self):
        self.model.save_excluded_files()






















