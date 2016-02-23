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

import pandas as pd
from contextlib import contextmanager
import logging as log
import datetime as TM


# User Interfaces
import ui_mainwindow as mw
import ui_tabledialog as td
import ui_tablepreviewDB as tp
import class_database as uow
import config


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
import PandasTableModelEdit as ptbE


class InputReceived(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        msg = QtGui.QMessageBox()
        msg.setText('Information Recorded')
        msg.addButton(
            QtGui.QPushButton('Ok'), QtGui.QMessageBox.YesRole)
        ret = msg.exec_()


#========================#
# Dialog Widget to Unique Values
# Derived from Data
#========================#

# Creating a Dialog box that will display the values that
# input by the user and will be used to push to the database
class DialogPreview(QtGui.QDialog, tp.Ui_dialog):
    '''
    This class is a pop up dialog box that I can use
    to display pandas dataframes that need to be verified
    by the user.
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


#========================#
# Dialog pop up widget
#========================#

# Creating a Dialog box that will display the values that
# input by the user and will be used to push to the database
class DialogPopUp(QtGui.QDialog, td.Ui_Dialog):
    '''
    This class is a pop up dialog box that I can use
    to display pandas dataframes that need to be verified
    by the user.
    '''
    # Constructor for creating an instance of this object
    # which is made through multiple inheritance
    # i.e. QDialog and Ui_Dialog

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


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
    Description:
    and the QMainWindow to integrate them into a class that
    we can enable signal and designate slots.

    To do: Need a file handler for the raw data files because it will
    be different every time we run it.---------DONE

    To do: Need to connect the file handler form the raw data
    forms to the global dataframe object that gets repeatedly called
    ------------------ DONE

    To do: Need to modify col_view_handle method to be able
    to display either unique vales from a column or a table
    of values created by the user...as of now it will be two
    different methods preview_view_handle.

    To do: Need code a better handler for reading files; add
    The ability to read different file types i.e. txt, tab-delimited,
    xlsx, and csv

    To do: Need to layout the structure of the program on paper
    or with a diagram

    To do: Need to be sure that all entries into the user interace
    are recorded and written to a file such that we can
    recreate everything from those files and edit the database
    if errors were made during the entry.

    To do: Catch errors for not having the LTER combo box checked.
    or the site number combo box checked.
    '''

    # Constructor for initiating this object which is essential
    # the program.
    def __init__(self, parent=None):
        super().__init__(parent)
        #======================#
        # Setting the User interface
        # from our qtdesigner code (this is inherited)
        #======================#
        self.setupUi(self)

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
        # Creating objects that will serve
        # to maintain a dialog box when called upon in different
        # methods
        # Additionally creating objects that will serve as dialog
        # boxes for each form in our program and to catch
        # specific signals to perform database operations with
        self.w = None
        self.colView = None
        self.siteDialog = DialogPreview()
        self.mainDialog = DialogPreview()
        self.taxaDialog = DialogPreview()
        self.rawDialog = DialogPreview()
        self.taxaDialog = DialogPreview()

        # Setting up the dictionaries that will be used to
        # concatenate user information
        self.taxatextdict = {}
        self.seasontextdict = {}
        self.seasonnumdict = {}

        # self.seasonindex = ['spring', 'summer', 'fall', 'winter']
        self.seasondateindex = [int(3), int(6), int(8), int(12)]

        #=====================#
        # Catching MENU BAR actions from user interface
        #=====================#
        # Open file
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.open_file)

        # Quit Program
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.triggered.connect(self.quit_program)
        #=====================#
        # Catching BUTTON signals from user interface
        #=====================#
        self.btnloadrawview.clicked.connect(self.open_file)
        self.btnSitePush.clicked.connect(self.site_concat)
        self.btnMainConcat.clicked.connect(self.main_concat)
        self.btnTaxaConcat.clicked.connect(self.taxa_concat)
        self.btnSeasConvertConcat.clicked.connect(self.season_convert)
        self.btnSeasonReset.clicked.connect(self.season_reset)
        self.btnNullReset.clicked.connect(self.null_reset)

        #=====================#
        # Catching SPIN BOX
        #=====================#
        self.spinboxselectmetaID.valueChanged.connect(
            self.meta_data_check)

        #=======================#
        # Catching LINE EDIT signals from user interface
        #=======================#
        #======= NULL VALUES =======#
        self.lnedNullnumeric.returnPressed.connect(self.null_handle)
        self.lnedNulltext.returnPressed.connect(self.null_handle)

        #======= SITE INFO =====#
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
        # Meata Data Url
        self.lnedselectmetaurl.returnPressed.connect(
            self.meta_data_check)

        #=========TAXA INFO======#
        # Assigning all the lned edits for the taxa table form
        # into a list
        self.taxalnedlist = [
            self.lnedSppCode, self.lnedKingdom, self.lnedPhylum,
            self.lnedClass, self.lnedOrder, self.lnedFamily,
            self.lnedGenus, self.lnedSpp]

        # Iterating over the objects in a list for the taxanomic
        # form and setting the line edits to disable and connecting
        # the check boxes to one method
        for i, item in enumerate(self.taxalnedlist):
            self.taxalnedlist[i].setEnabled(False)
            self.taxalnedlist[i].returnPressed.connect(
                self.multiple_text)

        #===========SEASON INFO=======#
        # Assing all the lned edits for the season table form
        # into a list
        self.seasonlnedlist = [
            self.lnedSpringConvert, self.lnedSummerConvert,
            self.lnedFallConvert, self.lnedWinterConvert]

        for i, item in enumerate(self.seasonlnedlist):
            self.seasonlnedlist[i].setEnabled(False)
            self.seasonlnedlist[i].returnPressed.connect(
                self.multiple_text)

        self.lnedSeasConvertLabel.returnPressed.connect(
            self.season_convert)

        #=======================#
        # Catching CHECK BOX signals from user interface
        #=======================#
        self.ckSiteCoordN.stateChanged.connect(self.site_coord_options)
        self.ckSiteCoordY.stateChanged.connect(self.site_coord_options)

        # Assiging all the check boxes for the taxa table form
        # into a list
        self.taxackboxlist = [
            self.ckSppCode, self.ckKingdom, self.ckPhylum,
            self.ckClass, self.ckOrder, self.ckFamily,
            self.ckGenus, self.ckSpp]

        for i, item in enumerate(self.taxackboxlist):
            self.taxackboxlist[i].stateChanged.connect(
                self.multiple_check_box_behavior)

        self.seasonckboxlist = [
            self.ckSpringConvert, self.ckSummerConvert,
            self.ckFallConvert, self.ckWinterConvert]

        for i, intem in enumerate(self.seasonckboxlist):
            self.seasonckboxlist[i].stateChanged.connect(
                self.multiple_check_box_behavior)

        #======================#
        # Catching the site COMBO BOX text
        #======================#
        self.cboxSiteCount.activated.connect(self.get_sitebox)
        self.cboxselectlter.activated.connect(self.meta_data_check)

        #======================#
        # Creating DATA MODELS to view pandas dataframes on
        # in qttreeView
        #======================#
        # Setting the metadata model data to mirrow what is in our
        # file titled meta_file_test.csv
        metamodel = ptb.PandasTableModel(self.metadf)
        self.tblViewmeta.setModel(metamodel)

    #=========================#
    # Defining the methods to ensure that
    # the user is starting the program correctly.
    # they must indicate the globalid of the dataset
    # they are working with, metadata url
    # and lterlocation
    #=========================#
    #========MAIN DATA=========#
    #---SPECIAL--VALUE--GLOBALID--#
    #---SPECIAL--VALUE--LTERLOCATION--#
    #---SPECIAL--VALUE---METAURL--#
    def meta_data_check(self):
        # Identify signal sender
        sender = self.sender()
        # Spin box value indicating the global_id of the row
        # that corresponds to the metadata information being
        # input
        if sender == self.spinboxselectmetaID:
            self.globalid = int(self.spinboxselectmetaID.value())
            return
        # Saving the lter location that is chosen from the
        # combo box
        elif sender == self.cboxselectlter:
            self.lterlocation = self.cboxselectlter.currentText()
            return
        # Writing a series of try except commands to
        # 1) check to see if an LTER Site was chosen before the
        # metadata url infomration is enter
        # 2) Check to see if the LTER Site location entered
        # matches that from the metadata
        # 3) Checks the URL to see if it is the correct one
        # according to the GlobalID entered.
        elif sender == self.lnedselectmetaurl:
            try:
                self.metaurl = self.lnedselectmetaurl.text()
                # Metadata check: data pulled from meta dataframe
                metacheck = str(self.metadf.loc[
                    self.metadf['global_id'] ==
                    self.globalid]['site_metadata'].values[0])
                # LTER check: data pulled from meta dataframe
                lterloccheck = str(self.metadf.loc[
                    self.metadf['global_id'] ==
                    self.globalid]['lter'].values[0])

                # Check global_id and lter metadata url entered
                # agains the user inputs (self)
                if metacheck  ==  self.metaurl and\
                   lterloccheck == self.lterlocation:

                    # Notification that the url is correct
                    QtGui.QMessageBox.about(
                        self, "Message Box", "Please enter this url in" +
                        " your internet browser. Then download the" +
                        " raw data from the site and load into the" +
                        " program. The file type must be a '.csv'." +
                        " Otherwise get Andrew to fix this.")
                    self.lnedselectmetaurl.clear()
                    self.lnedselectmetaurl.setEnabled(False)
                    return
                else:
                    # Error for mismatching metadata link
                    self.w = QtGui.QErrorMessage()
                    self.w.showMessage(
                        "The url you entered does not correspond to the" +
                        " url derived from the GlobalID value provided." +
                        " Please check the GlobalID value and url entered.")
                    return
            except:
                # Error for mismatching LTER site location
                self.w = QtGui.QErrorMessage()
                self.w.showMessage(
                    "The LTER Site you entered does not correspond" +
                    " to the one derived from the GlobalID value." +
                    " Please check the GlobalID value and LTER" +
                    " Site entered.")
                return
        else:
            return

    #======================#
    # Method to handle the conversion of
    # factors that represent NULL values
    #======================#
    def null_handle(self):
        # Identify sender
        sender = self.sender()

        # Check that the raw data frame
        # has been loaded
        try:
            if type(self.rawdf) is pd.DataFrame:
                pass
            # If it has not, raise a lookup error
            else:
                raise LookupError
        # Pop up Error message
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "Please make sure you have loaded a raw data file.")
            self.w.show()
            return

        # Because there are two line edits associated
        # with t his method we have to specify the behacvior
        # for each.

        # If the sender is from the line edit inteded
        # to handle numeric values that represent NULL
        if sender == self.lnedNullnumeric:
            # Extract the user into
            self.nullnuminput = self.lnedNullnumeric.text()
            try:
                # convert the user input into a list of strings
                # and integers.
                # This is done because a whole column in the
                # dataframe can be treated like a string if one
                # record is a string rather than a numeric type
                numnullinputlisttext = self.convert_string_to_List(
                    self.nullnuminput)
                numnullinputlist = self.convert_string_to_decimal(
                    self.nullnuminput, 'Integer')
                print(numnullinputlist)

                # Append the null values numeric list with
                # text counterparts
                for i in numnullinputlisttext:
                    numnullinputlist.append(i)

                # Use a nested for loop to iterate over
                # all columns in the data frame
                # and replace anything that matches
                # an item in our null value numeric list
                # with 'NULL'
                for i in numnullinputlist:
                    for j in self.rawdf.columns:
                        self.rawdf[j].replace(i, 'NULL', inplace=True)

            except Exception as e:
                print(str(e))
            message = InputReceived()
            message.show()
            self.lnedNullnumeric.clear()

        # Perform similar operations as above if the sender
        # is from the line edit intended to handle text
        # values that represent null values
        elif sender == self.lnedNulltext:
            self.nulltextinput = self.lnedNulltext.text()
            try:
                textnullinputlist = self.convert_string_to_List(
                    self.nulltextinput)
                print(textnullinputlist)

                for i in textnullinputlist:
                    for j in self.rawdf.columns:
                        self.rawdf[j].replace(i, 'NULL', inplace=True)

            except Exception as e:
                print(str(e))
            message = InputReceived()
            message.show()

        try:

            rawmodel = ptb.PandasTableModel(self.rawdf)
            self.rawdfnull = pd.DataFrame.copy(self.rawdf)
            self.tblViewraw.setModel(rawmodel)

        except Exception as e:
            print(str(e))

    #======================#
    # This method resets the rawdf
    # object if the values replaced with
    # the null_handle methods happend to
    # be incorrect
    #======================#
    #---SPECIAL--VARIABLE--UPDATE--RAWDF--#
    def null_reset(self):
        self.rawdf = pd.DataFrame.copy(self.rawdfnull)
        rawmodel = ptb.PandasTableModel(self.rawdf)
        self.tblViewraw.setModel(rawmodel)
        return
    #========================#
    # Defining a method to return a view of the unique site
    # abbreviations derived from the raw data.
    #========================#
    #=====SITE ABBR LOCATION DATA ======#
    #---SPECIAL--VARIABLE--SITECOLUMN---#
    #---SPECIAL--VARIABLE--SITELISTTOADD--#

    def col_view_handle(self):
        sender = self.sender()
        if sender == self.lnedViewSite:
            self.sitecolumn = self.lnedViewSite.text()

            # User input for identifying the column that
            # contains site abbreviations
            columntofind = self.lnedViewSite.text()

            # Quality control check: user supplied value of column
            # name, if not there, throw error
            try:
                collisttoadd = list(self.rawdf[columntofind].unique())

                # Special catch to create a list of unique site names
                # once the user has specified that column that
                # contains site abbreviations
                self.sitelisttoadd = collisttoadd
            except:
                self.w = QtGui.QErrorMessage()
                self.w.showMessage(
                    "You entered a string that does not match" +
                    " any column name in the raw data table. Please"
                    " re-enter the column name again. Addtionally" +
                    " make sure a raw data file is loaded into the" +
                    " program.")
                self.w.show()
                return
            finally:
                # Creating a list of unique column values based on
                # the column name the user supplied
                collistdf = pd.DataFrame(collisttoadd)
                collistdf.columns = [columntofind]

                # If quality control passes, instantiate the popup
                # dialog box that will display the derived informatoin
                self.colView = DialogPopUp()

                # Creating the table model to view the subsetted
                # values in dataframe form with qttableview
                self.collistmodel = ptbE.PandasTableModel(collistdf)

                # Settting the data Model to view through the
                # dialog box from UniqueColumnList
                self.colView.tblList.setModel(self.collistmodel)
                self.colView.show()

            # Catch designed to update the sitelist to add
            # if the user finds errors
            self.collistmodel.dataChanged.connect(
                self.update_site_list)

        else:
            pass

    #=======================#
    # Method to update the sitelisttoadd
    # special variable base on whether
    # the user adds or removes items
    # from the col list model view
    #=======================#
    #-----SPECIAL---VARIABLE--UPDATE---SITELISTTOADD--#
    def update_site_list(self):
        self.sitelisttoadd = self.collistmodel.data(
            None, QtCore.Qt.UserRole)
        print(self.sitelisttoadd)

    #=========================#
    # Method to retrieve the information from the combo box
    # that list the unique number of sites and
    # gives an error if this number is different from what
    # is derived from the raw data
    #=========================#
    def get_sitebox(self):
        # Create an attributre to hold the information
        # about the number of sites
        self.numsite = int(self.cboxSiteCount.currentText())

        # Quality control check: value vs derived from data
        if self.numsite == len(self.sitelisttoadd):
            pass
        else:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage('The number of unique sites selected' +
                               ' does not correspond to the raw' +
                               ' data loaded.')
            return

    #===========================#
    # Method ot handle the concatenation of sites
    # into a table to push to the database
    # Requires numsite, sitelisttoadd, lat,long
    #==========================#
    #--SPECIAL--VARIABLE--CHECK--SITELISTTOADD--#
    # IF there are errors due to whats derived
    # and whats input regarding the sitelisttoadd
    # the check here.
    # This is a thorogh check, turns input and
    # derived values to lower case
    def site_id_check(self):
        self.w = QtGui.QErrorMessage()
        try:
            required = self.numsite
        except:

            self.w.showMessage(
                "You must set the number of unique site " +
                "abbreviations before proceeding.")
            return
        try:
            required = self.sitelisttoadd
        except:
            self.w.showMessage(
                "You must identify the column in the raw data " +
                "that contains site abbreviations.")
            return

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
        self.siteIDrecord_re = self.convert_string_to_List(
            self.siteIDrecord)

        #-------#
        # Check siteID entries for conformity to raw data
        #-------#
        if [x.lower() for x in self.siteIDrecord_re] == [
                y.lower() for y in self.sitelisttoadd] and len(
                    self.siteIDrecord_re) == self.numsite:

            print([x.lower() for x in self.siteIDrecord_re])
            print([y.lower() for y in self.sitelisttoadd])

            QtGui.QMessageBox.about(
                self, "Message Box", "The site abbriviations have" +
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
                "The list of siteID's you have entered does not" +
                " match the list of unique siteID's displayed from" +
                " the raw data. Please re-enter a list of abbreviated" +
                " siteID's separated by commas.")
            return

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

        elif self.ckSiteCoordY.isChecked() == False and\
                self.ckSiteCoordN.isChecked() == False:
            self.lnedSiteformnock.setDisabled(True)
            self.lnedSiteformsiteID.setDisabled(True)
            self.lnedSiteformlat.setDisabled(True)
            self.lnedSiteformlong.setDisabled(True)

    #=======================#
    # Method for  handling user inputs regarding site coordinates
    # Check involves number of entried i.e. if the correct number is
    # entered or not AND whether the entry can successfully be
    # converted to a decimal value (If the error is not related
    # to the length of number of values entered then it can be traced
    # back to the method convert_string_to_decimal
    #=======================#
    #=========SITE LAT/LONG DATA============#
    def site_coord_check(self):
        # Identifying sender
        sender = self.sender()
        # Creating generic error messages that will be required
        # for looking at the number of entries (lengthError)
        # and the type of entries (coordinateError)
        coordinateError = (
            "The list of coordinates you entered did not" +
            " contain decimal numbers. Please" +
            " enter them again.")
        lengthError = (
            'Number of coordinates entered' +
            'is not the same as number of' +
            'sites')
        self.w = QtGui.QErrorMessage()

        if sender == self.lnedSiteformlat:
            try:
                # Extract the user input from the latitude
                # line edit form
                siteLatrecord = str(self.lnedSiteformlat.text())
                # Convert the user input into a list of
                # decimate values
                self.siteLatdec = self.convert_string_to_decimal(
                    siteLatrecord)

                # Check for length errors
                if len(self.siteLatdec) == self.numsite:
                    pass
                else:
                    self.w.showMessage(lengthError)
                    return
                # IF check for length passes clear the linedit
                # and disable the line edit box
                self.lnedSiteformlat.clear()
                self.lnedSiteformlat.setEnabled(False)
                # Send pop up message regarding the status of the
                # users entry (i.e. it was recorded in the program)
                QtGui.QMessageBox.about(
                    self, "Message Box", "The site lattitudes have" +
                    " been recorded in the program")
                return
            # If any of the steps above failed (likely the converting
            # user input into decimals) then throw our decimal
            # value error (coordinateError)
            except:
                self.w.showMessage(coordinateError)
                return

        # Same instructions as above except to handle user inputs
        # for longitute rather than lattitude
        elif sender == self.lnedSiteformlong:
            try:

                siteLongrecord = str(self.lnedSiteformlong.text())
                self.siteLongdec = self.convert_string_to_decimal(
                    siteLongrecord)

                if len(self.siteLongdec) == self.numsite:
                    pass
                else:
                    self.w.showMessage(lengthError)
                    return
                self.lnedSiteformlong.clear()
                self.lnedSiteformlong.setEnabled(False)

                QtGui.QMessageBox.about(
                    self, "Message Box", "The site longitudes have" +
                    " been recorded in the program")
                return
            except:
                self.w = QtGui.QErrorMessage()
                self.w.showMessage(coordinateError)
                return
        else:
            pass

    #=======================#
    # Method to check that the number
    # from the dropdown menu matches the
    # number of site abbreviation input
    # by the user
    #=======================#
    #=========SITE DESCRIPTION DATA============#
    # created from line edit
    def site_name_check(self):
        # Ensure that the combo box
        # for number of unique sites is set
        try:
            required = self.numsite
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "You must set the number for the unique site " +
                "abbreviations.")
            return

        # Check the set number of sites
        # Against the number of site abbreviation
        # input into the program by the user
        self.sitenames = self.convert_string_to_List(
            self.lnedSiteformnames.text())

        print(self.sitenames)

        # If the lengths of the list and numbers
        # fromt he combo box match up, record
        # The update status
        if len(self.sitenames) == self.numsite:
            QtGui.QMessageBox.about(
                self, "Message Box", "The site names have" +
                " been recorded in the program")
            self.lnedSiteformnames.clear()
            self.lnedSiteformnames.setEnabled(False)
        # Else delete the self.sitelist
        # and throw error.
        else:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "The list of names you entered did not" +
                " contain the correct number of entries. Please" +
                " enter them again.")
            del self.sitenames
            return

    #=======================#
    #
    #=======================#
    def site_concat(self):
        try:
            required = self.lterlocation
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "You must record the LTER site location of the data" +
                "that you are working with. This can be done " +
                "underneath the Raw Data and MetaData Viewers.")
            return

        lterlist = []
        for i in enumerate(self.siteIDrecord_re):
            lterlist.append(self.lterlocation)
        print(lterlist)

        if self.ckSiteCoordY.isChecked():
            try:

                self.siteDataAll = pd.DataFrame(
                    {'siteID': self.siteIDrecord_re,
                     'lterID': lterlist,
                     'lat': np.array(self.siteLatdec, dtype=np.float),
                     'long': np.array(self.siteLongdec, dtype=np.float),
                     'descript': self.sitenames},
                    columns=['siteID', 'lterID', 'lat', 'long',
                             'descript'])

                # Checking code
                print(self.sitenames)
                print(self.siteDataAll)
                print(self.siteDataAll.dtypes)

            except Exception as e:
                print(str(e))
                # self.w = QtGui.QErrorMessage()
                # self.w.showMessage(" Not all information is entered to" +
                #                   " proceed to this step. Please finish" +
                #                   " completing the form.")
                # return
        elif self.ckSiteCoordN.isChecked():
            try:
                nulllist = []
                for i in enumerate(self.siteIDrecord_re):
                    nulllist.append("NULL")
                print(nulllist)
                self.siteDataAll = pd.DataFrame(
                    {'siteID': self.siteIDrecord_re,
                     'lterID': lterlist,
                     'lat': nulllist,
                     'long': nulllist,
                     'descript': self.sitenames},
                    columns=['siteID', 'lterID', 'lat', 'long',
                             'descript'])

                convertcolumns = ['lat', 'long']
                for i in convertcolumns:
                    self.siteDataAll[i] = pd.to_numeric(
                        self.siteDataAll[i], errors='coerce')

            except Exception as e:
                print(str(e))

        else:
            pass

        siteDataAllmodel = ptbE.PandasTableModel(self.siteDataAll)
        self.siteDialog.tblList.setModel(siteDataAllmodel)
        self.siteDialog.show()
        self.siteDialog.btnPush.clicked.connect(self.upload_to_database)

    #====================#
    # Method to concatenate the information that will
    # be going in the main table of the databse
    # This is based on the user input of the globalid value
    # if this is wrong then the information will be wrong
    #====================#
    #=========MAIN DATA========#
    def main_concat(self):
        self.w = QtGui.QErrorMessage()

        # These are the columns that contain information that we're
        # interested in.
        maincolumns = ['title', 'data_type', 'start_date', 'end_date',
                       'temp_int', 'comm_data', 'study_type',
                       'site_metadata', 'portal_id']

        try:
            required = self.sitelisttoadd
        except:
            self.w.showMessage(
                " Establish the unique site abbreviations by " +
                " completing the Site Infomation from Raw Data box." +
                " This box is on the previous form.")
            return

        # Trying to take a subset of the meta data columns
        # based on user input of the globalid value
        try:
            submain = self.metadf[self.globalid - 1:self.globalid][
                maincolumns]

            # If subsetting the metadata fails because there is no
            # globalid value, throw error

            # Try to parse the dates for start and end date information
            # from the metadata. We only want to extract the
            # year information
            try:
                self.startyr = pd.to_datetime(
                    submain['start_date'], format="%m/%d/%Y").dt.year

                self.endyr = pd.to_datetime(
                    submain['end_date'], format="%m/%d/%Y").dt.year
                print(self.startyr, self.endyr)
            # If the parsing fails through an error
            except:
                self.w.showMessage("Date information can not be parsed")
                return

            # Try to create a preliminary main datatable based on
            # the information already provided in the meta data.
            try:
                # This command creates a single row with all the metadata
                # information and parsed dates and fills NULL values
                # where the user will have to input information
                mainDataSingle = pd.DataFrame(
                    {
                        'title': submain['title'],
                        'samplingunits': 'NULL',
                        'samplingprotocol': submain['data_type'],
                        'startyr': self.startyr,
                        'endyr': self.endyr,
                        'samplefreq': 'NULL',
                        'totalobs': 'NULL',
                        'studytype': submain['study_type'],
                        'community': submain['comm_data'],
                        'siteID': 'NULL',
                        'sp_rep1_ext': 'NULL',
                        'sp_rep2_ext': 'NULL',
                        'sp_rep3_ext': 'NULL',
                        'sp_rep4_ext': 'NULL',
                        'metalink': submain['site_metadata'],
                        'knbID': submain['portal_id']
                    },
                    columns=[
                        'title', 'samplingunits', 'samplingprotocol',
                        'startyr', 'endyr', 'samplefreq',
                        'totalobs', 'community', 'siteID', 'sp_rep1_ext',
                        'sp_rep2_ext', 'sp_rep3_ext', 'sp_rep4_ext',
                        'metalink', 'knbID'])
            # If for some reason the that dataframe above could not
            # be created then throw and error
            except:
                self.w.showMessage(
                    "Couldn't extract metadata information")
                return
            finally:
                print(mainDataSingle)

            # From the single row with metadata information,
            # create an expanded version of that row that has
            # informatoin about all the unique sites that are
            # present in the study being described by the meta data
            try:
                self.mainDataAll = pd.concat(
                    [mainDataSingle] * len(self.sitelisttoadd),
                    ignore_index=True)

                convertcolumns = [
                    'samplefreq', 'totalobs', 'sp_rep1_ext',
                    'sp_rep2_ext', 'sp_rep3_ext', 'sp_rep4_ext']

                for i in convertcolumns:
                    self.mainDataAll[i] = pd.to_numeric(
                        self.mainDataAll[i], errors='coerce')

                # This step is depedent on accurate information
                # provided from the siteView/ sitelisttoadd
                # attribute
                for i in range(len(self.sitelisttoadd)):
                    self.mainDataAll.loc[i, 'siteID']\
                        = self.sitelisttoadd[i]

                self.mainDataAllModel = ptbE.PandasTableModel(
                    self.mainDataAll)

                self.mainDialog = DialogPreview()
                self.mainDialog.tblList.setModel(self.mainDataAllModel)
                self.mainDialog.show()
                self.mainDialog.btnPush.clicked.connect(
                    self.upload_to_database)

            except Exception as e:
                print(str(e))

            finally:
                print(self.mainDataAll.dtypes)

            # If the data is change in the main table model
            # then record the changes
            self.mainDataAllModel.dataChanged.connect(
                self.update_main_table)
        except:
            self.w.showMessage("The globalID value is not set")
            return
        finally:
            print(submain)

    #=========================#
    # This method is giong to catch all the
    # edits that occur when users manually input
    # information into the main table. This
    # is for data regarding spatial extents
    # or sampling frequency
    #=========================#
    #=========MAIN DATA========#
    def update_main_table(self):
        print(self.mainDataAllModel.data(None, QtCore.Qt.UserRole))

    #=========================#
    # This method handles multiple checkbox
    # widgets that are directly connected
    # to multiple line edit widgets. Behavior of
    # objects within here are dependent on
    # multiple_text methods as well
    #=========================#
    #=========TAXA DATA==========#
    #=========SEASON DATA==========#
    def multiple_check_box_behavior(self):
        # Creating the behavior for the taxa table form with regard
        # to checked boxes and line edits that correspond to
        # those boxes

        self.CheckBoxSender = self.sender()

        # Using a list comprehension to see which list of
        # check boxes is sending the signal and assign
        # the activated variable accordingly

        if self.CheckBoxSender in self.taxackboxlist:
            activated = [x.isChecked() for x in self.taxackboxlist]
        elif self.CheckBoxSender in self.seasonckboxlist:
            activated = [x.isChecked() for x in self.seasonckboxlist]
        else:
            pass

        self.activeindex = [
            i for i, item in enumerate(activated) if item == True]

        print(self.activeindex)

        # Retrieve an index to our check box list to determine
        # if it has been deactivated (i.e. unchecked)
        self.inactiveindex = [
            i for i, item in enumerate(activated) if item == False]

        # Setting activation status for linedits (True AND False)
        # based on wether the corresponding check boxes have
        # been activated or deativated

        if self.CheckBoxSender in self.taxackboxlist:
            for i in self.activeindex:
                self.taxalnedlist[i].setEnabled(True)
        elif self.CheckBoxSender in self.seasonckboxlist:
            for i in self.activeindex:
                self.seasonlnedlist[i].setEnabled(True)

        # If the check box has be deactivated (unchecked) the
        # clear the line edit that corresponds with it
        # and disable text entries.
        # Additionally, if the user had modified the text
        # edit line and sent the input to the program, pop
        # it from the dictionary that houses the text entries.
        for i in self.inactiveindex:

            if self.CheckBoxSender in self.taxackboxlist:
                self.taxalnedlist[i].clear()
                self.taxalnedlist[i].setEnabled(False)
                if i in self.taxatextdict:
                    del self.taxatextdict[i]
                    self.multiple_text()
                else:
                    pass

            if self.CheckBoxSender in self.seasonckboxlist:
                self.seasonlnedlist[i].clear()
                self.seasonlnedlist[i].setEnabled(False)
                if i in self.seasontextdict:
                    del self.seasontextdict[i]
                    self.multiple_text()
                try:
                    if i in self.seasonnumdict:
                        del self.seasonnumdict[i]
                        self.multiple_text()
                except Exception as e:
                    print(str(e))

        print(self.taxatextdict)
        print(self.seasontextdict)

    #======================#
    # Method to handle multiple line
    # edit widgets that are directly
    # connected to check boxes
    # above them this method is pretty flexible
    # and can easily be appendend to handle
    # checkbox/linedit combos on multiple forms
    #======================#
    #=========TAXA DATA==========#
    #=========SEASON DATA==========#
    def multiple_text(self):
        self.w = QtGui.QErrorMessage()
        columnerror = (
            'Please make sure a raw data table is loaded' +
            ' and the column names input to the program' +
            ' match the column headers of the data.')

        # All text entries to the line edit forms on the taxa table
        # form go here if 'enter' is pressed in any of the line
        # edits

        # First thing to determine is whether the activated
        # line edit have any text modifications i.e. user inputs
        # If it does, save the input to the dictionary
        # title 'self.taxatextdict'
        if self.CheckBoxSender in self.taxackboxlist:

            for i in self.activeindex:
                if self.taxalnedlist[i].text() != None:
                    self.taxatextdict[i] = self.taxalnedlist[i].text()
                else:
                    pass
            # Using the dictionary to check the input against the
            # raw data file to see if they correspond
            # to actual columns in the raw data frame.
            try:
                if [x.isModified() for x in self.taxalnedlist]:
                    try:
                        print(self.rawdf[list(self.taxatextdict.values())])
                    except Exception as e:
                        print(str(e))
                        self.w.showMessage(columnerror)
                        return
            except Exception as e:
                print(str(e))

        # CHecking whether the season line edits have any inputs
        elif self.CheckBoxSender in self.seasonckboxlist:

            for i in self.activeindex:
                if self.seasonlnedlist[i].text() != None:
                    # If there are inputs then extract them and
                    # try to put their values intwo two
                    # different dictionaries (one which is text
                    # and one which attempts to convert input
                    # to numeric values because seasonal data can
                    # be represented by both numeric or text
                    # values
                    self.seasontextdict[i] = self.seasonlnedlist[i].text()
                    try:

                        self.seasonnumdict[i] = int(
                            self.seasonlnedlist[i].text().strip(" "))
                    except Exception as e:
                        print(str(e))

                    print(self.seasontextdict)
                    print(self.seasonnumdict)
                else:
                    pass

    #=============================#
    # Method to concatenate the taxonomic information
    # that uses help functions to merge perviously pushed
    # data and perform formatting operations.
    #
    # NOTE: the behavior underlying the taxatextdict object
    # is completely depedent on the multiple_check_box_behavior and
    # multiple_text methods... these allow for very
    # flexible editing
    #=============================#
    #=======TAXA DATA==========#
    def taxa_concat(self):

        try:
            if len(self.taxatextdict.values()) == 0:
                raise ValueError
            else:
                pass
            print('Testing Taxa Concatenate')

            print(self.data_list(
                ['projID'], self.merge_main_to_taxa()))

        except Exception as e:
            print(str(e))
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                'Make sure that you have designated the column  ' +
                'header in the raw data that contains the ' +
                'information about site abbreviations.')

    #===================#
    # This method uses information from the line edits
    # regarding season information that needs to be
    # changed as well as there check boxes
    #
    # NOTE: the behavior is completely dependend
    # on the multiple_check_box_behavior and
    # multiple_text methods... these allow for
    # flexible editing.
    #===================#
    #========SEASONDATA==========#

    def season_convert(self):
        self.w = QtGui.QErrorMessage()
        # Identifyin the sender
        sender = self.sender()

        # If the sender is the line edit where the column
        # containing seasonal information is called
        # the try the following
        if sender == self.lnedSeasConvertLabel:
            # See if the column actually exist or throw
            # error. Additionally save the column name
            # as a variable
            try:
                self.seasoncolumn = str(self.lnedSeasConvertLabel.text())
                print(self.rawdf[self.seasoncolumn])
                QtGui.QMessageBox.about(
                    self, 'Status', (
                        'This information has been recorded' +
                        ' in the program.'))
                self.lnedSeasConvertLabel.clear()
                return
            except Exception as e:
                print(str(e))
                self.w.showMessage(
                    "Please Identify the column that contains seasonal" +
                    " information")
                return
        # If the sender is anyone else, skip the above step
        else:
            pass

        # Testing our dictionary items regarding season and
        # defintions within the raw data file
        # The values to replace have to be all numeric or all
        # strings, can't be both. Hopefully that won't happen
        # much

        # If any of the items in the season number dictionary
        # (number for numeric) are > 0, then replace that
        # variable with the corresponding month we are
        # defaulting to descibe seasons
        if any([x > 0 for i, x in self.seasonnumdict.items()]):

            # This is a nested loop to go through our
            # list of our dictionaries, items
            # and index the column of the raw dataframe
            # and replace the value there with the dictionary
            # date that it should be
            for i, item in self.seasonnumdict.items():
                print(type(item))
                if type(item) == int:
                    # Replace item with our date index
                    self.rawdf[self.seasoncolumn].replace(
                        item, self.seasondateindex[i], inplace=True)

        # if the above attempt to convert labels based on
        # numeric types fails then fall back to object types
        # (or strings).
        # Perfor the same operations above i.e. replace
        # factor levels with prefered date index
        elif any([x is not None for i, x in self.seasontextdict.items()]):
            print('No numeric values only text...')
            for i, item in self.seasontextdict.items():
                print(type(item))
                if type(item) == str:
                    self.rawdf[self.seasoncolumn].replace(
                        item, self.seasondateindex[i], inplace=True)

        else:
            self.w.showMessage(
                "Can't convert seasonal information. Be" +
                " sure you pressed 'enter' after filling " +
                "in the lines underneath the check boxes.")
            return

        # And reset our model view for the raw data to
        # reflect the changexs
        self.rawdfseason = pd.DataFrame.copy(self.rawdf)
        self.rawmodelseas = ptb.PandasTableModel(self.rawdf)
        self.tblViewraw.setModel(self.rawmodelseas)

    #========================#
    # Method to reset the raw data frame
    # because the changes to seasonal information
    # went wrong.
    #========================#
    #========SEASONDATA==========#
    def season_reset(self):
        # Reset the season dictionaries to correct the
        # behavior of the line edits before
        # resetting the data
        self.seasonnumdict = {}
        self.seasontextdict = {}

        # Creating an intermediate variable to hold
        # the dataframe with all the unchanged values
        # that occured on forms before this one!!!!
        self.rawdf = pd.DataFrame.copy(self.rawdfnull)

        # Creating new model view to update the
        # viewer based on the reset.
        self.rawmodelreset = ptb.PandasTableModel(self.rawdf)
        self.tblViewraw.setModel(self.rawmodelreset)
        print(self.rawdf)

    #=====================#
    # This is a helper method that takes two inputs
    # an 'extracolumns' variable which is supposed
    # to be a column from a dataframe AND inputdata
    # which is a dataframe where the extracolumns
    # column exists.
    #======================#
    #=========HELPER========#
    def data_list(self, extracolumns, inputdata):
        col = extracolumns
        taxadiclist = list(self.taxatextdict.values())

        # Appending the dictionary list to include other
        # columns we want to return
        for i in taxadiclist:
            col.append(i)

        # Creating a list that will house subsets of the raw data
        # (subseted by site Abbreviations)
        mergeddata = inputdata
        datalist = []

        # Iterating over our list of site Abbreviatoins
        # and subsetting the merged dataframe. Each subset
        # is an element of the data list
        for i in self.sitelisttoadd:
            datalist.append(
                mergeddata[mergeddata[str(self.sitecolumn)].isin([i])])

        # Iterating over each dataframe in the list to
        # take the unique combinations of factors between each
        # of our selected columns
        subsetdatalist = []
        for i in datalist:
            subsetdatalist.append(
                i[col].drop_duplicates(col))

        # Transforming the list of dataframes to
        # one large dataframe to be pushed
        subdfaddNULL = subsetdatalist[0]
        subdfaddNULL = subdfaddNULL.append(subsetdatalist[1::])

        return(subdfaddNULL)

    #======================#
    # This is the method that calls the classes that
    # interact with the postgresql database
    #======================#
    #=========HELPER========#
    def upload_to_database(self):
        # Identifying the sender of the signal
        sender = self.sender()
        print(sender)
        self.w = QtGui.QErrorMessage()
        # Establishing a generic response for failures
        # to load to database based on quality assurance
        # checks
        errormessage = ("Data is already present in the database:" +
                        " please check the file you are using.")

        try:
            required = self.sitelisttoadd
        except:
            self.w.showMessage(
                "You must verify the unique site abbreviation" +
                " in the Site Names and Coordinates Form.")
            return
        try:
            self.cboxselectlter.currentText() is not None
        except:
            self.w.showMessage(
                "You must select the current LTER site that you are" +
                " are working with. This can be set underneath the" +
                "Raw Data and MetaData Viewers.")
            return
        try:
            required = self.metaurl
        except:
            self.w.showMessage(
                "You must enter the metadata link for the dataset" +
                "you will be working with. This can be entered" +
                "underneath the Raw Data and MetaData Viewers.")
            return

        # If the sender is from siteDialog perform those
        # opertations given the arguments our 'uow' classes
        if sender == self.siteDialog.btnPush:
            # Creating an instance of our class
            # that will do quieres to check data before
            # pushing to databse
            # Supplying the following arguments:
            # dataframe, config classes, tablename,
            # list of unique site abbreviations, current LTER
            # that we're working with
            dbhandle = uow.UploadToDatabase(
                self.siteDataAll, config, 'sitetable',
                sitelist=self.sitelisttoadd,
                lter=self.cboxselectlter.currentText())

        elif sender == self.mainDialog.btnPush:
            # Note this handle checks more than just the sites
            # because its going to load data into the main table.
            # It also checks that each site about to be loaded
            # does NOT have the same metadata url as previous
            # entries. This ensures that different projects,
            # which may use the same sites, can be able to
            # use the same abbreviations in the main data table.
            # Could check again project title also but seems harder...
            dbhandle = uow.UploadToDatabase(
                self.mainDataAll, config, 'maintable',
                sitelist=self.sitelisttoadd,
                lter=self.cboxselectlter.currentText(),
                meta=self.metaurl)
        else:
            pass

        if sender == self.siteDialog.btnPush or\
           sender == self.mainDialog.btnPush:
            try:

                # Use the method with our database handler
                # to perform queries and checks given our
                # arguments; if returned TRUE
                # then procees to push the information to
                # the database.
                sitecheck = dbhandle.check_previous_sites()
                print(sitecheck)

                if (any(sitecheck) == True):
                    dbhandle.push_table_to_postgres()

                    QtGui.QMessageBox.about(
                        self, "Progress Box",
                        "The table information has now been" +
                        " uploaded to the database.")
                else:
                    # If False is returned than the data is likely
                    # already present based on the checks that were
                    # built into the UploadToDatabase class
                    self.w.showMessage(errormessage)
                    return

            except Exception as e:
                print(str(e))

        if sender == self.siteDialog.btnPush:
            self.siteDialog.close()
        elif sender == self.mainDialog.btnPush:
            self.mainDialog.close()

    #===========================#
    # Helper function to merge
    # queries from the database to
    # the raw data so that we can push to tables
    # deeper in the database schema
    #===========================#
    #=========HELPER========#
    def merge_main_to_taxa(self):
        try:
            required = self.sitecolumn
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                'Please make sure you have designated the column ' +
                'in the raw data table that contains site' +
                'abbreviations.')

        # Performing a unit of work to
        # to query the main table in the database
        session = config.Session()
        maintablequery = uow.MainTableQuery(
        ).go(session, config.maintable)
        session.close()

        # Initializing two empty list that will store the
        # results from the query
        projid = []
        siteid = []

        # Appending the list with query results
        for row in maintablequery:
            projid.append(row.projID)
            siteid.append(row.siteID)

        # Turning the list into a dataframe that will
        # be merged with the raw data
        tomergewithraw = pd.DataFrame(
            {'projID': projid,
             str(self.sitecolumn): siteid
             })

        # Merging the queried results with the raw data
        # that is loaded in the database. Note I am not
        # saving this to the program cause it will be
        # someone redundant
        rawmergedMain = pd.merge(
            tomergewithraw, self.rawdf,
            left_on=[str(self.sitecolumn)],
            right_on=[str(self.sitecolumn)])

        return rawmergedMain
    #===========================#
    # Method/Helper function to convert the user input strings into
    # a list.
    #===========================#
    #=========HELPER========#

    def convert_string_to_List(self, StrtoConvert):
        strTolist = re.sub(
            ",\s", " ", StrtoConvert.rstrip()).split()
        return strTolist

    #========================#
    # Method/ Helper function to convert an input string (user inputs)
    # to a list of  numeric values (decimal)
    #=========================#
    #=========HELPER========#
    def convert_string_to_decimal(
            self, ItemtoConvert, ItemType='Decimal'):
        # This is a function that substitutes commas followed by
        # a space (",\s") with only spaces (" ") and then splits
        # the string on those spaces to return a list where each
        # element is an individual number entered by the user
        strTolist = self.convert_string_to_List(ItemtoConvert)

        if ItemType == 'Decimal':

            # This is a list comprehension that takes the items
            # in the list and converts them to Decimal numbers
            strToNumeric = [dc.Decimal(x.strip(" ")) for x in strTolist]

        elif ItemType == 'Integer':
            strToNumeric = [int(x.strip(" ")) for x in strTolist]

        return strToNumeric

    #=======================#
    # Method to open a csv file that contain raw data
    #=======================#
    def open_file(self):

        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        print(name)
        try:
            self.rawdf = pd.read_csv(name)
            self.rawdfresetall = pd.DataFrame.copy(self.rawdf)

            rawmodel = ptb.PandasTableModel(self.rawdf)
            self.tblViewraw.setModel(rawmodel)
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "The file you have tried to open is a different" +
                " format that a csv. Please convert file to a" +
                " csv format and then load. TELL ANDREW TO MAKE THIS" +
                " 'file open action' more flexible...")
            return

    #=======================#
    # Method to prompt a message when exiting program through either
    # the exit menu button or through 'ctrl+q'
    #=======================#
    def quit_program(self):
        quitmsg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(
            self, 'Message', quitmsg,
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
