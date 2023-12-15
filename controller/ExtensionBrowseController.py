from model.FileOrganizerModel import FileOrganizerModel


class ExtensionBrowseController:
    def __init__(self):
        self.model = FileOrganizerModel()

        self.model.is_automated = True
        self.model.is_browse_window = True


    def add_files_types_to_excluded_files(self,listView, treeView):
        self.model.add_files_types_to_excluded_files(listView, treeView)

    def toggle_select_all_items(self, listView):
        self.model.toggle_select_all_items(listView)

    def refresh_list_widget(self,list_view):
        self.model.refresh_list_widget(list_view)

    def fill_tree_with_data(self, treeView):
        self.model.fill_tree_with_data(treeView)