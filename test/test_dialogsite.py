#!/usr/bin/env python
import pytest
import pytestqt
import pandas as pd
from PyQt4 import QtGui, QtCore
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_logic_session as logicsess
import class_userfacade as face
import class_inputhandler as ini
import class_helpers as hlp
import ui_dialog_site as dsite
import ui_mainrefactor as mw
import class_modelviewpandas as view
import config as orm

@pytest.fixture
def MainWindow():
    class SiteDialog(QtGui.QDialog, dsite.Ui_Dialog):
        
        changed_data = QtCore.pyqtSignal(object)
        site_unlocks = QtCore.pyqtSignal(object)
        
        def __init__(self,  parent=None):
            super().__init__(parent)
            self.setupUi(self)

            # Placeholders
            # user input for dialog box
            # logging class
            self.siteini = None
            self._log = None

            # Placeholders:
            # Site Table from Raw data
            # and Site Table after edits
            self.rawdata = None
            self.rawdataog = None
            self.sitetabledata = None

            # Placeholders:
            # Queried Site Table from database
            # List of site factor levels that are present in database
            # Orms to populate Site Table information into database
            self.sitedbtable = None
            self.queryupdate = None

            # Place holder for sqlalchemy Orms
            self.siteorms = {}
            
            # Viewer Classes (editable and not)
            self.viewEdit = view.PandasTableModelEdit
            self.view = view.PandasTableModel

            # Placeholders for data model classes for viewers:
            # Original data model
            # Database query model
            # Data model if updated from query
            self.sitetablemodel = None
            self.sitedbtablemodel = None
            self.sitequerymodel = None
            
            #  Updated site factor level list
            self.sitemodlist = None

            # User facade composed from main window
            self.facade = None

            # Table Director to build site table from
            # Builder classes
            self.sitedirector = None
            self.siteloc = {'siteid': None}

            # Status Message
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox

            # Signals and slots
            self.btnSiteID.clicked.connect(self.site_handler)
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnSkip.clicked.connect(self.close)
            self.btnQuery.clicked.connect(self.query_database)

        def site_handler(self):
            ''' 
            Method to take user input from line edit and
            wrap it with a InputHandler. Then send 
            the wrapped object to the Main Window.
            '''
            lned = {'siteid': self.lnedSiteID.text().strip()}
            self.siteloc['siteid'] = self.lnedSiteID.text().strip()            
            self.siteini = ini.InputHandler(
                name='siteinfo', tablename='sitetable',
                lnedentry=lned)
            
            self.facade.input_register(self.siteini)

            self.site_manager()
            self.message.about(
                self, 'Status', 'Site Column Recorded')

        def site_manager(self):
            '''
            Receives an InputHandler object from the Site Dialog
            box. Registers the object to the Facade class
            and initiates a method to do work on that user input.
            '''
            try:
                self.sitedirector = self.facade.make_table('siteinfo')
                self._log = self.facade._tablelog['sitetable']

                self.facade.register_site_levels(
                    self.sitedirector._availdf[
                        'siteid'].values.tolist())
                
            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Check data is loaded and column name is correct')
                raise AttributeError('Column name not valid')

            if self.queryupdate is None:
                self.rawdataog = (
                    self.sitedirector._availdf.sort_values(
                        by='siteid'))
                self.sitetablemodel= self.viewEdit(
                    self.rawdataog)
                self.listviewSiteLabels.setModel(
                    self.sitetablemodel)
            else:
                pass

        def submit_change(self):
            '''
            Method to change factor levels of the raw
            data frame displayed on the MainWindow
            when the factor levels are modified by users.

            Additionally populates Site orms (self.siteorms)
            with final data and adds it to the orm.session

            More tabs in teh MainWindow are enabled once
            this dialog box is completed
            '''
            if not self.sitedbtable.values.tolist():
                self.sitetabledata = self.sitetablemodel.data(
                    None, QtCore.Qt.UserRole)
            else:
                self.sitetabledata = self.sitedbtablemodel.data(
                    None, QtCore.Qt.UserRole)
            self.changed_data.emit(self.facade._data)

            # Logging changes
            if self.rawdata is None:
                hlp.updated_df_values(
                    self.sitedirector._availdf.reset_index(drop=True),
                    self.sitetabledata.reset_index(drop=True),
                    self._log, 'sitetable')
            else:
                hlp.updated_df_values(
                    self.rawdata.reset_index(drop=True),
                    self.sitetabledata.reset_index(drop=True),
                    self._log, 'sitetable')
            # End logging

            remove = self.sitetabledata['siteid'].isin(
                self.sitedbtable['siteid'].values.tolist())
            self.sitetabledata = self.sitetabledata[~remove]
            self.sitemodlist = self.sitetabledata[
                list(self.siteloc.keys())].values.tolist()

            try:
                self.facade.replace_levels(
                    'siteinfo', self.sitemodlist)
            except Exception as e:
                print(str(e))
                self.error.showMessage('Could not modified levels')
                raise ValueError
            finally:
                for i in range(len(self.sitetabledata)):
                    self.siteorms[i] = orm.Sitetable(
                        siteid=self.sitetabledata.loc[i,'siteid'])
                    orm.session.add(self.siteorms[i])

                for i in range(len(self.sitetabledata)):
                    dbupload = self.sitetabledata.loc[
                        i,self.sitetabledata.columns].to_dict()
                    for key in dbupload.items():
                        setattr(self.siteorms[i], key[0], key[1])
                
                self.site_unlocks.emit('Tables Enabled')
                self.site_manager()
                self.close()

        def query_database(self):
            '''
            Method to query the database based on the current
            levels of our 'siteid' column.

            Return quries are display in the tabviewDbSiteQuery
            QtTableModel

            listviewSiteLabels QtTable model is updated with 
            an appended list to remove rows that already have
            a record inside the database
            '''
            try:
                qsitecondition = self.sitetablemodel.data(
                    None, QtCore.Qt.UserRole)
                self.queryupdate = qsitecondition[
                    'siteid'].values.tolist()

                dbsites = orm.session.query(
                    orm.Sitetable).order_by(
                        orm.Sitetable.siteid).filter(
                        orm.Sitetable.siteid.in_(self.queryupdate))

                self.sitedbtable = pd.read_sql(
                    dbsites.statement, dbsites.session.bind)
                self.sitequerymodel = self.view(
                    self.sitedbtable.sort_values(by='siteid'))
                self.tabviewDbSiteQuery.setModel(
                    self.sitequerymodel)

                self.message.about(self, 'Status', 'Database Queried')
                if not self.sitedbtable.values.tolist():
                    pass
                else:
                    remove = self.rawdataog['siteid'].isin(
                        self.sitedbtable['siteid'].values.tolist())            
                    self.rawdata = self.rawdataog[~remove]
                    self.sitedbtablemodel= self.viewEdit(
                        self.rawdataog[~remove])
                    self.listviewSiteLabels.setModel(
                        self.sitedbtablemodel)

            except Exception as e:
                print(str(e))
                raise LookupError('Could not query database')
        
    class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
        '''
        The main window class will serve to gather all informatoin
        from Dialog boxes, actions, and instantiate classes
        that are required to perform the necessary lower level logic
        (i.e. implement a Facade, Commander, MetaVerifier, etc.
        '''

        def __init__(self, parent=None):
            super().__init__(parent)
            # attributes
            self.setupUi(self)

            # ------- SITE DIALOG CONSTRUCTOR ARGS ----- #
            self.facade = face.Facade()
            self.dsite = SiteDialog()
            # Actions
            self.actionSiteTable.triggered.connect(self.site_display)
            # Custom Signals
            self.dsite.changed_data.connect(self.update_data_model)
            self.dsite.site_unlocks.connect(self.site_complete_enable)

            # ------ SESSION DIALOG CONSTRUCTOR ARGS ----- #
            # Dialog boxes for user feedback
            self.dsession = logicsess.SessionDialog()
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox
            # Custom signals
            self.dsession.raw_data_model.connect(
                self.update_data_model)
            self.dsession.webview_url.connect(
                self.update_webview)
            # actions
            self.actionStart_Session.triggered.connect(
                self.session_display)

        @QtCore.pyqtSlot(object)
        def update_data_model(self, dataobject):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)

        @QtCore.pyqtSlot(object)
        def update_webview(self, url):
            self.webView.load(QtCore.QUrl(url))

        def session_display(self):
            ''' Displays the Site Dialog box'''
            self.dsession.show()
            self.dsession.facade = self.facade
        # ------- END SESSION DIAGLOG CODE --------#

        # -------- START SITE DIALOG CODE ---------#

        @QtCore.pyqtSlot(object)
        def site_complete_enable(self):
            ''' 
            Method to enable actions for display dialog 
            boxes that corresond to different database tables
            '''
            self.actionMainTable.setEnabled(True)
            self.actionTaxaTable.setEnabled(True)
            self.actionTimeFormat.setEnabled(True)
            self.actionRawTable.setEnabled(True)
            self.actionCovariates.setEnabled(True)

        def site_display(self):
            ''' Displays the Site Dialog box'''
            self.dsite.show()
            self.dsite.facade = self.facade

    return UiMainWindow()

    
def test_dialog_site(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()

