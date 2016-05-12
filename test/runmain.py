#!usr/bin/env python
import userview as uv
from PyQt4 import QtGui
import sys
import class_userfacade as face

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = uv.UiMainWindow()
    ex.show()

    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
