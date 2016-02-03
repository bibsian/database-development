# Going to run our test window script

from PyQt4 import QtCore, QtGui
from PyQt4 import QtWebKit
import sys
import view1_test as v


from PyQt4 import QtGui, QtCore, uic
import numpy as np
import pandas as pd

# The code below loads a local path to find the
# custom modules
import sys
# sys.path.insert(0,'C:\\Users\\MillerLab\\Dropbox\\\
# database-development\\classestested\\')
sys.path.insert(0, '/Users/bibsian/Dropbox/\
database-development/classestested/')

from PandasTableModel import PandasTableModel
from TreeGraphModel import TreeGraphModel


# winmeta = 'C:\\Users\\MillerLab\\Dropbox\\database-development\\\
# data\\meta_file_test.csv'

macmeta = '/Users/bibsian/Dropbox/database-development/\
data/meta_file_test.csv'
metadf = pd.read_csv(macmeta, encoding='iso-8859-1')


# winraw = 'C:\\Users\\MillerLab\\Dropbox\\database-development\\\
# data\\raw_table_test.csv'

macraw = '/Users/bibsian/Dropbox/database-development/\
data/raw_table_test.csv'
rawdf = pd.read_csv(macraw)


class MainView(QtGui.QMainWindow, v.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)

        #============================#
        # Raw table and metadata  Display
        #============================#
        rawModel = PandasTableModel(metadf)
        self.tblViewTop.setModel(rawModel)

        metaModel = PandasTableModel(rawdf)
        self.tblViewBot.setModel(metaModel)


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainView()  # Create instance of our Main User Interface
    window.show()  # Make that instance visible
    window.tblViewTop.show()
    window.tblViewBot.show()
    sys.exit(app.exec_())  # monitor application for events

if __name__ == "__main__":
    main()
