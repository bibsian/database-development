#! /usr/bin/env python
from poplerGUI import ui_logic_mainwindow as uv
from PyQt4 import QtGui
import sys


def main():
    app = QtGui.QApplication(sys.argv)
    ex = uv.UiMainWindow()
    ex.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
