# main.py

import sys
from PyQt5.QtWidgets import QApplication

from view.MenuView import MenuView

def main():
    app = QApplication(sys.argv)

    menu_view = MenuView()
    menu_view.show()


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
