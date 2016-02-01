# Implementing a Qt.AbstractTableModel using
# TreeGraphModel modeified from:
# http://www.yasinuludag.com/blog/?p=98
from PyQt4 import QtGui, QtCore, uic


#=================================#
# Creating a custom class to actually visualize the tree
# structure created by our 'Node' class
#=================================#
class TreeGraphModel (QtCore.QAbstractItemModel):
    '''
    This class is used to visualize a hierarchy tree structre (i.e.
    the TreeGraph) that is constructed with the node class

    TO DO: Determine how to place icons next to each node
    index and place little pictures of tables, foreign keys,
    and primary keys... maybe add some color.

    '''
    # Input Constructor
    def __init__(self, root, parent=None):
        super(TreeGraphModel, self).__init__(parent)
        self._rootNode = root

    #  Needs to return the amount of children
    # an item has
    def rowCount(self, parent):
        # If the node is the root node it will return
        # that self root node, else it will return
        # the number of children
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    # Return 1 for all column calls
    def columnCount(self, parent):
        return 1

    # Telling the data portion to not be implemented
    # for this widget
    def data (self, index, role):
        if not index.isValid():
            return None
        
        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            return node.name()

    # Telling the the header informatoin to not
    # be implemented for this widget so we can select
    # items
    def headerData(self, section, orientation, role):
        return "Database Structure"

    # Needs to return that the items are enabled and that the
    # items are selectable
    def flags(self, index):
       return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # Tree models need parent methodds defined:
    def parent(self, index):
        # Indexes the node using an internalPointer
        node = index.internalPointer()
        # Returns the parent node rom our Node class
        parentNode = node.parent()

        # Check to see if the parent is the root node
        # which it will be for the first call and if
        # it is return the index
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()

        # If is not the rootNode then create an index
        # using the parent node information??
        return self.createIndex(parentNode.row(), 0, parentNode)

    # Index method is responsible for returning a child at the
    # given row and column of the given parent
    def index(self, row, column, parent):

        # Check if parent is parent
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()


        # Get the child 
        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()


