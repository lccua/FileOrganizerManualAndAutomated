import json


class FileOrganizerStateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileOrganizerStateManager, cls).__new__(cls)

            cls._instance.is_automated = None
            cls._instance.is_toggled = False
            cls._instance.is_browse_window = None

            cls._instance.included_tree = None
            cls._instance.excluded_tree = None

            cls._instance.checked_items = {}

            cls._instance.categorized_files = {}
            cls._instance.excluded_files = {}

            cls._instance.checkboxes = {}

            cls._instance.selected_folder_paths_manual = []
            cls._instance.selected_folder_paths_automated = []

            cls._instance.day_checkboxes_dict = {}

            cls._instance.checkbox_states = {}

            cls._instance.config = {}
            cls._instance.load_config()

        return cls._instance

    def __init__(self):
        # Ensure initialization happens only once
        if not hasattr(self, '_initialized'):
            # Call any setup methods or any additional initialization here if needed
            self._initialized = True

    def load_config(self):
        with open('file_categories.json', 'r') as file:
            self.config = json.load(file)