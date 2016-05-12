#!usr/bin/env python
# 'http://stackoverflow.com/questions/31588584/
# pyqt-qtableview-prohibitibily-slow-when-scrolling-with-large-data-sets
# /31591015#31591015'
# TreeGraphModel modeified from:
# http://www.yasinuludag.com/blog/?p=98
from PyQt4 import QtGui, QtCore, uic
import numpy as np
import pandas as pd


class PandasTableModel(QtCore.QAbstractTableModel):
    '''
    This class is an abstract table class from Qt to visualize
    data in a table format and using the pandas dataframe
    as object that supply the data to be visualized.
    To Do: Nothing
    Last edit: Removed the ability to edit the table
    ''' 
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__data = np.array(data.values)
        self.__cols = data.columns
        self.r, self.c = np.shape(self.__data)

    def rowCount(self, parent=None):
        return self.r

    def columnCount(self, parent=None):
        return self.c

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__cols[section]
            elif orientation == QtCore.Qt.Vertical:
                return section

    def data(self, index, role):
        if index.isValid():
            # This is the role to display every item
            # That you created...I think
            if role == QtCore.Qt.DisplayRole:
                return self.__data[index.row(), index.column()]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class PandasTableModelEdit(QtCore.QAbstractTableModel):
    '''
    This class is an abstract table class from Qt to visualize
    data in a table format and using the pandas dataframe
    as object that supply the data to be visualized.
    To Do: Nothing
    Last edit: Removed the ability to edit the table
    ''' 
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__data = np.array(data.values)
        self.__cols = data.columns
        self.r, self.c = np.shape(self.__data)

    def rowCount(self, parent=None):
        return self.r

    def columnCount(self, parent=None):
        return self.c

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__cols[section]
            elif orientation == QtCore.Qt.Vertical:
                return section

    def data(self, index, role):
        if role == QtCore.Qt.UserRole:
            index = None
            return self.__data
        else:
            pass
    
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return self.__data[index.row(), index.column()]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |\
            QtCore.Qt.ItemIsEditable

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            self.__data[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def event(self, event):
        if (event.key() == QtCore.Qt.Key_Return):
            print('Presed Enter')
            raise KeyError

        return QtCore.QAbStractTableModel.event(self, event)
    

