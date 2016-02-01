# Implementing a Qt.AbstractTableModel using
# Numpy and Pandas.
# PandasModel code modified from:
# 'http://stackoverflow.com/questions/31588584/
# pyqt-qtableview-prohibitibily-slow-when-scrolling-with-large-data-sets
# /31591015#31591015'
# TreeGraphModel modeified from:
# http://www.yasinuludag.com/blog/?p=98


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
# Creating custom class build the tree structure
# of the database that will be used as a visualization tool
#=========================#
class Node(object):
    # Constructor portion
    def __init__(self, name, parent=None):
        self._name= name
        self._children = []
        self._parent = parent

        # Conditional statement to Add child Node's
        # when the parent is anything other than
        # none
        if parent is not None:
            parent.addChild(self)

    # Method to add the child name
    # to a list if there is one
    def addChild(self, child):
        self._children.append(child)

    # method to return the name of the Node
    # that you created
    def name(self):
        return self._name

    # Pass row number to acces child
    # from list
    def child(self, row):
        return self._children[row]

    # ChildCount returns the lenght
    # of the childrens list
    def childCount(self):
        return len(self._children)

    # Return the parent node
    def parent(self):
        return self._parent

        # To get the index of the node, relative
    # to the parent.
    # If self has a parent then
    # we return the index that the node corresponds to
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    # Log function to print out the parent
    # node structure
    # This is a recursive function that
    # will print out tabs/ names
    # parent and childrens.
    def log(self, tabLevel= -1):
        output = ""
        tabLevel += 1

        # Increase tab count in output text
        for i in range(tabLevel):
            output += "\t"

        # Add the name of the current node and a line break
        output += "|----" +  self._name + "\n"

        # This is the recursive part. It calls child
        # log for every child listed via the nodes
        for child in self._children:
            output += child.log(tabLevel)
        tabLevel -= 1
        output += "\n"

        return output

    # This is a special method that when called, calls the log
    # method and evaluates it to print out sturucture
    def __repr__(self):
        return self.log()


#=================================#
# Creating a custom class to actually visualize the tree
# structure created by our 'Node' class
#=================================#
class TreeGraphModel (QtCore.QAbstractItemModel):
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
    # Create tree view and show
    #===========================#
    treeView = QtGui.QTreeView()
    treeView.show()

    #============================# 
    # Creating nodes for tree sturcutre
    #===========================#
    # Root
    Root= Node("root", parent=None)
    Database= Node("Database", parent=Root)
    LTER = Node("LTER", parent = Database)
    Tables = Node("Tables", parent = LTER)
    
    lterNode = Node("lterID", parent=Tables)
    ltername = Node("lter_name", parent=lterNode)
    currentfunding = Node("currently_funded", parent=lterNode)
    lat = Node("lat", parent=lterNode)
    long = Node("long", parent=lterNode)

    
    siteIDNode= Node("siteID", parent=Tables)
    site = Node("siteID", parent=siteIDNode)
    lterID = Node("lterID", parent=siteIDNode)
    latsite = Node("lat", parent=siteIDNode)
    longsite = Node("long", parent=siteIDNode)
    descript = Node("descript", parent=siteIDNode)


    mainNode = Node ("main_data", parent=Tables)
    projID = Node("projID", parent=mainNode)
    title = Node("title", parent=mainNode)
    samplingunits = Node("samplineunits", parent=mainNode)
    samplingproto = Node("samplingprotocol", parent=mainNode)
    structuremain = Node("structured", parent=mainNode)
    startyr = Node("startyr", parent=mainNode)
    endyr = Node("endyr", parent=mainNode)
    samplefreq = Node("samplefreq", parent=mainNode)
    totalobs = Node("totalobs", parent=mainNode)
    studytype = Node("studytype", parent=mainNode)
    comm = Node("community", parent=mainNode)
    sitemain = Node("siteID", parent=mainNode)
    sprep2 = Node("sp_rep2_ext", parent=mainNode)
    sprep3 = Node("sp_rep3_ext", parent=mainNode)
    sprep4 = Node("sp_rep4_ext", parent=mainNode)
    metalink = Node("metalind", parent=mainNode)
    knbID = Node("knbID", parent=mainNode)

    taxaNode = Node ("taxa", parent=Tables)
    taxaID = Node("taxaId", parent=taxaNode)
    taxaproj = Node("projID", parent=taxaNode)
    sppcode = Node("sppcode", parent=taxaNode)
    kingdom = Node("kingdom", parent=taxaNode)
    phylum = Node("phylum", parent=taxaNode)
    classtaxa = Node("class", parent=taxaNode)
    order = Node("order", parent=taxaNode)
    family = Node("family", parent=taxaNode)
    genus = Node("genus", parent=taxaNode)
    spp = Node("species", parent=taxaNode)
    authority = Node("authority", parent=taxaNode)

    rawNode = Node ("rawobs", parent=Tables)
    sampleID = Node("sampleID", parent=rawNode)
    rawtaxaID = Node("taxaID" , parent=rawNode)
    rawproj = Node("projID", parent=rawNode)
    year = Node("year", parent=rawNode)
    month = Node("month", parent=rawNode)
    day = Node("day", parent=rawNode)
    sptrep1 = Node("spt_rep1", parent=rawNode)
    sptrep2 = Node("spt_rep2", parent=rawNode)
    sptrep3 = Node("spt_rep3", parent=rawNode)
    sptrep4 = Node("spt_rep4", parent=rawNode)
    rawstruct = Node("structure", parent=rawNode)
    indivID = Node("indivID", parent=rawNode)
    unitobs = Node("unitobs", parent=rawNode)
    #===========================#
    # Implementing the model view designs
    #============================#
    model = PandasTableModel(lterdf)
    model2= PandasTableModel(rawdf)
    model3 = TreeGraphModel(Root)
    #========================#
    # Set model classes
    #========================#
    lterView.setModel(model)
    rawView.setModel(model2)
    treeView.setModel(model3)

    sys.exit(app.exec_())
