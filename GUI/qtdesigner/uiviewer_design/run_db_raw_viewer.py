# This script is to test the first portion of the LTER
# User interface.

# Testing Working Tab with database tree and raw csv file
# viewer

from PyQt4 import QtCore, QtGui
from PyQt4 import QtWebKit
import sys
import UiTest1


class MainView(QtGui.QMainWindow, UiTest1.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainView()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

