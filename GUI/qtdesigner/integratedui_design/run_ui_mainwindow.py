# This script is going to be used to run the user interface
# generated with pyqt

#=========================#
# Importing modules
#=========================#

# Base modules
import sys
import re
from collections import defaultdict
import decimal as dc
import numbers as nm

# Third party modules
from PyQt4 import QtCore, QtGui
import pandas as pd
import numpy as np

# User Interfaces
import ui_mainwindow as mw

# Custom Classes:
# This is an if elif statement to choose
# which scripts to read from based on the operating
# system the program is being used on. These
# imports are custom classes
from sys import platform as _platform
if _platform == "darwin":
    sys.path.insert(
        0, "/Users/bibsian/Dropbox/database-development/classestested/")
elif _platform == "win32":
    sys.path.insert(
        0, 'C:\\Users\\MillerLab\\Dropbox\\database-development\\classestested\\')

import PandasTableModel as ptb



#========================#
# Dialog pop up widget
#========================#

# Creating a Dialog box that will display the values that
# input by the user and will be used to push to the database
class DialogPopUp(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.show()
        layout = QtGui.QVBoxLayout(self)
        self.tblList = QtGui.QTableView()
        layout.addWidget(self.tblList)
        self.setLayout(layout)

#=========================#
# User interface
#=========================#

# Creating the subclass that inherits from the Ui_MainWindow
# object i.e. our user interface
# and the user interface module we created (ui_mainwindow)


class UiMainWindow (QtGui.QMainWindow, mw.Ui_MainWindow):
    '''
    This class displays the user interface that was created with
    QtDesigner. We're multiply inheriting the user interface
    and the QMainWindow to integrate them into a class that
    we can enable signal and designate slots.

    To do: Need a file handler for the raw data files because it will
    be different every time we run it.---------DONE

    To do: Need to connect the file handler form the raw data
    forms to the global dataframe object that gets repeatedly called
    ------------------ DONE

    To do: Need code a better handler for reading files; add
    The ability to read different file types i.e. txt, tab-delimited,
    xlsx, and csv
    '''

    def __init__(self, parent=None):
        super().__init__(parent)

        #=====================#
        # Creating self global data frame to access
        # metadata file... this will never change
        # so I'm hard coding the paths for mac or windows 
        #======================#
        # This is an if elif statement to choose
        # which scripts to read from based on the platform
        # the program is running on (Mac or Windows)
        if _platform == "darwin":
            self.metapath = (
                "/Users/bibsian/Dropbox/database-development/data/meta_file_test.csv")
        elif _platform == "win32":
            #=======================#
            # Paths to data and conversion of files to dataframe
            #=======================#
            self.metapath = ("C:\\Users\MillerLab\\Dropbox\\database-development"
                             + "\\data\\meta_file_test.csv")
        self.metadf = pd.read_csv(self.metapath, encoding="iso-8859-11")
        
        
        #===================#
        # Setting up a global blank widget so it will
        # persist in applicaiton when called to take the form
        # of a dialog box.
        #===================#
        # Creating a class object called w that will serve
        # to maintain a dialog box when called upon in different
        # methods
        self.w = None
        
        #======================#
        # Setting the User interface
        # from our qtdesigner code (this is inherited)
        #======================#
        self.setupUi(self)

        
        #=====================#
        # Catching menu bar actions from user interface
        #=====================#
        # Open file
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.open_file)

        # Quit Program
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.triggered.connect(self.quit_program)
        #=====================#
        # Catiching button signals from user interface
        #=====================#
        self.btnloadrawview.clicked.connect(self.open_file)


        #=======================#
        # Catching line edit signals from user interface
        #=======================#
        self.lnedViewSite.returnPressed.connect(self.col_view_handle)

        # LINE EDITS: SITE SPATIAL INFORMATION
        # SITEID, LATTITUDE, LONGITUDE, NAMES, DESCRIPTIONS
        # siteID if Yes check box is checked
        self.lnedSiteformsiteID.returnPressed.connect(
            self.site_id_check)
        # site ID if No check box is checked
        self.lnedSiteformnock.returnPressed.connect(
            self.site_id_check)
        # Lattitude
        self.lnedSiteformlat.returnPressed.connect(
            self.site_coord_check)
        # Longitude
        self.lnedSiteformlong.returnPressed.connect(
            self.site_coord_check)
        # Descriptions
        self.lnedSiteformnames.returnPressed.connect(
            self.site_name_check)

        #=======================#
        # Catching Check box signals from user interface
        #=======================#
        self.ckSiteCoordN.stateChanged.connect(self.site_coord_options)
        self.ckSiteCoordY.stateChanged.connect(self.site_coord_options)

        #======================#
        # Catching the site combo box text
        #======================#
        self.cboxSiteCount.activated.connect(self.get_sitebox)

        #======================#
        # Creating data models to view pandas dataframes on
        # in qttreeView
        #======================#
        # Setting the metadata model data to mirrow what is in our
        # file titled meta_file_test.csv
        metamodel = ptb.PandasTableModel(self.metadf)
        self.tblViewmeta.setModel(metamodel)


    def get_sitebox(self):
        self.numsite = int(self.cboxSiteCount.currentText())
        print(self.numsite)

    #========================#
    # Defining a method to return a list of unique values
    # in a column
    #========================#
    def col_view_handle(self):
        # Save text from input...might have to change this
        # to a list that we search and pull from if we are
        # going to resuse this method a lot.
        columntofind = self.lnedViewSite.text()

        # Catch error
        try:
            collisttoadd = list(self.rawdf[columntofind].unique())
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
            "You entered a string that does not match" +
            " any column name in the raw data table. Please re-enter" +
            " the column name again.")
            self.w.show()
            return

        self.w = DialogPopUp()


        # Special catch to create a list of unique site names
        # once the user has specified that column that
        # contains site abbreviations
        if self.lnedViewSite.editingFinished:
            self.sitelisttoadd = list(
                self.rawdf[columntofind].unique())
            print(self.sitelisttoadd)
        else:
            pass

        # Creating a list of unique column values based on
        # the column name the user supplied
        collisttoadd = list(self.rawdf[columntofind].unique())
        collistdf = pd.DataFrame(collisttoadd)
        collistdf.columns = [columntofind]

        # Creating the table model to view the subsetted
        # values in dataframe form with qttableview
        collistmodel = ptb.PandasTableModel(collistdf)

        # Settting the data Model to view through the
        # dialog box from UniqueColumnList
        self.w.tblList.setModel(collistmodel)       

    #=======================#
    # Deploying a method to activate/deactivate line edits on
    # the site coordinates form based on what
    # is or is not checked in the boxes
    #=======================#
    def site_coord_options(self):
        if self.ckSiteCoordN.isChecked():
            self.lnedSiteformnock.setEnabled(True)

            self.lnedSiteformsiteID.setDisabled(True)
            self.lnedSiteformlat.setDisabled(True)
            self.lnedSiteformlong.setDisabled(True)

        elif self.ckSiteCoordY.isChecked():

            self.lnedSiteformnock.setDisabled(True)
            self.lnedSiteformsiteID.setEnabled(True)
            self.lnedSiteformlat.setEnabled(True)
            self.lnedSiteformlong.setEnabled(True)


    #===========================#
    # Method ot handle the concatenation of sites
    # into a table to push to the database
    #==========================#
    def site_id_check(self):
        if self.ckSiteCoordN.isChecked():
            self.siteIDrecord = self.lnedSiteformnock.text()
        elif self.ckSiteCoordY.isChecked():
            self.siteIDrecord = self.lnedSiteformsiteID.text()

        #-------#
        # Regular expression to turn the text entered into the line
        # editor into a list with words (or abbreviations) separated
        # by commas (this will match the list constructed by
        # looking at the unique values of the site columns)
        #-------#
        self.siteIDrecord_re = re.sub(
            "[^\w]", " ", self.siteIDrecord).split()  


        #-------#
        # Check siteID entries for conformity to raw data
        #-------#
        if [x.lower() for x in self.siteIDrecord_re] == [
                y.lower() for y in self.sitelisttoadd] and len(
                    self.siteIDrecord_re) == self.numsite:
            
            print([x.lower() for x in self.siteIDrecord_re])
            print([y.lower() for y in self.sitelisttoadd])
            
            QtGui.QMessageBox.about(
                self, "Message Box", "The site abbriviations have"+
                " been recorded in the program")
            if self.ckSiteCoordN.isChecked():
                self.lnedSiteformnock.clear()
                self.lnedSiteformnock.setEnabled(False)
            elif self.ckSiteCoordY.isChecked():
                self.lnedSiteformsiteID.clear()
                self.lnedSiteformsiteID.setEnabled(False)
            return

        else:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "The list of siteID's you have entered does not"+
                " match the list of unique siteID's displayed from"+
                " the raw data. Please re-enter a list of abbreviated"+
                " siteID's separated by commas.")
            return


    #=======================#
    # Method for  handling user inputs regarding site coordinates
    # Check involves number of entried i.e. if the correct number is
    # entered or not AND whether the entry can successfully be
    # converted to a decimal value (If the error is not related
    # to the length of number of values entered then it can be traced
    # back to the method convert_string_to_decimal
    #=======================#
    def site_coord_check(self):
        sender = self.sender()
       
        if sender == self.lnedSiteformlat:
            try:
                siteLatrecord = str(self.lnedSiteformlat.text())
                self.siteLatdec = self.convert_string_to_decimal(
                    siteLatrecord)

                if len(self.siteLatdec) == self.numsite:
                    pass
                else:
                    raise ValueError('Number of coordinates entered'+
                                     'is not the same as number of'+
                                     'sites')

                self.lnedSiteformlat.clear()
                self.lnedSiteformlat.setEnabled(False)
                QtGui.QMessageBox.about(
                    self, "Message Box", "The site lattitudes have"+
                    " been recorded in the program")
                return
            except:
                self.w = QtGui.QErrorMessage()
                self.w.showMessage(
                    "The list of coordinates you entered did not"+
                    " contain the correct number of entries or"+
                    " did not contain decimal numbers. Please"+
                    " enter them again.")
                return
            
        elif sender == self.lnedSiteformlong:
            try:
                
                siteLongrecord = str(self.lnedSiteformlong.text())
                self.siteLongdec = self.convert_string_to_decimal(
                    siteLongrecord)
                
                if len(self.siteLongdec) == self.numsite:
                    pass
                else:
                    raise ValueError('Number of coordinates entered'+
                                     'is not the same as number of'+
                                     'sites')
                
                self.lnedSiteformlong.clear()
                self.lnedSiteformlong.setEnabled(False)
                QtGui.QMessageBox.about(
                    self, "Message Box", "The site longitudes have"+
                    " been recorded in the program")
                return 
            except:
                self.w = QtGui.QErrorMessage()
                self.w.showMessage(
                    "The list of coordinates you entered did not"+
                    " contain the correct number of entries or"+
                    " did not contain decimal numbers. Please"+
                    " enter them again.")
                return
        else:
            pass

        
    def site_name_check(self):
        pass
    
    #===========================#
    # Method/Helper function to convert the user input strings into
    # a list.
    #===========================#
    def convert_string_to_List(self, StrtoConvert):
        strTolist  = re.sub(
            ",\s", " ", StrtoConvert.rstrip()).split()
        return strTolist
    
    #========================#
    # Method/ Helper function to convert an input string (user inputs)
    # to a list of  numeric values (decimal)
    #=========================#
    def convert_string_to_decimal(self, ItemtoConvert):
        # This is a function that substitutes commas followed by
        # a space (",\s") with only spaces (" ") and then splits
        # the string on those spaces to return a list where each
        # element is an individual number entered by the user
        strTolist = self.convert_string_to_List(ItemtoConvert)

        # This is a list comprehension that takes the items
        # in the list and converts them to Decimal numbers
        strTofloat = [dc.Decimal(x.strip(" ")) for x in strTolist]
       
        return strTofloat
 
    #=======================#
    # Method to open a csv file that contain raw data
    #=======================#
    def open_file(self):
        
        name = QtGui.QFileDialog.getOpenFileName(self,'Open File')
        print(name)
        try:
            self.rawdf = pd.read_csv(name)
            self.rawmodel = ptb.PandasTableModel(self.rawdf)
            self.tblViewraw.setModel(self.rawmodel)
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "The file you have tried to open is a different"+
                " format that a csv. Please convert file to a"+
                " csv format and then load. TELL ANDREW TO MAKE THIS"+
                " 'file open action' more flexible...")

    #=======================#
    # Method to prompt a message when exiting program through either
    # the exit menu button or through 'ctrl+q'
    #=======================#
    def quit_program(self):
        quitmsg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(
            self, 'Message',quitmsg,
            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QtGui.QApplication.quit()
        else:
            pass

#======================#
# Main function
#======================#
# Defining the main function which
# shows the user interface.
def main():
    app = QtGui.QApplication(sys.argv)
    ex = UiMainWindow()
    ex.show()
    sys.exit(app.exec_())


#=================#
# Excute from command line setup
#=================#

if __name__ == "__main__":
    main()
