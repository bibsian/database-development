# This script goint to be used to understand how to use
# model view programming with pyqt
# This is a software design style that  lets us decouple the UI from
# the data it displays... which is what I need to figure out
# to get our program running
# http://www.yasinuludag.com/blog/?p=98 is where I started
# The model acts as the middle man between the UI and the data
# itself.
# Step 1: Display widgets that share a list view model

# Creating our own model class to represent our data
# Three choice: List, Table or Tree model
# Step 2;: Creating our list view model. Every model has to
# imlement two methods in a model (***2 Methods***)- DATA & ROW COUNT


# This is also going to implement inserting and removing

from PyQt4 import QtGui, QtCore, uic
import sys


# To make this class allow editable methodsd we need to
# set 'flags' and 'setdata'
#=================================#
# Defining a custom class for PyQt4
#=================================#
class LTERListModel(QtCore.QAbstractListModel):
    def __init__(self, names = [], parent = None):
        QtCore.QAbstractListModel.__init__(self,parent)
        self.__names = names

     # Row count method tells view how many items the data
     # Contains
    def rowCount(self, parent):
        return len(self.__names)

    # Section shows index on row
    # Orientation 
    def headerData (self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str("LTER")

        
    
    # This is the data method
    # Responsible for giving the right data for the index
    # parameter given.
    # The parameters of this method are
    # 1) the Qindex class 'index'- this stores information
    # about the wanted item for the view.
    # can use index.row, index.column, index.parent (who is the
    # parent item so we can traverse it)
    def data(self, index, role):

        # This is the role to display every item
        # That you created...I think
        if role == QtCore.Qt.DisplayRole:
           row = index.row()
           value = self.__names[row]

           return value


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

    def setData(self, index, value, role = QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            row= index.row()
            self.__names[row]= value
            self.dataChanged.emit(index,index)
            return True
        return False

    #=============================================#
    # Inserting and removing items
    #=============================================#
    # Postion: Where in the data we want to insert new data
    # rows: how many rows we want to insert
    # Parent.... for some reason we never care about parent
    # parameter unless we need to implement hierarchical structre
    # 
    #
    def insertRows(self, position, rows, parent= QtCore.QModelIndex()):
        # These methods of inserting and deleting emit a signal
        # that is connected by the views so that views
        # handle the data they display correctly and synchronously
        # among the different views.

        # We need to set parameters for this method to tell
        # the beginInsertRows where to do the insert.. NOTE
        # This argument take 3 parameters:index, first, last
        # first and last are indeces of where the view should
        # occurupdate. All the items between first and last
        # are where the insert occurs.
        # index= QtCore.ModelIndex defaults to the root
        # position parameter is where the first insert is to
        # occur.... first = position

        self.beginInsertRows(parent, position,
                             position + rows-1)

        for i in range(rows):
            self.__names.insert(position, " ")
        
        self.endInsertRows()

        return True

    #===========================#
    # Removeing
    #===========================#

    def removeRows(self, position, rows, parent= QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position,
                             position + rows-1)

        for i in range(rows):
            value = self.__names[position]
            self.__names.remove(value)
        self.endRemoveRows()

        return True



#=========================================#
# Section to execute program from command line
#=========================================#
if __name__ == '__main__':

    app= QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")

    listView = QtGui.QListView()
    listView.show()

    comboBox= QtGui.QComboBox()
    comboBox.show()

    treeView = QtGui.QTreeView()
    treeView.show()

    tableView= QtGui.QTableView()
    tableView.show()

    data = list()
    data.extend(["AND", "MCM", "HELLO"])
    
    # Model Calls
    model = LTERListModel(data)

    # Set model class
    listView.setModel(model)
    treeView.setModel(model)
    comboBox.setModel(model)
    tableView.setModel(model)

    model.insertRows(1,2)
    model.removeRows(1,2)
    
    sys.exit(app.exec_())
