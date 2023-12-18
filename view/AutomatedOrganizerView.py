from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox

from controller.AutomatedOrganizerController import AutomatedFileOrganizerController

from constants import *




class AutomatedOrganizerView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = AutomatedFileOrganizerController()

        # variables
        self.is_toggled = None
        self.is_toggled = self.controller.load_toggle_state()

        self.selected_days = []



        # creates the layout
        self.create_layout()



        self.day_checkboxes_dict = self.controller.load_selected_days()


        # Load the state of the "Remove Duplicates" checkbox when the application starts
        remove_duplicates_state = self.controller.load_remove_duplicates_state()
        if remove_duplicates_state is not None:
            self.remove_duplicates_checkbox.setChecked(remove_duplicates_state)




        self.controller.load_selected_folders(self.folder_selector_list)

        self.controller.load_excluded_files(self.file_overview_tree, self.excluded_items_tree)

        self.check_automation_toggle()
        self.create_day_checkboxes()
        self.set_automation_label_properties()
        self.set_automation_button_properties()

        self.controller.get_excluded_tree(self.excluded_items_tree)
        self.controller.get_included_tree(self.file_overview_tree)



        self.connect_signals()

    def create_layout(self):

        # Set the window title
        self.setWindowTitle('First Window')
        # Set the fixed size of the window
        self.setFixedSize(1221, 845)

        # Create a container for the checkboxes related to days of the week
        self.days_checkboxes_container = QtWidgets.QWidget(self)
        self.days_checkboxes_container.setGeometry(QtCore.QRect(10, 140, 1201, 22))
        self.days_checkboxes_container.setObjectName("layoutWidget")

        # Create a layout for the days of the week checkboxes
        self.days_checkboxes_layout = QtWidgets.QHBoxLayout(self.days_checkboxes_container)
        self.days_checkboxes_layout.setContentsMargins(200, 0, 200, 0)
        self.days_checkboxes_layout.setSpacing(0)
        self.days_checkboxes_layout.setObjectName("days_checkboxes_layout")

        # Create the main container widget
        self.main_container = QtWidgets.QWidget(self)
        self.main_container.setGeometry(QtCore.QRect(10, 310, 1201, 351))
        self.main_container.setObjectName("main_container")

        # Create a horizontal layout for the main container
        self.main_horizontal_layout = QtWidgets.QHBoxLayout(self.main_container)
        self.main_horizontal_layout.setContentsMargins(50, 0, 50, 0)
        self.main_horizontal_layout.setObjectName("main_horizontal_layout")



        # Create a grid layout for the main container
        self.main_grid_layout = QtWidgets.QGridLayout()
        self.main_grid_layout.setHorizontalSpacing(111)
        self.main_grid_layout.setVerticalSpacing(0)
        self.main_grid_layout.setObjectName("main_grid_layout")

        # Create a ListWidget for folder selection
        self.folder_selector_list = QtWidgets.QListWidget(self.main_container)
        self.folder_selector_list.setObjectName("folder_selector_list")
        self.main_grid_layout.addWidget(self.folder_selector_list, 0, 0, 1, 1)

        # Create a TreeWidget for file overview
        self.file_overview_tree = QtWidgets.QTreeWidget(self.main_container)
        self.file_overview_tree.setObjectName("file_overview_tree")
        self.file_overview_tree.setHeaderHidden(True)
        self.main_grid_layout.addWidget(self.file_overview_tree, 0, 1, 1, 1)
        #get_inlcuded_tree(self.file_overview_tree)

        # Create a ListWidget for excluded items
        self.excluded_items_tree = QtWidgets.QTreeWidget(self.main_container)
        self.excluded_items_tree.setObjectName("excluded_items_tree")
        self.excluded_items_tree.setHeaderHidden(True)
        self.main_grid_layout.addWidget(self.excluded_items_tree, 0, 2, 1, 1)
        #get_excluded_tree(self.excluded_items_tree)

        # Create a checkbox for "Remove Duplicates"
        self.remove_duplicates_checkbox = QtWidgets.QCheckBox(self)
        self.remove_duplicates_checkbox.setGeometry(QtCore.QRect(540, 680, 141, 20))
        self.remove_duplicates_checkbox.setChecked(False)
        self.remove_duplicates_checkbox.setObjectName("remove_duplicates_checkbox")
        self.remove_duplicates_checkbox.setText("Remove Duplicates")


        # Create a horizontal layout for folder selection buttons
        self.folder_selector_button_layout = QtWidgets.QHBoxLayout()
        self.folder_selector_button_layout.setContentsMargins(0, 10, -1, -1)
        self.folder_selector_button_layout.setSpacing(30)
        self.folder_selector_button_layout.setObjectName("folder_selector_button_layout")

        # Create the "Add Folder" button
        self.add_folder_button = QtWidgets.QPushButton(self.main_container)
        self.add_folder_button.setObjectName("add_folder_button")
        self.add_folder_button.setText("Add Folder")
        self.folder_selector_button_layout.addWidget(self.add_folder_button)

        # Create the "Delete Folder" button
        self.delete_folder_button = QtWidgets.QPushButton(self.main_container)
        self.delete_folder_button.setObjectName("delete_folder_button")
        self.delete_folder_button.setText("Delete Folder")
        self.folder_selector_button_layout.addWidget(self.delete_folder_button)

        # Add the folder selection button layout to the main grid layout
        self.main_grid_layout.addLayout(self.folder_selector_button_layout, 1, 0, 1, 1)

        # Create a horizontal layout for excluded items buttons
        self.excluded_items_button_layout = QtWidgets.QHBoxLayout()
        self.excluded_items_button_layout.setContentsMargins(0, 10, -1, -1)
        self.excluded_items_button_layout.setSpacing(30)
        self.excluded_items_button_layout.setObjectName("excluded_items_button_layout")

        # Create the "Include Item" button
        self.include_item_button = QtWidgets.QPushButton(self.main_container)
        self.include_item_button.setObjectName("include_item_button")
        self.include_item_button.setText("Delete Selected")

        self.include_item_button.setToolTip("Click to INCLUDE selected items above")

        self.excluded_items_button_layout.addWidget(self.include_item_button)

        # Add the excluded items button layout to the main grid layout
        self.main_grid_layout.addLayout(self.excluded_items_button_layout, 1, 2, 1, 1)

        # Create a horizontal layout for file overview buttons
        self.file_overview_button_layout = QtWidgets.QHBoxLayout()
        self.file_overview_button_layout.setContentsMargins(0, 10, -1, -1)
        self.file_overview_button_layout.setSpacing(30)
        self.file_overview_button_layout.setObjectName("file_overview_button_layout")

        # Create the "Browse" button
        self.browse_button = QtWidgets.QPushButton(self.main_container)
        self.browse_button.setObjectName("browse_button")
        self.browse_button.setText("Browse")

        self.browse_button.setToolTip("Click to browse specific file types or categories, that you want to EXCLUDE")

        self.file_overview_button_layout.addWidget(self.browse_button)

        # Create the "Exclude Item" button
        self.exclude_item_button = QtWidgets.QPushButton(self.main_container)
        self.exclude_item_button.setObjectName("exclude_item_button")
        self.exclude_item_button.setText("Exclude Selected")

        self.exclude_item_button.setToolTip("Click to EXCLUDE selected items above")

        self.file_overview_button_layout.addWidget(self.exclude_item_button)

        # Add the file overview button layout to the main grid layout
        self.main_grid_layout.addLayout(self.file_overview_button_layout, 1, 1, 1, 1)

        # Add the main grid layout to the main horizontal layout
        self.main_horizontal_layout.addLayout(self.main_grid_layout)

        # Create a horizontal line
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(60, 200, 1101, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Create another horizontal line
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(60, 710, 1091, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # Create labels for sections
        self.file_overview_label = QtWidgets.QLabel(self)
        self.file_overview_label.setGeometry(QtCore.QRect(480, 250, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.file_overview_label.setFont(font)
        self.file_overview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_overview_label.setObjectName("file_overview_label")
        self.file_overview_label.setText("Current Files")

        self.folder_selector_label = QtWidgets.QLabel(self)
        self.folder_selector_label.setGeometry(QtCore.QRect(60, 250, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.folder_selector_label.setFont(font)
        self.folder_selector_label.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_selector_label.setObjectName("folder_selector_label")
        self.folder_selector_label.setText("Folder Selector")

        self.excluded_items_label = QtWidgets.QLabel(self)
        self.excluded_items_label.setGeometry(QtCore.QRect(870, 250, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.excluded_items_label.setFont(font)
        self.excluded_items_label.setAlignment(QtCore.Qt.AlignCenter)
        self.excluded_items_label.setObjectName("excluded_items_label")
        self.excluded_items_label.setText("Excluded Files")

        # Create a container for the days of the week labels
        self.days_label_container = QtWidgets.QWidget(self)
        self.days_label_container.setGeometry(QtCore.QRect(10, 30, 1201, 91))
        self.days_label_container.setObjectName("days_label_container")

        # Create a label for the days of the week
        self.days_label = QtWidgets.QLabel(self.days_label_container)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.days_label.setFont(font)
        self.days_label.setAlignment(QtCore.Qt.AlignCenter)
        self.days_label.setObjectName("days_label")
        self.days_label.setText("Days Of The Week")

        # Create a layout for the days of the week label
        self.days_label_layout = QtWidgets.QHBoxLayout(self.days_label_container)
        self.days_label_layout.setContentsMargins(0, 0, 0, 0)
        self.days_label_layout.setObjectName("days_label_layout")
        self.days_label_layout.addWidget(self.days_label)

        # Create a container for the "Automate" button
        self.automate_button_container = QtWidgets.QWidget(self)
        self.automate_button_container.setGeometry(QtCore.QRect(10, 750, 1201, 31))
        self.automate_button_container.setObjectName("automate_button_container")

        # Create the "Automate" button
        self.automate_button = QtWidgets.QPushButton(self)
        self.automate_button.setGeometry(QtCore.QRect(10, 750, 1201, 31))
        self.automate_button.setObjectName("automate_button")

        # Create a layout for the "Automate" button
        self.automate_button_layout = QtWidgets.QHBoxLayout(self.automate_button_container)
        self.automate_button_layout.setContentsMargins(452, 0, 452, 0)
        self.automate_button_layout.setSpacing(0)
        self.automate_button_layout.setObjectName("automate_button_layout")
        self.automate_button_layout.addWidget(self.automate_button)

        # Create a container for the "Automation Status" label
        self.automate_label_container = QtWidgets.QWidget(self)
        self.automate_label_container.setGeometry(QtCore.QRect(10, 785, 1201, 31))
        self.automate_label_container.setObjectName("automate_label_container")

        self.automate_label = QtWidgets.QLabel(self)
        self.automate_label.setGeometry(QtCore.QRect(10, 785, 1201, 31))
        self.automate_label.setObjectName("automate_label")
        self.automate_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create a layout for the "Automation Status" label
        self.automate_label_layout = QtWidgets.QHBoxLayout(self.automate_label_container)
        self.automate_label_layout.setContentsMargins(452, 0, 452, 0)
        self.automate_label_layout.setSpacing(0)
        self.automate_label_layout.setObjectName("automate_label_layout")
        self.automate_label_layout.addWidget(self.automate_label)




    # button and event connection
    def connect_signals(self):
        self.delete_folder_button.clicked.connect(
            lambda: self.controller.delete_selected_folder_and_contents(self.folder_selector_list, self.file_overview_tree,self.excluded_items_tree))

        self.add_folder_button.clicked.connect(
            lambda: self.controller.select_and_display_folder_contents(self.folder_selector_list, self.file_overview_tree, self.excluded_items_tree))

        self.include_item_button.clicked.connect(
            lambda: self.controller.include_files(self.file_overview_tree, self.excluded_items_tree))

        self.exclude_item_button.clicked.connect(
            lambda: self.controller.exclude_files(self.file_overview_tree, self.excluded_items_tree))

        self.automate_button.clicked.connect(
            lambda: self.toggle_automation())

        self.browse_button.clicked.connect(
            lambda: self.controller.open_browse_view())

        self.file_overview_tree.itemSelectionChanged.connect(self.on_tree_item_selected)
        self.excluded_items_tree.itemSelectionChanged.connect(self.on_tree_item_selected)


    # on item click event
    def on_tree_item_selected(self):

        if self.file_overview_tree.hasFocus():
            selected_items = self.file_overview_tree.selectedItems()
        else:
            selected_items = self.excluded_items_tree.selectedItems()

        if selected_items:
            selected_item = selected_items[0]

            selected_item_text = selected_item.text(0)

            self.select_children(selected_item)
            self.select_parents(selected_item)

    # on item click event helpers
    def select_children(self, selected_item):

        # Select all children recursively
        for child_index in range(selected_item.childCount()):
            child = selected_item.child(child_index)
            child.setSelected(True)
            child_text = child.text(0)
            self.select_children(child)

    def select_parents(self, selected_item):
        # Select all parents recursively
        if selected_item.parent():
            # Select all parents recursively
            parent = selected_item.parent()

            while parent:
                parent_text = parent.text(0)
                parent.setSelected(True)
                parent = parent.parent()

    def update_selected_days(self, state):
        checkbox = self.sender()  # Get the checkbox that emitted the signal
        day = checkbox.objectName()

        if state == QtCore.Qt.Checked:
            # Checkbox is checked, add the day to the selected_days list
            if day not in self.selected_days:
                self.selected_days.append(day)
        else:
            # Checkbox is unchecked, remove the day from the selected_days list if it's present
            self.selected_days = [d for d in self.selected_days if d != day]

        if not self.selected_days:
            self.is_toggled = True
            self.toggle_automation()

        print("Selected Days:", self.selected_days)

    # puts the automation label and button in a false or true state
    def toggle_automation(self):

        if self.is_toggled == False:
            if not self.selected_days:
                QMessageBox.warning(self, "No Days Selected","Please select at least one day before turning on automation.")
                return

            self.automate_button.setText("ON")
            self.automate_label.setText("Automation is turned ON")
            self.automate_label.setStyleSheet("color: green;")
            self.is_toggled = True
        else:
            self.automate_button.setText("OFF")
            self.automate_label.setText("Automation is turned OFF")
            self.automate_label.setStyleSheet("color: red;")
            self.is_toggled = False

    # checks if the automation is on
    def check_automation_toggle(self):
        if self.is_toggled == True:
            print("automation button toggled")
            self.controller.check_current_day(self.file_overview_tree, self.remove_duplicates_checkbox, self.excluded_items_tree)


    def create_day_checkboxes(self):
        self.day_checkboxes_dict = {}
        loaded_days = self.controller.load_selected_days()  # Load the saved states
        for day in DAYS:
            checkbox = QtWidgets.QCheckBox(day, self.days_checkboxes_container)
            checkbox.setObjectName(day)
            checkbox.setText(day)
            checkbox.stateChanged.connect(self.update_selected_days)
            self.days_checkboxes_layout.addWidget(checkbox)
            self.day_checkboxes_dict[day] = checkbox

            # Set the initial state of the checkbox from the loaded data
            if day in loaded_days:
                checkbox.setChecked(loaded_days[day])

    def set_automation_label_properties(self):

        # Create the "Automation Status" label
        self.label_text = "Automation is turned ON" if self.is_toggled else "Automation is turned OFF"
        self.automate_label.setText(self.label_text)
        self.automate_label.setStyleSheet("color: green;" if self.is_toggled else "color: red;")

    def set_automation_button_properties(self):
        self.automate_button.setCheckable(not self.is_toggled)
        self.automate_button.setText("Automate" if self.is_toggled else "OFF")

    def closeEvent(self, event):
        # This method is called when the window is closed
        self.controller.save_selected_folders()
        self.controller.save_selected_days(self.day_checkboxes_dict)
        self.controller.save_toggle_state(self.is_toggled)
        self.controller.save_excluded_files()

        # Save the state of the "Remove Duplicates" checkbox
        remove_duplicates_state = self.remove_duplicates_checkbox.isChecked()
        self.controller.save_remove_duplicates_state(remove_duplicates_state)

        event.accept()

