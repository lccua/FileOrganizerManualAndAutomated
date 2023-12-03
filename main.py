# main.py

import sys
from PyQt5.QtWidgets import QApplication
from controller.MenuController import MenuController

def main():
    app = QApplication(sys.argv)

    menu_controller = MenuController()  # Store the instance in a variable

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
