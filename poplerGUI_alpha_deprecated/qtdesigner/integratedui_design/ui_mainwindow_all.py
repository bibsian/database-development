#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import ui_mainwindow as ui

#=========================#
# User interface
#=========================#

# Creating the subclass that inherits from the Ui_MainWindow
# object i.e. our user interface
# and the user interface module we created (ui_mainwindow)


class UiMainWindow (QtGui.QMainWindow, mw.Ui_MainWindow):
    '''
    This class displays the user interface that was created with
    QtDesigner. 

    We're multiply inheriting the user interface and it's
    behavior.
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
        self.siteDialog = DialogPreview()
        self.mainDialog = DialogPreview()
        self.taxaDialog = DialogPreview()
        self.rawDialog = DialogPreview()
        self.siteDBView = DialogPreview()
        
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
        # Create a column for taxonomic information
    
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
        self.btnObsConcat.clicked.connect(self.obs_concat)

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

        for i in self.splnedlist:
            i.returnPressed.connect(self.sp_obs_record)

        
        #======IND ID=========#
        self.lnedObsIndID.setDisabled(True)
        #======STRUCTURE=======#
        self.lnedObsStruct.setDisabled(True)

        self.optionallnedlist = [
            self.lnedObsIndID, self.lnedObsStruct]

        for i in self.optionallnedlist:
            i.returnPressed.connect(self.optional_obs_record)

        self.lnedObsData.returnPressed.connect(self.optional_obs_record)

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

        # =====================#
        # Connecting user defined
        # signal
        # =====================#
        
        
        #======================#
        # Creating DATA MODELS to view pandas dataframes on
        # in qttreeView
        #======================#
        # Setting the metadata model data to mirrow what is in our
        # file titled meta_file_test.csv
        metamodel = ptb.PandasTableModel(self.metadf)
        self.tblViewmeta.setModel(metamodel)

