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
import numpy as np
import pandas as pd

# The code below loads a local path to find the
# custom modules
import sys
sys.path.insert(0,'C:\\Users\\MillerLab\\Dropbox\\\
database-development\\classestested\\')

from  Node import Node
from PandasTableModel import PandasTableModel
from TreeGraphModel import TreeGraphModel

#===========================#
# Reading in data fro testing
#===========================#

winmeta = 'C:\\Users\\MillerLab\\Dropbox\\database-development\\\
data\\meta_file_test.csv'
metadf = pd.read_csv(winmeta, encoding = 'iso-8859-1')


winraw = 'C:\\Users\MillerLab\\Dropbox\\database-development\\\
data\\raw_table_test.csv'
rawdf = pd.read_csv(winraw)


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
    
    metaView = QtGui.QTableView()
    metaView.show()

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
    model = PandasTableModel(metadf)
    model2= PandasTableModel(rawdf)
    model3 = TreeGraphModel(Root)
    #========================#
    # Set model classes
    #========================#
    metaView.setModel(model)
    rawView.setModel(model2)
    treeView.setModel(model3)

    sys.exit(app.exec_())
