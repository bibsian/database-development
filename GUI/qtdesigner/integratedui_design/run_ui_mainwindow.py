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
import gc

import pandas as pd
from contextlib import contextmanager
import logging as log
import datetime as TM

# User Interfaces
import ui_mainwindow as mw
import ui_tabledialog as td
import ui_tablepreviewDB as tp
import ui_tablequery as tq
import class_columntodictframe as cdictframe
import class_database as uow
import config
import class_timeparse as tparse


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
# input by the user To View Certain information


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


#========================#
# Dialog pop up widget
#========================#

# Creating a Dialog box that will display the values that are
# input by the user and a query from the database with
# related informatoin


class DialogQuery(QtGui.QDialog, tq.Ui_Dialog):
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
        self.timeview = DialogPopUp()
        self.rawPreview = DialogPopUp()
        self.siteDialog = DialogPreview()
        self.mainDialog = DialogPreview()
        self.taxaDialog = DialogPreview()
        self.rawDialog = DialogPreview()

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
        self.btnTimeConcat.clicked.connect(self.time_concat)
        self.btnObsConcat.clicked.connect(self.covariate_concat)
        self.btnObsPreview.clicked.connect(self.obs_concat)
        
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
        self.lnedNullphrase.returnPressed.connect(self.null_handle)

        #======= SITE INFO =====#
        self.lnedViewSite.returnPressed.connect(self.col_view_handle)

        # Setting line edits for sit abbreivations, lat, long,
        # and descriptions to Disabled on start
        self.lnedSiteformsiteID.setDisabled(True)
        # site ID if No check box is checked
        self.lnedSiteformnock.setDisabled(True)
        # Lattitude
        self.lnedSiteformlat.setDisabled(True)
        # Longitude
        self.lnedSiteformlong.setDisabled(True)

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

        #============TIME INFO==========#
        self.timelnedlist = [
            self.lnedTempSchCol1, self.lnedTempSchCol2,
            self.lnedTempSchCol3]
        for i in self.timelnedlist:
            i.returnPressed.connect(self.time_format)

        #============OBS INFO=============#
        #====SPATIAL REPS====#
        self.lnedSpRep1.setDisabled(True)

        self.splnedlist = [
            self.lnedSpRep1, self.lnedSpRep2, self.lnedSpRep3,
            self.lnedSpRep4]

        for i,item in enumerate(self.splnedlist):
            item.returnPressed.connect(self.sp_obs_record)
            if i > 0:
                item.setEnabled(True)
            else:
                pass
            
        #======IND ID=========#
        self.lnedObsIndID.setDisabled(True)
        #======STRUCTURE=======#
        self.lnedObsStruct.setDisabled(True)

        self.optionallnedlist = [
            self.lnedObsIndID, self.lnedObsStruct]

        for i in self.optionallnedlist:
            i.returnPressed.connect(self.optional_obs_record)

            
        self.lnedObsData.returnPressed.connect(self.optional_obs_record)

        self.lnedCov.returnPressed.connect(self.covariate_concat)
        #=======================#
        # Catching CHECK BOX signals from user interface
        #=======================#
        self.ckSiteCoordN.stateChanged.connect(self.site_coord_options)
        self.ckSiteCoordY.stateChanged.connect(self.site_coord_options)

        # Assiging all the check boxes for the taxa table form
        # into a list

        #====TAXA DATA=====#
        self.taxackboxlist = [
            self.ckSppCode, self.ckKingdom, self.ckPhylum,
            self.ckClass, self.ckOrder, self.ckFamily,
            self.ckGenus, self.ckSpp]

        for i, item in enumerate(self.taxackboxlist):
            self.taxackboxlist[i].stateChanged.connect(
                self.multiple_check_box_behavior)

        #====SEASON DATA=====#
        self.seasonckboxlist = [
            self.ckSpringConvert, self.ckSummerConvert,
            self.ckFallConvert, self.ckWinterConvert]

        for i, item in enumerate(self.seasonckboxlist):
            self.seasonckboxlist[i].stateChanged.connect(
                self.multiple_check_box_behavior)

        #====TIME DATA=====#
        # List to facilitate parsing date informatoin
        self.timedatalist = []
        # COLUMN/BLOCK 1
        # Creating a list of check boxes that will aid in parsing
        # date time information. Col1 reference to the first block
        # of check boxes in the UI (could be up to 3)
        self.timecol1list = [
            self.ckCol1MDYcombo, self.ckCol1MYcombo, self.ckCol1DYcombo,
            self.ckCol1DMcombo, self.ckCol1Y, self.ckCol1M,
            self.ckCol1J, self.ckCol1D]
        # A corresponding dictionary for the 1st block of check
        # boxes
        self.timecol1dict = {
            0: 'dmy', 1: 'my', 2: 'dy', 3: 'dm', 4: 'y', 5: 'm',
            6: 'j', 7: 'd'}

        # COLUMN/BLOCK 2
        # Creating more list and check boxes for other blocks
        # in the UI
        self.timecol2list = [
            self.ckCol2MYcombo, self.ckCol2DYcombo,
            self.ckCol2DMcombo, self.ckCol2Y, self.ckCol2M,
            self.ckCol2J, self.ckCol2D]
        # Dictionary
        self.timecol2dict = {0: 'my', 1: 'dy', 2: 'dm', 3: 'y', 4: 'm',
                             5: 'j', 6: 'd'}

        # COLUMN/BLOCK 3
        self.timecol3list = [
            self.ckCol3MYcombo, self.ckCol3DYcombo,
            self.ckCol3DMcombo, self.ckCol3Y, self.ckCol3M,
            self.ckCol3J, self.ckCol3D]
        # Dictionary
        self.timecol3dict = {0: 'my', 1: 'dy', 2: 'dm', 3: 'y', 4: 'm',
                             5: 'j', 6: 'd'}

        # Connecting checkboxes to methods
        for i, item in enumerate(self.timecol1list):
            self.timecol1list[i].stateChanged.connect(
                self.time_indexing)
            if i <= len(self.timecol2dict) - 1:

                self.timecol2list[i].stateChanged.connect(
                    self.time_indexing)
                self.timecol3list[i].stateChanged.connect(
                    self.time_indexing)
            else:
                pass

        #=======OPTIONAL OBS DATA========#
        self.optionalobscklist = [
            self.ckObsIndIDY, self.ckObsStructY, self.ckObsIndIDN,
            self.ckObsStructN]

        for i, item in enumerate(self.optionalobscklist):
            item.stateChanged.connect(self.optional_obs_record)

        #======================#
        # Catching the site COMBO BOX text
        #======================#
        self.cboxSiteCount.activated.connect(self.get_sitebox)
        self.cboxselectlter.activated.connect(self.meta_data_check)

        #========================#
        # Pooling radio buttons
        #========================#
        self.rbtnlist = [
            self.rbtnMYnull, self.rbtnDYnull, self.rbtnDMnull,
            self.rbtnYnull, self.rbtnMnull, self.rbtnMnull,
            self.rbtnAllpresent]

        #=====================#
        # Connecting user defined
        # signal
        #=====================#

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
    # METHOD to handle the conversion of
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
            self.lnedNulltext.clear()

        elif sender == self.lnedNullphrase:
            self.nullphraseinput = self.lnedNullphrase.text()

            try:
                textnullinputlist = self.convert_phrases_to_List(
                    self.nullphraseinput)
                print(textnullinputlist)
                for i in textnullinputlist:
                    for j in self.rawdf.columns:
                        self.rawdf[j].replace(i, 'NULL', inplace=True)

            except Except as e:
                print(str(e))

            message = InputReceived()
            message.show()
            self.lnedNullphrase.clear()
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
        self.rawdf = pd.DataFrame.copy(self.rawdfresetall)
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

                try:
                    session = config.Session()
                    query = uow.SiteTableQuery().go(
                        session, config.sitetable)
                    if len(query) == 0:
                        querydf = pd.DataFrame()
                    else:
                        querydf = pd.DataFrame(query).iloc[:, 1:]
                        for i, item in enumerate(['lat', 'long']):
                            querydf[item] = querydf[item].astype(float)
                        print(querydf.dtypes)

                except Exception as e:
                    print(str(e))
                    return

                # If quality control passes, instantiate the popup
                # dialog box that will display the derived informatoin
                self.colView = DialogQuery()

                # Creating the table model to view the subsetted
                # values in dataframe form with qttableview
                self.collistmodel = ptbE.PandasTableModel(collistdf)
                self.querytablemodel = ptb.PandasTableModel(
                    querydf)

                # Settting the data Model to view through the
                # dialog box from UniqueColumnList
                self.colView.tblList.setModel(self.collistmodel)
                self.colView.queryTable.setModel(
                    self.querytablemodel)
                self.colView.show()

                self.colView.btnboxOk.accepted.connect(
                    self.colView.accept)

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
        if [x.lower() for x in self.siteIDrecord_re].sort() == [
                y.lower() for y in self.sitelisttoadd].sort() and len(
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

        self.siteDataAllmodel = ptbE.PandasTableModel(self.siteDataAll)
        self.siteDialog.tblList.setModel(self.siteDataAllmodel)
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
                        'structured': 'NULL',
                        'startyr': self.startyr,
                        'endyr': self.endyr,
                        'samplefreq': submain['temp_int'],
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
                        'structured','startyr', 'endyr', 'samplefreq',
                        'totalobs','studytype', 'community', 'siteID',
                        'sp_rep1_ext','sp_rep2_ext', 'sp_rep3_ext',
                        'sp_rep4_ext','metalink', 'knbID'])
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
                    'totalobs', 'sp_rep1_ext',
                    'sp_rep2_ext', 'sp_rep3_ext', 'sp_rep4_ext']

                for i in convertcolumns:
                    self.mainDataAll[i] = pd.to_numeric(
                        self.mainDataAll[i], errors='coerce')

                totalobslist = []
                # This step is depedent on accurate information
                # provided from the siteView/ sitelisttoadd
                # attribute
                for i in range(len(self.sitelisttoadd)):
                    self.mainDataAll.loc[i, 'siteID']\
                        = self.sitelisttoadd[i]
                    totalobslist.append(
                        len(
                            self.rawdf[
                                self.rawdf[self.sitecolumn] ==
                                self.sitelisttoadd[i]]))
                    self.mainDataAll.loc[i, 'totalobs']\
                        = totalobslist[i]

                print(totalobslist)
                print(sum(totalobslist))
                print(len(self.rawdf))

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
        except Exception as e:
            print(str())
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
        pass
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
    #---SPECIAL---VARIABLE---TAXADATAALL--#
    #--SPECIAL--VARIABLE---TAXAPROJCTCURRENT--#
    def taxa_concat(self):

        try:
            if len(self.taxatextdict.values()) == 0:
                raise ValueError
            else:
                pass
            print('Testing Taxa Concatenate')

        except Exception as e:
            print(str(e))
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                'Make sure that you have designated the column  ' +
                'header in the raw data that contains the ' +
                'information about site abbreviations.')
            return
        try:
            # Using a helper function to use the taxa dictionary
            # and extra information from the raw dataframe
            # that is current up to this form (taxa form)
            taxadataraw = self.data_list(
                ['projID'], self.merge_tables('main_taxa'))
            print(taxadataraw)
            # Created a list of column names for the taxa table
            # as it is in the data base and it
            # is hard coded because it doesn't change
            taxadfcol = [
                'projID', 'sppcode', 'kingdom', 'phylum', 'class',
                'order', 'family', 'genus', 'species', 'authority']

            # Extracting the keys from the taxa dictionary
            # Which will help index which columns we already
            # have information for
            taxadictcolindex = list(self.taxatextdict.keys())

            # Adding 1 to each above indeces to acccount
            # for the fact that the taxa text dicationary
            # does not include informatoin about the projID
            # and hence throws the index information off by 1
            # if you wanted a 1:1 correspondence to names
            taxadictcolindex = [x + 1 for x in taxadictcolindex]

            # Extracting the values (names) from the taxa text
            # dictionary
            taxadictcol = list(self.taxatextdict.values())

            # Extracting the column names from the raw taxa
            # data that was created with our helper function
            # NOTE: These column names are NOT what is
            # present in the database and they MUST be changed
            self.taxacurrentcol = list(taxadataraw.columns)

            # Using the true column names and the index
            # from the taxa dictionary to replace the
            # raw column names with the true one
            self.taxacolumns = [taxadfcol[i] for i in taxadictcolindex]
            # Inserting the projID column into the taxa column list
            self.taxacolumns.insert(0, 'projID')

            # Reseting the raw taxa column names with matching
            # ones from the database
            taxadataraw.columns = self.taxacolumns

            print(taxadataraw.columns)
            #=============#
            # Finding what data are missing in the raw taxa
            # info by comparing the list of the true column names
            # with the raw taxa data column names and looking for
            # mismatches
            #==============#
            rawtaxacolset = set(self.taxacolumns)
            missingcollist = [
                x for x in taxadfcol if x not in rawtaxacolset]

            print(missingcollist)
            print(len(taxadataraw))

            #=============#
            # Creating a data frame of NULL values for information
            # that is missing from the raw taxa table
            # Note: this is a data frame with 1 row
            #=============#
            taxanulldf = self.produce_null_df(
                len(missingcollist), missingcollist,
                len(taxadataraw), 'NULL ')

            print(taxanulldf)

            # Merging the raw taxa data with missing data
            self.taxaDataAll = pd.concat(
                [taxadataraw.reset_index(drop=True),
                 taxanulldf.reset_index(drop=True)], axis=1)

            print(self.taxaDataAll)
            self.taxaprojcurrent = list(
                set(self.taxaDataAll['projID']))

            # Setting the model view for the taxa table
            self.taxamodel = ptbE.PandasTableModel(self.taxaDataAll)

            self.taxaDialog.tblList.setModel(self.taxamodel)
            self.taxaDialog.show()

            # Connecting the push database button to method
            self.taxaDialog.btnPush.clicked.connect(
                self.upload_to_database)

        except Exception as e:
            print(str(e))
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
    # Method to aid in parsing the time
    # information: Deals with what
    # check boxes have been clicked or not
    # And creates a list with an index specific
    # to a type of date format
    #=====================#
    def time_indexing(self):

        deldata = [0, 1, 2]
        # Creating list that will house the index
        # regarding the format of the raw date information
        self.timeactivated1 = []
        self.timeactivated2 = []
        self.timeactivated3 = []

        self.timeactivatedall = [
            self.timeactivated1, self.timeactivated2,
            self.timeactivated3]

        # Iterating over the list of of checked boxes
        # regarding the date format to retrieve an index
        # for the time dictionaries to use with our
        # TimeParser class (will be an argument for the class)

        # Note, there is a separate dictionary for each of the
        # blocks of check boxes on the time parser form. The if
        # statement makes sure that the iterator does not
        # index a number that does not exist (as the col2 and col3
        # time format dictionaries are smaller that col1 time dict)

        # The timeactivated list are appended with the index
        # of the checkbox from out time check box lists
        # ('timecol1list, timecol2list, timecol3list')
        for i, item in enumerate(self.timecol1list):
            if self.timecol1list[i].isChecked():
                self.timeactivated1.append(i)
            if i <= len(self.timecol2list) - 1:
                if self.timecol2list[i].isChecked():
                    self.timeactivated2.append(i)

                if self.timecol3list[i].isChecked():
                    self.timeactivated3.append(i)
            else:
                pass

        # This is a list that will be used to pop information
        # in case the user wants to re-edit the form because
        # they made an error.
        popdata = []

        # This nested loop iterates over the elements
        # of our timeactivated list created above
        # and appends the popdata list to inform the program
        # which data associated with each should be stored
        # still and not removed
        for i, item in enumerate(self.timeactivatedall):
            for j in range(len(self.timeactivatedall[i])):
                popdata.append(i)
        # The missing list comprehension indexs which data
        # associated with a block should be deleted from
        # our overall time data gathered
        missing = [x for x in deldata if x not in popdata]

        try:
            # Deleting data that should be because the user unchecked
            # a box and wants to re-enter informatoin
            for i in missing:
                del self.timedatalist[i]
            else:
                pass
        except:
            print('Data not set')
        finally:
            # This last part of the indexing block is
            # to aid in keeping track of  which line edits are
            # Enabled or disabled based on user inputs and
            # currently checked boxes

            print(self.timedatalist)
            try:
                # Inspecting each block to determine what is checked
                block1 = [x.isChecked() for x in self.timecol1list]
                block2 = [x.isChecked() for x in self.timecol2list]
                block3 = [x.isChecked() for x in self.timecol3list]

                # if any block is completely unchecked (any(block1))
                # then reactivate the line edit. Line edits
                # are deactivate in the time_concat method
                # after a user inputs information and it has been
                # accepting into memory
                reactivate = [
                    any(block1) == False, any(block2) == False,
                    any(block3) == False]

                # This is the loop to reactivate
                for i, item in enumerate(reactivate):
                    print("went into the reactivate loop")
                    if item is True:
                        self.timelnedlist[i].setEnabled(True)
                    else:
                        pass

                # Print the list of booleans regarding reactivating
                print(reactivate)
            except:
                print('Already enabled')

    #=====================#
    # Method that helps to format
    # date time informatoin
    # once it has been parsed
    #=====================#
    # NOTE, could probably shorten with a loop but
    # not going to focus on that now.
    def time_format(self):
        self.w = QtGui.QErrorMessage()

        timeformatedcolumns = ['year', 'month', 'day']
        # Checking if requried informatoin is present in the
        # program; if not then throw message
        try:
            required = self.rawdf
        except:
            self.w.showMessage(
                "Must upload raw data table before proceeding")
            return

        # Identifying the sender
        sender = self.sender()
        # Generic error message for the set of line edits associated
        # with this form
        columnerr = (
            " The column name you specified is incorrect.")
        checkerr = (
            "More than one checkbox has been selected. Please " +
            "correct this.")

        # Identifying which linedit is the
        # sending a signal to catch. Has the extra condition
        # that the number of boxes checked in each block
        # should be one.
        if sender == self.lnedTempSchCol1 and\
           len(self.timeactivated1) == 1:
            # Attempting to parse the time infomratoin based
            # on the checked boxes in the first block on the
            # time parser form and the line edit input
            try:
                # Uses TimeParser class
                timedatac1 = tparse.TimeParser(
                    self.rawdf, self.lnedTempSchCol1.text(),
                    self.timecol1dict, self.timeactivated1[0]).go()
                print(type(timedatac1))
                print(timedatac1.columns)

            except Exception as e:
                print(str(e))
                print('Always going to go to error block')

            finally:
                if type(timedatac1) is pd.DataFrame:
                    print(type(timedatac1))
                    self.timedatalist.append(timedatac1)
                    updatemess = InputReceived()
                    self.lnedTempSchCol1.clear()
                    self.lnedTempSchCol1.setDisabled(True)

                else:
                    self.w.showMessage(columnerr)
                    return

        elif sender == self.lnedTempSchCol2 and\
                len(self.timeactivated2) == 1:
            # Attempting to parse the time infomratoin based
            # on the checked boxes in the second block on the
            # time parser form and the line edit input
            try:
                # Uses TimeParser class
                timedatac2 = tparse.TimeParser(
                    self.rawdf, self.lnedTempSchCol2.text(),
                    self.timecol2dict, self.timeactivated2[0]).go()
                print(timedatac2.columns)
            except Exception as e:
                print(str(e))

            finally:
                if type(timedatac2) is pd.DataFrame:
                    self.timedatalist.append(timedatac2)
                    updatemess = InputReceived()
                    self.lnedTempSchCol2.clear()
                    self.lnedTempSchCol2.setDisabled(True)
                else:
                    self.w.showMessage(columnerr)
                    return

        elif sender == self.lnedTempSchCol3 and\
                len(self.timeactivated3) == 1:
            # Attempting to parse the time infomratoin based
            # on the checked boxes in the third block on the
            # time parser form and the line edit input
            try:
                # Uses TimeParser class
                timedatac3 = tparse.TimeParser(
                    self.rawdf, self.lnedTempSchCol3.text(),
                    self.timecol3dict, self.timeactivated3[0]).go()
                print(timedatac3.columns)

            except Exception as e:
                print(str(e))

            finally:
                if type(timedatac3) is pd.DataFrame:
                    self.timedatalist.append(timedatac3)
                    updatemess = InputReceived()
                    self.lnedTempSchCol3.clear()
                    self.lnedTempSchCol3.setDisabled(True)
                else:
                    self.w.showMessage(columnerr)
                    return
        else:
            self.w.showMessage(checkerr)

    #======================#
    # Method to concatenate the temporal
    # information provided above and additionally
    # use the information gained from our radio buttons
    # on the Time Parser Form
    #======================#
    def time_concat(self):

        self.alltimedata = None
        # A series of conditional statments that will direct the
        # concatenation and/or creation of the final formated
        # date time informatoin

        # Condition 1: If our data frame list corresponding to each
        # block in the time parser form is 1 AND the All present
        # radio button is checked then, this is our data information
        # already formated; save it and return
        print("start")
        if len(self.timedatalist) == 1 and\
           self.rbtnAllpresent.isChecked():
            print("List length 1, All present CHEKCED")
            self.alltimedata = self.timedatalist[0]

            print(self.alltimedata)
            print(self.alltimedata.dtypes)
            print("Exit list length 1, all present CHECKED")

        # Condition 2: If our data frame list corresponding to each
        # block in the time parser form is 1 AND the All present
        # radio button is NOT checked then look at which
        # informatoin is missing (must be 2 time components)
        # and make Null values for them
        elif len(self.timedatalist) == 1 and\
                (not self.rbtnAllpresent.isChecked()):
            print("List length 1, All present NOT CHECKED")

            # Day/Month Null
            if self.rbtnDMnull.isChecked():
                print("List length 1, D/M NULL ")
                self.alltimedata = pd.concat(
                    [
                        self.timedatalist[0],
                        self.produce_null_df(
                            2, ['day', 'month'],
                            len(self.timedatalist[0]), 'nan ')],
                    axis=1)
                print(self.alltimedata)
                print("Exit List length 1, D/M NULL")

            # Day/Year Null
            elif self.rbtnDYnull.isChecked():
                print("List length 1, D/Y Null")
                self.alltimedata = pd.concat(
                    [
                        self.timedatalist[0],
                        self.produce_null_df(
                            2, ['day', 'year'],
                            len(self.timedatalist[0]), 'nan ')],
                    axis=1)
                print(self.alltimedata)
                print("Exit List length 1, D/Y Null")

            # Month/Year Null
            elif self.rbtnMYnull.isChecked():
                print("List length 1, M/Y Null")
                self.alltimedata = pd.concat(
                    [
                        self.timedatalist[0],
                        self.produce_null_df(
                            2, ['month', 'year'],
                            len(self.timedatalist[0]), 'nan ')],
                    axis=1)
                print(self.alltimedata)
                print("Exit List length 1, M/Y Null")

            else:
                print("Passing List Length 1 block")
                pass

        # Condition 3: If our 'data frame' list corresponding to each
        # block in the time parser form is length 2
        # Go into this block
        elif len(self.timedatalist) == 2:
            print("List Length 2 block")
            self.alltimedata = pd.concat(
                [self.timedatalist[0], self.timedatalist[1]], axis=1)
            self.alltimecolumns = list(self.alltimedata.columns)

            print("List Length 2, above jd/y")
            # Check if julian date and year were in separte
            # data frames of our 'data frame' list if so
            # combind and parse time once more.
            if ('julianday' in self.alltimecolumns) == True and\
               ('year' in self.alltimecolumns) == True:

                print("This should only appear under special cases")
                self.alltimedata['cbind'] = self.alltimedata[
                    self.alltimecolumns[0]].astype(str).map(str) +\
                    "-" + self.alltimedata[self.alltimecolumns[1]].astype(str)

                self.alltimedata = tparse.TimeParser(
                    self.alltimedata, 'cbind', self.timecol1dict, 0).go()

                print(self.alltimedata)
                print(self.alltimedata.dtypes)
                print("Exiting jd/y formating")

            # If no julian date or year are present then
            # add columns of null values for missing infomraion
            else:
                print("In list length 2, past jd")
                # No missing information means concatenate
                # dataset
                if len(self.timedatalist) == 2 and\
                   self.rbtnAllpresent.isChecked():
                    print("In list length 2, All present block")

                    self.alltimedata = pd.concat(
                        [self.timedatalist[0], self.timedatalist[1]],
                        axis=1)

                    print(self.alltimedata)
                    print(self.alltimedata.dtypes)
                    print("Exiting list length 2, All present block")

                # Missing Year data
                elif self.rbtnYnull.isChecked():
                    print("List lenght 2, In Year Null block")
                    self.alltimedata = pd.concat(
                        [
                            self.timedatalist[0], self.timedatalist[1],
                            self.produce_null_df(
                                1, ['year'],
                                len(self.timedatalist[0]), 'nan ')],
                        axis=1)
                    print(self.alltimedata.dtypes)
                    print("Exiting list length 2,Year Null block")

                # Missing Month data
                elif self.rbtnMnull.isChecked():
                    print("List lenght 2, In Month Null block")
                    self.alltimedata = pd.concat(
                        [
                            self.timedatalist[0], self.timedatalist[1],
                            self.produce_null_df(
                                1, ['month'],
                                len(self.timedatalist[0]), 'nan ')],
                        axis=1)
                    print(self.alltimedata.dtypes)
                    print("Exiting list lenght 2, In Month Null block")

                # Missing Day data
                elif self.rbtnDnull.isChecked():
                    print("List lenght 2, Day Null block")
                    self.alltimedata = pd.concat(
                        [
                            self.timedatalist[0], self.timedatalist[1],
                            self.produce_null_df(
                                1, ['day'],
                                len(self.timedatalist[0]), 'nan ')],
                        axis=1)
                    print(self.alltimedata.dtypes)
                    print("Exiting list lenght 2, Day Null block")

                else:
                    print("Passing List length 2 block")
                    pass
            print()

        # Condition 3: If our 'data frame' list is length 3
        # then we just need to concatenate the informatoin
        # and save it in the program
        elif len(self.timedatalist) == 3 and\
                self.rbtnAllpresent.isChecked():
            print("In List length 3 data frame block")
            self.alltimedata = pd.concat(
                [self.timedatalist[0], self.timedatalist[1],
                 self.timedatalist[2]], axis=1)
            print(self.alltimedata)
        else:

            pass

        # Try and display the supposedly save information
        # from above; if a data frame with all time informatoin
        # could not be concatenated then there was likely a user
        # input error and they checked the wrong information
        # of put in the wrong type of columns etc.
        try:
            print('Tryin to make the model view')

            copy = self.alltimedata.copy()
            copy['day'] = copy['day'].astype(str)

            print(copy)
            print(copy.dtypes)

            timemodel = ptbE.PandasTableModel(copy)
            self.timeview.tblList.setModel(timemodel)
            self.timeview.show()

        except Exception as e:
            print(str(e))
            self.w.showMessage(
                "Information does not compute please double" +
                " check your inputs and NULL buttons.")

    def sp_obs_record(self):
        sender = self.sender()

        # Making list comprehesions to extra text
        # from line edits, identify sender of signals, and
        # get a length of characters on the text
        self.spinfolist = [x.text() for x in self.splnedlist]
        self.spinfoboolist = [x == sender for x in self.splnedlist]
        self.spinfolen = [len(x.text()) for x in self.splnedlist]
        self.spinfolabel = [
            'spt_rep1', 'spt_rep2', 'spt_rep3', 'spt_rep4']
        # Required that raw df is loaded into the program
        try:
            self.obsdf = self.rawdf[self.sitecolumn]
        # Throw exception if not loaded
        except Exception as e:
            print(str(e))
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                " Make sure the location of site ID information " +
                "has been specified on the Site Form.")
            return

        # If a signal is sent from a line edit then try
        # to subset that column from the rawdf
        try:
            [print(self.rawdf[x]) for x, y in zip(
                self.spinfolist, self.spinfoboolist) if y == True]

        # If the rawdf is not subsetable then throw errormessag
        # to reenter user input
        except Exception as e:
            print(str(e))
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(" Column not available; try again.")
            return

        # Column names for subsetted data frame
        self.obsrename = ['spt_rep1']
        # Iterate over the list containing the identified
        # columns and concatenate them together using
        # the siteID column as the base
        for i, item in enumerate(self.spinfolen):
            if item > 0:
                self.obsdf = pd.concat(
                    [self.obsdf, self.rawdf[self.spinfolist[i]]],
                    axis=1)
                self.obsrename.append(self.spinfolabel[i])
            else:
                pass

    def optional_obs_record(self):
        sender = self.sender()

        print(sender)
        optionallnedlisttext = [x.text() for x in self.optionallnedlist]
        optionallnedbool = [x == sender for x in self.optionallnedlist]
        optionallnedlab = ['indivID', 'structure']
        # Check Box and linedit behavior
        # managed with a list comprehension connection
        # the list of checkboxes (Yes or No) with
        # the line edits
        [x.setEnabled(True) if y.isChecked()
         else x.setEnabled(False) for x, y in
         zip(self.optionallnedlist, self.optionalobscklist)]

        # If a signal is sent from a line edit then try
        # to subset that column from the rawdf
        try:
            self.obsoptdf = self.obsdf
            self.obsoptrename = list(self.obsrename)
            [print(self.rawdf[x]) for x, y in zip(
                optionallnedlisttext,
                optionallnedbool) if y == True]

            # Iterate over the list containing the identified
            # columns and concatenate them together using
            # the siteID column as the base
            for i, item in enumerate(optionallnedlisttext):
                if len(item) > 0:
                    self.obsoptdf = pd.concat(
                        [self.obsoptdf, self.rawdf[item]],
                        axis=1)
                    self.obsoptrename.append(optionallnedlab[i])
            else:
                pass

        # If the rawdf is not subsetable then throw errormessag
        # to reenter user input
        except Exception as e:
            print(str(e))
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(" Column not available; try again.")
            return

        if sender == self.lnedObsData or sender == self.btnObsPreview:
            rawdatacol = self.lnedObsData.text()
            try:
                self.obsoptdf = pd.concat(
                    [self.obsoptdf, self.rawdf[rawdatacol]],
                    axis=1)
                self.obsoptrename.append('unitobs')
                print("We're in the optional Block")
                print(self.obsoptdf)

            except Exception as e:
                print(str(e))
                self.w = QtGui.QErrorMessage()
                self.w.showMessage(" Column not available; try again.")
                return

    def obs_concat(self):

        try:
            if self.alltimedata is None:
                raise ValueError
            else:
                pass
        except Exception as e:
            print(str(e))
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "Be sure you have completed the Time Parser Form.")
            return

        self.sp_obs_record()
        self.optional_obs_record()
        print("In concatenate block")
        print(self.obsoptdf)
        
        # These are the column names that need to be present
        # to push to the database
        self.obstruecol = [
            'spt_rep1', 'spt_rep2', 'spt_rep3', 'spt_rep4',
            'structure', 'indivID', 'unitobs']
        self.obsoptdf.columns = self.obsoptrename

        # Checking the missing columns
        missing = [
            x for x in self.obstruecol if x not in self.obsoptrename]
        print(missing)

        # Creating the null dataframe
        nulldf = self.produce_null_df(
            len(missing), missing, len(self.obsoptdf), 'NULL ')

        
        if len(missing) > 0:
            self.obsall = pd.concat(
                [self.obsoptdf, nulldf, self.alltimedata,
                 ], axis=1)
        else:
            self.obsall = pd.concat(
                [self.obsoptdf, self.alltimedata,
                 ], axis=1)

        rawmerged = self.merge_tables('taxa_raw')
        self.futureprojID = list(set(rawmerged['projID']))
        self.futuretaxaID = list(set(rawmerged['taxaID']))

        self.obsall = pd.concat(
            [self.obsall, rawmerged[['projID', 'taxaID']]], axis=1)

        self.obsall['unitobs'] = pd.to_numeric(
            self.obsall['unitobs'], errors='coerce')

        self.obsmodel = ptbE.PandasTableModel(self.obsall) 
        self.rawPreview.tblList.setModel(self.obsmodel)
        self.rawPreview.show()

        

    def covariate_concat(self):
        sender = self.sender()
        try:
            collist = self.convert_string_to_List(self.lnedCov.text())
            self.rawdf[collist]

        except Exception as e:
            print(str(e))
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                "Column Not Present in data; please re-enter list.")
            return

        if sender == self.lnedCov:
            
            self.covdata = cdictframe.ColumnToDictionaryFrame(
                self.rawdf, collist).dict_df()

            self.rawalldata = pd.concat(
                [self.obsall, self.covdata], axis=1)

        else:
            pass
        
        if sender == self.btnObsConcat:
            
            self.rawallmodel = ptbE.PandasTableModel(self.rawalldata)
            self.rawDialog.tblList.setModel(self.rawallmodel)
            self.rawDialog.show()

            self.rawDialog.btnPush.clicked.connect(
                self.upload_to_database)
        else:
            pass

    
    #========================#
    # This is a hleper method to create a dataframe of
    # null values based on inputs about the number of columns
    # names of columns, and length of values (n)
    #=========================#
    #=========HELPER==========#

    def produce_null_df(self, ncols, names, length, input):

        # Test regarding input types
        try:
            if (type(names) is list) == True and\
                    (type(ncols) is int) == True:
                pass
        except:
            raise TypeError
            return

        # Create a NULL dataframe based on the length provided
        # Make the number of columns necessary
        # piece together along axis 1
        allnulls = pd.concat(
            [
                pd.DataFrame(re.sub(" ", " ", (str(input) * length))
                             .split())] * len(names), axis=1)
        # Rename columns
        allnulls.columns = names

        # Return objects
        return allnulls

    #=====================#
    # This is a helper method that takes two inputs
    # an 'extracolumns' variable which is supposed
    # to be a column from a dataframe AND inputdata
    # which is a dataframe where the extracolumns
    # column exists.
    #======================#
    #=========HELPER========#
    #--SPECIAL--VALUE--DEPENDENCY--SITELISTTOADD--#

    # Could make text all lower case before appending data...
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
                pd.DataFrame(
                    self.siteDataAllmodel.data(
                        index=None, role=QtCore.Qt.UserRole),
                    columns=self.siteDataAll.columns),
                config, 'sitetable',
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
                pd.DataFrame(
                    self.mainDataAllModel.data(
                        index=None, role=QtCore.Qt.UserRole),
                    columns=self.mainDataAll.columns),
                config, 'maintable',
                sitelist=self.sitelisttoadd,
                lter=self.cboxselectlter.currentText(),
                meta=self.metaurl)

        elif sender == self.taxaDialog.btnPush:
            # This handle only checks the project ID's from
            # the taxonomic table.
            dbhandle = uow.UploadToDatabase(
                pd.DataFrame(
                    self.taxamodel.data(
                        index=None, role=QtCore.Qt.UserRole),
                    columns=self.taxaDataAll.columns),
                config, 'taxatable',
                taxaprojIDlist=self.taxaprojcurrent)

        elif sender == self.rawDialog.btnPush:
            # This handle chekcs for taxaID and projID
            dbhandle = uow.UploadToDatabase(
                pd.DataFrame(
                    self.obsmodel.data(
                        index=None, role=QtCore.Qt.UserRole),
                    columns=self.obsall.columns),
                config, 'rawtable',
                rawprojID=self.futureprojID,
                rawtaxaID=self.futuretaxaID)

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

                if (all(sitecheck) == True):
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

        if sender == self.taxaDialog.btnPush:
            try:
                # Use the modules in class_database.py
                # to return a test best on our inputs
                # to the dbhandle
                taxacheck = dbhandle.check_previous_taxa()
                print(taxacheck)

                # If the booleans in our list returned
                # are true then push to database
                if (all(taxacheck)) == True:

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

        elif sender == self.rawDialog.btnPush:
            try:
                # Use the modules in class_database.py
                # to return a test best on our inputs
                # to the dbhandle
                rawcheck = dbhandle.check_previous_rawobs()
                print(rawcheck)

                # If the booleans in our list returned
                # are true then push to database
                if (all(rawcheck)) == True:

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
        elif sender == self.taxaDialog.btnPush:
            self.taxaDialog.close()
        elif sender == self.rawDialog.btnPush:
            self.rawDialog.close()

    #===========================#
    # Helper function to merge
    # queries from the database to
    # the raw data so that we can push to tables
    # deeper in the database schema
    #===========================#
    #=========HELPER========#
    def merge_tables(self, tablename):
        try:
            required = self.sitecolumn
        except:
            self.w = QtGui.QErrorMessage()
            self.w.showMessage(
                'Please make sure you have designated the column ' +
                'in the raw data table that contains site' +
                'abbreviations.')

        # Initializing two empty list that will store the
        # results from the query
        projidmain = []
        projidtaxa = []
        siteid = []
        taxaid = []
        taxacolumnkey = []

        # Performing a unit of work to
        # to query the main table in the database
        session = config.Session()
        query = uow.MainTableQuery(
        ).go(session, config.maintable)
        session.close()

        # Appending the list with query results
        for row in query:
            projidmain.append(row.projID)
            siteid.append(row.siteID)

        # Turning the list into a dataframe that will
        # be merged with the raw data
        self.tomergewithraw = pd.DataFrame(
            {'projID': projidmain,
             str(self.sitecolumn): siteid
             })

        if tablename == 'main_taxa':

            # Merging the queried results with the raw data
            # that is loaded in the database. Note I am not
            # saving this to the program cause it will be
            # someone redundant
            rawmergedMain = pd.merge(
                self.tomergewithraw, self.rawdf,
                left_on=[str(self.sitecolumn)],
                right_on=[str(self.sitecolumn)])

            return rawmergedMain

        if tablename == 'taxa_raw':
                        # Performing a unit of work to
            # to query the main table in the database
            session = config.Session()
            query = uow.TaxaTableQuery(
            ).go(session, config.taxatable)
            session.close()

            # Appending the list with query results
            for row in query:
                projidtaxa.append(row.projID)
                taxaid.append(row.taxaID)
                taxacolumnkey.append(
                    eval('row.' + self.taxacolumns[1]))

            # Turning the list into a dataframe that will
            # be merged with the raw data
            taxamergewithraw = pd.DataFrame(
                {'taxaID': taxaid,
                 'projID': projidtaxa,
                 str(self.taxacolumns[1]): taxacolumnkey
                 })

            finalmerge = pd.merge(
                self.tomergewithraw, taxamergewithraw,
                left_on=['projID'], right_on=['projID'])

            # Merging the queried results with the raw data
            # that is loaded in the database. Note I am not
            # saving this to the program cause it will be
            # someone redundant
            rawmerged = pd.merge(
                finalmerge, self.rawdf,
                left_on=[
                    str(self.sitecolumn), str(self.taxacolumns[1])],
                right_on=[
                    str(self.sitecolumn), str(self.taxatextdict[0])])

            return rawmerged

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

    #============================#
    # Method to convert a string of phrases
    # into a list of phrases
    #=========HELPER===========#
    def convert_phrases_to_List(self, StrtoConvert):
        strTolist = re.sub(
            "^,\s$", " ", StrtoConvert.rstrip()).split(",")

        return strTolist
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
