# This script is to test the first portion of the LTER
# User interface; base code for the window was
# created using QtDesigner, see file 'db_raw_viewr.ui'

# Testing Working Tab with database tree and raw csv file
# viewer

from PyQt4 import QtCore, QtGui
from PyQt4 import QtWebKit
import sys
import db_raw_viewer


from PyQt4 import QtGui, QtCore, uic
import numpy as np
import pandas as pd

# The code below loads a local path to find the
# custom modules
import sys
sys.path.insert(0,'C:\\Users\\MillerLab\\Dropbox\\\
database-development\\classestested\\')
from PandasTableModel import PandasTableModel
from TreeGraphModel import TreeGraphModel

sys.path.insert(0,'C:\\Users\\MillerLab\\Dropbox\\\
database-development\\development\\functionsdev\\')
import db_tree as db



winmeta = 'C:\\Users\\MillerLab\\Dropbox\\database-development\\\
data\\meta_file_test.csv'
metadf = pd.read_csv(winmeta, encoding = 'iso-8859-1')


class MainView(QtGui.QMainWindow, db_raw_viewer.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)
        self.show()


        #========================#
        # Tree Graph Data and Model
        #========================#
       
        treeModel = TreeGraphModel(
            db.DatabaseTree("Root", parent=None).full_tree())
        self.treeDB.setModel(treeModel)

        
        #============================#
        # Raw table model data and Display
        #============================#
        rawModel = PandasTableModel(metadf)
        self.tblRaw.setModel(rawModel)



def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainView()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

