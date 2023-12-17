from model.FileBrowserModel import FileBrowserModel
from model.SharedFileOrganizerModel import SharedFileOrganizerModel
from model.FileOrganizerStateManager import FileOrganizerStateManager



class ExtensionBrowseController:
    def __init__(self):
        self.browse_model = FileBrowserModel()
        self.shared_model = SharedFileOrganizerModel()
        self.state = FileOrganizerStateManager()


        self.state.is_automated = True
        self.state.is_browse_window = True


    def add_files_types_to_excluded_files(self,listView, treeView):
        self.browse_model.add_files_types_to_excluded_files(listView, treeView)

    def toggle_select_all_items(self, listView):
        self.shared_model.toggle_select_all_items(listView)

    def refresh_list_widget(self,list_view):
        self.shared_model.refresh_list_widget(list_view)

    def fill_tree_with_data(self, treeView):
        self.shared_model.fill_tree_with_data(treeView)