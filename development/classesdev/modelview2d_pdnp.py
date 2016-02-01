# Implementing a Qt.AbstractTableModel using
# Numpy and Pandas.
# Code from:
# 'http://stackoverflow.com/questions/31588584/
# pyqt-qtableview-prohibitibily-slow-when-scrolling-with-large-data-sets
# /31591015#31591015'
#
# Will likely modify some what but this will really get things going

# TO DO:
# Let's remove the ability to edit the displayed data


from PyQt4 import QtGui, QtCore, uic
import sys
import numpy as np
import pandas as pd

#===========================#
# Reading in data fro testing
#===========================#

winlter = 'C:\\Users\MillerLab\\Box Sync\\LTER\\Database\\\
GUIdevelopment\\QtDesigner\\lter_table_test.csv'
lterdf = pd.read_csv(winlter)


winraw = 'C:\\Users\MillerLab\\Box Sync\\LTER\\Database\\\
GUIdevelopment\\QtDesigner\\raw_table_test.csv'
rawdf = pd.read_csv(winraw)

#=========================#
# Creating custom class to display tree structure of database
#=========================#
class Node(object):
    def __init__(self, name, parent=None):
        self._name= name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tabLevel= -1):
        output = ""
        tabLevel += 1
        for i in range(tabLevel):
            output += "\t"

        output += "/----" +  self._name + "\n"
            
        for child in self._children:
            output += child.log(tabLevel)
        tabLevel -= 1
        output += "\n"

        return output

#=================================#
# Defining a custom class for PyQt4
#=================================#
class PandasTableModel(QtCore.QAbstractTableModel):

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
        return QtCore.Qt.ItemIsEditable| QtCore.Qt.ItemIsEnabled|\
            QtCore.Qt.ItemIsSelectable

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



#=========================================#
# Section to execute program from command line
#=========================================#
if __name__ == '__main__':

    #==========================#
    # Initiate application
    #===========================#
    app= QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")

    #===========================#
    # Create lter Table View Widget
    #============================#
    
    lterView = QtGui.QTableView()
    lterView.show()

    #============================#
    # Create raw data Table View Widget
    #============================#
    
    rawView = QtGui.QTableView()
    rawView.show()

    #============================# 
    # Creating nodes for tree sturcutre
    #===========================#
    lterNode = Node("lterID")
    siteIDNode= Node("siteID", lterNode)
    localNode= Node("localclimate", siteIDNode)
    mainNode = Node ("main_data", localNode)
    taxaNode = Node ("taxaID", mainNode)
    sampleID = Node ("rawobs", mainNode)

    print(lterNode)
    
    #===========================#
    # Implementing the model view design
    #============================#
    model = PandasTableModel(lterdf)
    model2= PandasTableModel(rawdf)

    #========================#
    # Set model classes
    #========================#
    lterView.setModel(model)
    rawView.setModel(model2)

    sys.exit(app.exec_())
