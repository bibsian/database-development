# Node class modeified from:
# http://www.yasinuludag.com/blog/?p=98
from PyQt4 import QtGui, QtCore, uic


#=========================#
# Creating custom class build the tree structure
# of the database that will be used as a visualization tool
#=========================#
class Node(object):
    ''' This class creates the Node object or tree hierarchy that is  
    visually represented with the TreeGraphModel class. Note, to
    use this class you must hard code parent and child nodes on a
    'boilerplate' script.

    To Do: Try and change this code so that a tree hierarchy can be
    created from the metaData object that you can derive with 
    SQLAlchemy, or least called from a separate class rather
    than having the hard code in the script to run the program.
    '''
    # Constructor portion
    def __init__(self, name, parent=None):
        self.name= name
        self.children = []
        self.parent = parent

        # Conditional statement to Add child Node's
        # when the parent is anything other than
        # none
        if parent is not None:
            parent.addChild(self)

    # Method to add the child name
    # to a list if there is one
    def addChild(self, child):
        self.children.append(child)

    # method to return the name of the Node
    # that you created
    def name(self):
        return self.name

    # Pass row number to acces child
    # from list
    def child(self, row):
        return self.children[row]

    # ChildCount returns the lenght
    # of the childrens list
    def childCount(self):
        return len(self.children)

    # Return the parent node
    def parent(self):
        return self.parent

        # To get the index of the node, relative
    # to the parent.
    # If self has a parent then
    # we return the index that the node corresponds to
    def row(self):
        if self.parent is not None:
            return self.parent._children.index(self)

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
        output += "|----" +  self.name + "\n"

        # This is the recursive part. It calls child
        # log for every child listed via the nodes
        for child in self.children:
            output += child.log(tabLevel)
        tabLevel -= 1
        output += "\n"

        return output

    # This is a special method that when called, calls the log
    # method and evaluates it to print out sturucture
    def __repr__(self):
        return self.log()
