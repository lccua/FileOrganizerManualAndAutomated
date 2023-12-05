from model.FileOrganizerModel import FileOrganizerModel


class ExtensionBrowseController:
    def __init__(self):
        self.model = FileOrganizerModel()

        self.model.is_automated = True



    def merge_items_together(self,listView, treeView):
        self.model.merge_items_together(listView, treeView)

    def toggle_select_all(self, listView):
        self.model.toggle_select_all(listView)

    def update_list_widget(self,list_view, folders):
        self.model.update_list_widget(list_view, folders)

    def populate_tree(self, treeView,FILE_CATEGORIES, is_browse_window):
        self.model.populate_tree(treeView, FILE_CATEGORIES, is_browse_window)

    def get_selected_folder_paths_automated(self):
        return self.model.get_selected_folder_paths_automated()




