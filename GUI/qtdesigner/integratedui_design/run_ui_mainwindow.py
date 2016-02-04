# This script is going to be used to run the user interface
# generated with pyqt

import sys

import pandas as pd
import numpy as np
from PyQt4 import QtCore, QtGui


import ui_mainwindow as mw
sys.path.insert(0,'C:\\Users\\MillerLab\\Dropbox\\\
database-development\\classestested\\')
import PandasTableModel as ptb

winmeta = 'C:\\Users\\MillerLab\\Dropbox\\database-development\\\
data\\meta_file_test.csv'

winraw = 'C:\\Users\MillerLab\\Dropbox\\database-development\\\
data\\raw_table_test.csv'

# Creating a Dialog box that will display the unqiue site
# abbreviatiuons from the raw data file that is loaded into
# the user interface
class UniqueSiteList(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tblList = QtGui.QTableView()
        layout = QtGui.QGridLayout()
        layout.addWidget(self.tblList,0,1)
        self.setLayout(layout)

# Creating the subclass that inherits from the Ui_MainWindow
# object i.e. our user interface
# and the user interface module we created (ui_mainwindow)
class UiMainWindow (QtGui.QMainWindow, mw.Ui_MainWindow):
    '''
    This class displays the user interface that was created with
    QtDesigner. We're multiply inheriting the user interface
    and the QMainWindow to integrate them into a class that
    we can enable signal and designate slots.

    To do: Need a file handler for the raw data files because it will
    be different every time we run it
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setupUi(self)
        self.w = None

        # Pointing a button and a line edit to the
        # same handler... is this possible?
        self.btnViewSite.clicked.connect(self.handler)
        self.lnedViewSite.returnPressed.connect(self.handler)

        # Class attributes??
        self._metadf = pd.read_csv(winmeta, encoding = 'iso-8859-1')
        self._rawdf= pd.read_csv(winraw)
    
        # Setting the metadata model data to mirrow what is in our
        # file titled meta_file_test.csv
        metamodel = ptb.PandasTableModel(self._metadf)
        self.tblViewmeta.setModel(metamodel)

        #Setting the raw data model to mirror what is in our file
        # titled raw_tbl_test.csv
        rawmodel = ptb.PandasTableModel(self._rawdf)
        self.tblViewraw.setModel(rawmodel)


    def handler(self):
        self.w = UniqueSiteList()
        self.w.show()
        
# Defining the main function which
# shows the user interface.
def main():
    app= QtGui.QApplication(sys.argv)
    ex = UiMainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
