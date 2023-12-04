from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox


from view.AutomatedOrganizerView import AutomatedOrganizerView
from model.FileOrganizerModel import FileOrganizerModel
from constants import *


class AutomatedFileOrganizerController:
    def __init__(self):
        self.av = AutomatedOrganizerView()
        self.model = FileOrganizerModel()

        self.av.show()



        self.checkbox = None

        self.check_automation_toggle()
        self.create_day_checkboxes()
        self.set_automation_label_properties()
        self.set_automation_button_properties()

        self.connect_signals()






    def connect_signals(self):

        self.av.delete_folder_button.clicked.connect(lambda: self.model.delete_selected_folder(self.av.folder_selector_list, self.av.file_overview_tree, self.av.excluded_items_tree))
        self.av.add_folder_button.clicked.connect(lambda: self.model.open_and_select_folder(self.av.folder_selector_list, self.av.file_overview_tree, self.av.excluded_items_tree))
        self.av.include_item_button.clicked.connect(lambda: self.model.include_files(self.av.file_overview_tree, self.av.excluded_items_tree))
        self.av.exclude_item_button.clicked.connect(lambda: self.model.exclude_files(self.av.file_overview_tree, self.av.excluded_items_tree))
        self.av.browse_button.clicked.connect(lambda: self.open_browse_window)
        self.av.automate_button.clicked.connect(lambda: self.toggle_automation)

        self.av.file_overview_tree.itemSelectionChanged.connect(lambda: self.on_tree_item_selected)
        self.av.excluded_items_tree.itemSelectionChanged.connect(lambda: self.on_tree_item_selected)

        self.checkbox.stateChanged.connect(lambda: self.update_selected_days)




    def on_tree_item_selected(self):

        if self.av.file_overview_tree.hasFocus():
            selected_items = self.av.file_overview_tree.selectedItems()
        else:
            selected_items = self.av.excluded_items_tree.selectedItems()

        if selected_items:
            selected_item = selected_items[0]

            selected_item_text = selected_item.text(0)

            self.select_children(selected_item)
            self.select_parents(selected_item)

    def select_children(self, selected_item):

        # Select all children recursively
        for child_index in range(selected_item.childCount()):
            child = selected_item.child(child_index)
            child.setSelected(True)
            child_text = child.text(0)
            self.select_children(child)

    def select_parents(self, selected_item):
        # Select all parents recursively
        parent = selected_item.parent()

        while parent:
            parent_text = parent.text(0)
            parent.setSelected(True)
            parent = parent.parent()

    def open_browse_window(self):
        if not self.browse_window:
            self.browse_window = AutomatedOrganizerView()
        self.browse_window.show()

    def toggle_automation(self):

        if self.is_toggled == False:
            if not self.model.selected_days:
                QMessageBox.warning(self,"No Days Selected", "Please select at least one day before turning on automation.")
                return

            self.av.automate_button.setText("ON")
            self.av.automate_label.setText("Automation is turned ON")
            self.av.automate_label.setStyleSheet("color: green;")
            self.is_toggled = True
        else:
            self.av.automate_button.setText("OFF")
            self.av.automate_label.setText("Automation is turned OFF")
            self.av.automate_label.setStyleSheet("color: red;")
            self.is_toggled = False

    def update_selected_days(self):

        self.model.selected_days = [day for day, checkbox in self.model.day_checkboxes_dict.items() if checkbox.isChecked()]

        if not self.model.selected_days:
            self.model.is_toggled = True
            self.toggle_automation()

        print("Selected Days:", self.model.selected_days)

    def create_day_checkboxes(self):
        for day in DAYS:
            self.checkbox = QtWidgets.QCheckBox(day, self.av.days_checkboxes_container)

            self.checkbox.setObjectName(day)
            self.checkbox.setText(day)
            self.av.days_checkboxes_layout.addWidget(self.checkbox)

            # Set the initial state of the checkbox from the loaded data
            if day in self.model.day_checkboxes_dict:
                self.checkbox.setChecked(self.model.day_checkboxes_dict[day])

            # Store the checkbox in the dictionary
            self.model.day_checkboxes_dict[day] = self.checkbox

    def check_automation_toggle(self):
        if self.model.is_toggled == True:
            print("automation button works")
            self.model.check_current_day(self.model.selected_days, self.av.remove_duplicates_checkbox,self.av.file_overview_tree, self.av.excluded_items_tree)
        else:
            print("normale gang van zaken")

    def set_automation_label_properties(self):

        # Create the "Automation Status" label
        self.label_text = "Automation is turned ON" if self.model.is_toggled else "Automation is turned OFF"
        self.av.automate_label.setText(self.label_text)
        self.av.automate_label.setStyleSheet("color: green;" if self.model.is_toggled else "color: red;")

    def set_automation_button_properties(self):
        self.av.automate_button.setCheckable(not self.model.is_toggled)
        self.av.automate_button.setText("Automate" if self.model.is_toggled else "OFF")






