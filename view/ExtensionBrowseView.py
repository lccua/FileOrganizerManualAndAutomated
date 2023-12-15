# third party imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel


from controller.ExtensionBrowseController import ExtensionBrowseController


class ExtensionBrowseView(QWidget):
    def __init__(self):
        super().__init__()


        self.create_layout()

        self.controller = ExtensionBrowseController()

        self.controller.refresh_list_widget(self.listView)
        self.controller.fill_tree_with_data(self.treeView)



        self.connect_signals()

    def create_layout(self):
        # Set the window title
        self.setWindowTitle('Browse Window')
        # Set the fixed size of the window
        self.setFixedSize(532, 495)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.treeViewLabel = QLabel("Folders", self)
        self.treeViewLabel.setGeometry(QtCore.QRect(110, 120, 91, 31))
        self.treeViewLabel.setFont(font)

        self.listViewLabel = QLabel("Items", self)
        self.listViewLabel.setGeometry(QtCore.QRect(350, 120, 71, 31))
        self.listViewLabel.setFont(font)


        self.listView = QtWidgets.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(50, 170, 201, 261))
        self.listView.setObjectName("listView")


        self.treeView = QtWidgets.QTreeWidget(self)
        self.treeView.setGeometry(QtCore.QRect(280, 170, 201, 261))
        self.treeView.setObjectName("treeView")
        self.treeView.setHeaderHidden(True)

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(55, 35, 420, 60))
        self.label_2.setObjectName("label_2")
        self.label_2.setWordWrap(True)  # Enable word wrap
        self.label_2.setText("Choose a folder from the Folders column. Select the item(s) you wish to exclude "
                             "in from the Items column, and then click the 'exclude item(s)' button to exclude "
                             "those selected items from the chosen folder.")

        self.label_2.setAlignment(QtCore.Qt.AlignCenter)  # Center-align the text

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(280, 440, 201, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Exclude Item")

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 440, 201, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Select All")


    def connect_signals(self):

        self.pushButton.clicked.connect(lambda: self.controller.add_files_types_to_excluded_files(self.listView, self.treeView))
        self.pushButton_2.clicked.connect(lambda: self.controller.toggle_select_all_items(self.listView))
        self.treeView.itemSelectionChanged.connect(self.on_tree_item_selected)

    def on_tree_item_selected(self):
        # Get the currently selected item
        selected_item = self.treeView.currentItem()

        if selected_item:
            selected_item_text = selected_item.text(0)

            # Select children and parents of the clicked item
            self.select_parents(selected_item)
            self.select_children(selected_item)

    def select_children(self, selected_item):
        # Select all children recursively
        for child_index in range(selected_item.childCount()):
            child = selected_item.child(child_index)

            # Check if the child is not already selected
            if not child.isSelected():
                child.setSelected(True)




    def select_parents(self, selected_item):
        # Check if the selected item has a parent
        if selected_item.parent():
            # Select all parents recursively
            parent = selected_item.parent()

            while parent:
                parent_text = parent.text(0)
                parent.setSelected(True)
                parent = parent.parent()
