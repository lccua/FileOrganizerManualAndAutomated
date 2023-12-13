from model.FileOrganizerModel import FileOrganizerModel


class ExtensionBrowseController:
    def __init__(self):
        self.model = FileOrganizerModel()

        self.model.is_automated = True
        self.model.is_browse_window = True


    def combine_items_into_single_list(self,listView, treeView):
        self.model.combine_items_into_single_list(listView, treeView)

    def toggle_select_all_items(self, listView):
        self.model.toggle_select_all_items(listView)

    def refresh_list_widget(self,list_view, folders):
        self.model.refresh_list_widget(list_view, folders)

    def fill_tree_with_data(self, treeView):
        self.model.fill_tree_with_data(treeView)

    def get_selected_folder_paths_automated(self):
        return self.model.get_selected_folder_paths_automated()

    def post_excluded_files(self, excluded_files):
        self.model.post_excluded_files(excluded_files)




