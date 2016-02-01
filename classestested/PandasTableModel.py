# Implementing a Qt.AbstractTableModel using
# Numpy and Pandas.
# PandasModel code modified from:
# 'http://stackoverflow.com/questions/31588584/
# pyqt-qtableview-prohibitibily-slow-when-scrolling-with-large-data-sets
# /31591015#31591015'
# TreeGraphModel modeified from:
# http://www.yasinuludag.com/blog/?p=98

from PyQt4 import QtGui, QtCore, uic
import numpy as np
import pandas as pd
#=================================#
# Defining a custom class for PyQt4
#=================================#
class PandasTableModel(QtCore.QAbstractTableModel):
    '''
    This class is an abstract table class from Qt to visualize
    data in a table format and using the pandas dataframe
    as object that supply the data to be visualized.

    To Do: Nothing

    Last edit: Removed the ability to edit the table
    '''
    #============================#
    # Constructors
    #============================#
    
    def __init__(self, data, parent = None):
        QtCore.QAbstractTableModel.__init__(self,parent)

        # This initiates the private instance variable (our data)
        # based on the values within the dataframe.
        # These values are extracted using pandas method
        # '.values' and comverted to a numpy array.
        self.__data = np.array(data.values)

        # This gives us a private instance variable with the column
        # headers from the dataframe
        self.__cols= data.columns

        self.r, self.c = np.shape(self.__data)

    #============================#
    # Row Count implementation
    #============================#

    # Defing the rowCount method by calling on the inistatiated
    # object (self) and asking for the for the unique
    # instance variables that were defined
    def rowCount(self, parent = None):
        return self.r

    #===============================#
    # Column Count implementation
    #===============================#
    
    # Defing the rowCount method by calling on the inistatiated
    # objected (self) and asking for the attribute that was
    # constructed above (columns, self.c)
    def columnCount(self, parent = None):
        return self.c

    #===============================#
    # Data header implementation
    #===============================#
    
    # The headerData method is used to label columns and rows
    # when Viewing through a table.
    # If the orientation is horizontal or veritcal, the argument
    # section corresponds to the row or column index respectively.
    def headerData (self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__cols[section]
            elif orientation == QtCore.Qt.Vertical:
                return section

    #==========================#
    # Data Display Implementation
    #==========================#
    
    # Displaying the data in the table.
    # index.row, index.column, index.parent
    def data(self, index, role):
        if index.isValid():
            # This is the role to display every item
            # That you created...I think
            if role == QtCore.Qt.DisplayRole:
                return self.__data[index.row(), index.column()]

    #============================#
    # Flags Implementations for emiting signals
    #============================#
    
    # This method is raising flags so that when an item is
    # double clicked the program will search for a flag
    # and determin what that item can do according to the
    # methods in the class... I think that means
    # we need to have classes for all of the essential functions
    # of the program. 
    def flags(self, index):
        #
        return QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsSelectable

    #=============================#
    # Editing Implimentation
    #=============================#
    def setData(self, index, value, role = QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            row= index.row()
            col= index.column()
            self.__data[index.row(), index.column()] = value
            self.dataChanged.emit(index,index)
            return True
        return False
