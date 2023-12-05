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




















