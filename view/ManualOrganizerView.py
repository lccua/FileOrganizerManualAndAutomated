from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget
from controller.ManualOrganizerController import ManualFileOrganizerController


class ManualOrganizerView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ManualFileOrganizerController()

        self.folders = []

        self.create_layout()


        self.connect_signals()

    def create_layout(self):
        # Set the window title
        self.setWindowTitle('First Window')

        # Set the fixed size of the window
        self.setFixedSize(852, 540)

        # Create a horizontal layout widget for the main content
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(60, 110, 731, 351))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")

        # Create a grid layout for organizing widgets
        self.main_grid_layout = QtWidgets.QGridLayout()
        self.main_grid_layout.setHorizontalSpacing(111)
        self.main_grid_layout.setVerticalSpacing(0)
        self.main_grid_layout.setObjectName("main_grid_layout")

        # Create "Delete Folder" button
        self.delete_folder_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.delete_folder_button.setObjectName("delete_folder_button")
        self.delete_folder_button.setText("Delete Folder")


        # Create a horizontal layout for folder selector buttons
        self.folder_selector_button_layout = QtWidgets.QHBoxLayout()
        self.folder_selector_button_layout.setContentsMargins(0, 10, -1, -1)
        self.folder_selector_button_layout.setSpacing(30)
        self.folder_selector_button_layout.setObjectName("folder_selector_button_layout")

        # Add folder selector button layout to the main grid layout
        self.main_grid_layout.addLayout(self.folder_selector_button_layout, 2, 0, 1, 1)

        # Create a horizontal layout for excluded items buttons
        self.excluded_items_button_layout = QtWidgets.QHBoxLayout()
        self.excluded_items_button_layout.setContentsMargins(0, 10, -1, -1)
        self.excluded_items_button_layout.setSpacing(30)
        self.excluded_items_button_layout.setObjectName("excluded_items_button_layout")

        # Create "Select All" button
        self.organize_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.organize_button.setObjectName("organize_button")
        self.organize_button.setText("Organize Files")
        self.excluded_items_button_layout.addWidget(self.organize_button)



        # Add excluded items button layout to the main grid layout
        self.main_grid_layout.addLayout(self.excluded_items_button_layout, 2, 1, 1, 1)

        # Create a horizontal layout for file overview buttons
        self.file_overview_button_layout = QtWidgets.QHBoxLayout()
        self.file_overview_button_layout.setContentsMargins(0, 10, -1, -1)
        self.file_overview_button_layout.setSpacing(30)
        self.file_overview_button_layout.setObjectName("file_overview_button_layout")

        # Create "Add Folder" button
        self.add_folder_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.add_folder_button.setObjectName("add_folder_button")
        self.add_folder_button.setText("Add Folder")

        # Create a list widget for folder selection
        self.folder_selector_list = QtWidgets.QListWidget(self.horizontalLayoutWidget_3)
        self.folder_selector_list.setObjectName("folder_selector_list")
        self.main_grid_layout.addWidget(self.folder_selector_list, 0, 0, 1, 1)


        # Create a tree widget for displaying data
        self.file_overview_tree = QtWidgets.QTreeWidget(self.horizontalLayoutWidget_3)
        self.file_overview_tree.setObjectName("file_overview_tree")
        self.file_overview_tree.setHeaderHidden(True)
        self.main_grid_layout.addWidget(self.file_overview_tree, 0, 1, 1, 1)


        self.folder_selector_button_layout.addWidget(self.add_folder_button)

        self.folder_selector_button_layout.addWidget(self.delete_folder_button)

        # Add file overview button layout to the main grid layout
        self.main_grid_layout.addLayout(self.file_overview_button_layout, 1, 1, 1, 1)

        # Create a horizontal layout for the main content
        self.main_horizontal_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.main_horizontal_layout.setContentsMargins(50, 0, 50, 0)
        self.main_horizontal_layout.setObjectName("main_horizontal_layout")

        # Add the main grid layout to the main horizontal layout
        self.main_horizontal_layout.addLayout(self.main_grid_layout)



        # Create a label for file overview
        self.file_overview_label = QtWidgets.QLabel(self)
        self.file_overview_label.setGeometry(QtCore.QRect(470, 50, 271, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.file_overview_label.setFont(font)
        self.file_overview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_overview_label.setObjectName("file_overview_label")
        self.file_overview_label.setText("File Overview")

        # Create a label for folder selector
        self.folder_selector_label = QtWidgets.QLabel(self)
        self.folder_selector_label.setGeometry(QtCore.QRect(90, 50, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.folder_selector_label.setFont(font)
        self.folder_selector_label.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_selector_label.setObjectName("folder_selector_label")
        self.folder_selector_label.setText("Folder Selector")






        # Create a checkbox for removing duplicates
        self.remove_duplicates_checkbox = QtWidgets.QCheckBox(self)
        self.remove_duplicates_checkbox.setGeometry(QtCore.QRect(363, 480, 151, 20))
        self.remove_duplicates_checkbox.setChecked(False)
        self.remove_duplicates_checkbox.setObjectName("remove_duplicates_checkbox")
        self.remove_duplicates_checkbox.setText("Remove Duplicates")

    def connect_signals(self):
        self.delete_folder_button.clicked.connect(
            lambda: self.controller.delete_selected_folder_and_contents(self.folder_selector_list, self.file_overview_tree))

        self.organize_button.clicked.connect(
            lambda: self.controller.organize_chosen_files(self.file_overview_tree, self.remove_duplicates_checkbox))

        self.add_folder_button.clicked.connect(
            lambda: self.controller.select_and_display_folder_contents(self.folder_selector_list, self.file_overview_tree))

