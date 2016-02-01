
from PyQt4 import QtCore, QtGui
from PyQt4 import QtWebKit
import sys
import lterGUI


class MainView(QtGui.QMainWindow, lterGUI.Ui_MainWindow):

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
