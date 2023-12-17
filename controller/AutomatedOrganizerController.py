from view.ExtensionBrowseView import ExtensionBrowseView
from model.AutomatedFileOrganizerModel import AutomatedFileOrganizerModel
from model.SharedFileOrganizerModel import SharedFileOrganizerModel
from model.FileOrganizerStateManager import FileOrganizerStateManager



class AutomatedFileOrganizerController:
    def __init__(self):
        self.shared_model = SharedFileOrganizerModel()
        self.automated_model = AutomatedFileOrganizerModel()
        self.state = FileOrganizerStateManager()

        self.state.is_automated = True
        self.state.is_browse_window = False


    def delete_selected_folder_and_contents(self, folder_selector_list, file_overview_tree, excluded_items_tree):
        self.shared_model.delete_selected_folder_and_contents(folder_selector_list, file_overview_tree, excluded_items_tree)

    def select_and_display_folder_contents(self, folder_selector_list, file_overview_tree, excluded_items_tree):
        self.shared_model.select_and_display_folder_contents(folder_selector_list, file_overview_tree, excluded_items_tree)

    def include_files(self, file_overview_tree, excluded_items_tree):
        self.automated_model.include_files(file_overview_tree, excluded_items_tree)

    def exclude_files(self, file_overview_tree, excluded_items_tree):
        self.automated_model.exclude_files(file_overview_tree, excluded_items_tree)

    def check_current_day(self, file_overview_tree, remove_duplicates_checkbox, excluded_items_tree):
        self.automated_model.check_current_day(file_overview_tree, remove_duplicates_checkbox, excluded_items_tree)

    def open_browse_view(self):
        self.browse_view = ExtensionBrowseView()
        self.browse_view.show()

    def get_excluded_tree(self, excluded_items_tree):
        self.automated_model.get_excluded_tree(excluded_items_tree)

    def get_included_tree(self, file_overview_tree):
        self.automated_model.get_included_tree(file_overview_tree)


    def load_toggle_state(self):
        return self.automated_model.load_toggle_state()

    def load_selected_days(self):
        return self.automated_model.load_selected_days()

    def load_selected_folders(self, folder_selector_list):
        self.automated_model.load_selected_folders(folder_selector_list)

    def load_excluded_files(self, file_overview_tree, excluded_items_tree):
        self.automated_model.load_excluded_files(file_overview_tree, excluded_items_tree)

    def load_remove_duplicates_state(self):
        return self.automated_model.load_remove_duplicates_state()

    # SAVE JSON

    def save_remove_duplicates_state(self, remove_duplicates_state):
        self.automated_model.save_remove_duplicates_state(remove_duplicates_state)

    def save_selected_folders(self):
        self.automated_model.save_selected_folders()

    def save_selected_days(self,day_checkboxes_dict):
        self.automated_model.save_selected_days(day_checkboxes_dict)

    def save_toggle_state(self, is_toggled):
        self.automated_model.save_toggle_state(is_toggled)

    def save_excluded_files(self):
        self.automated_model.save_excluded_files()






















