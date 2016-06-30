#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
from pandas import read_sql
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_mainrefactor as mw
import ui_logic_session as logicsess
import ui_logic_site as logicsite
import ui_dialog_main as dmainw
import class_userfacade as face
import class_inputhandler as ini
import class_helpers as hlp
import class_modelviewpandas as view
import class_flusher as flsh
import config as orm

@pytest.fixture
def MainWindow():
    class MainDialog(QtGui.QDialog, dmainw.Ui_Dialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            self.facade = None
            
            self.mainini = ini.InputHandler(
                name='maininfo', tablename='maintable')

            # Place holder: Data Model/ Data model view
            self.mainmodel = None
            self.viewEdit = view.PandasTableModelEdit

            # Placeholders: Data tables
            self.maintable = None
            self.maintablemod = None

            # Placeholder: Director (table builder), log
            self.maindirector = None
            self._log = None

            # Placeholder for maindata Orms
            self.mainorms = {}

            # Actions
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnCancel.clicked.connect(self.close)

            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()
        def set_data(self):
            '''
            Method to register user input with facade,
            request the formated table from the facade,
            invoke the logger,
            set the data model,
            set the data model viewer
            '''
            if self.maintablemod is None:
                self.facade.input_register(self.mainini)
                self.maindirector = self.facade.make_table('maininfo')
                self.facade.create_log_record('maintable')
                self._log = self.facade._tablelog['maintable']
                self.maintable = self.maindirector._availdf.copy()
                self.maintable = self.maintable.reset_index(drop=True)
            else:
                self.maintable = self.mainmodel.data(
                    None, QtCore.Qt.UserRole).reset_index(drop=True)

            self.mainmodel = self.viewEdit(self.maintable)
            self.tabviewMetadata.setModel(self.mainmodel)

        def submit_change(self):
            self.maintablemod = self.mainmodel.data(
                None, QtCore.Qt.UserRole).reset_index(drop=True)

            print('retrieved edited data')

            try:
                maincheck = orm.session.query(
                    orm.Maintable.metarecordid).order_by(
                        orm.Maintable.metarecordid)
                maincheckdf = read_sql(
                    maincheck.statement, maincheck.session.bind)
                metaid_entered = maincheckdf[
                    'metarecordid'].values.tolist()
                if self.facade._valueregister[
                        'globalid'] in metaid_entered:
                    self.message.about(
                        self, 'Status',
                        'Metarecord ID is already present in database')
                    return
                else:
                    pass
                
                orm.convert_types(self.maintable, orm.maintypes)
                orm.convert_types(self.maintablemod, orm.maintypes)            
                hlp.updated_df_values(
                    self.maintable, self.maintablemod,
                    self._log, 'maintable'
                )

                main_flush = flsh.Flusher(
                    self.maintablemod, 'maintable',
                    'siteid', self.facade._valueregister['lterid'])
                ck = main_flush.database_check(
                    self.facade._valueregister['sitelevels'])                
                if ck is True:
                    main_flush.go()
                else:
                    raise AttributeError

                self.close()
            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Incorrect datatypes on main table')
                raise AttributeError(
                    'Incorrect datatypes on maindata table')
            

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
            self.dsite = logicsite.SiteDialog()
            # Actions
            self.actionSiteTable.triggered.connect(self.site_display)
            # Custom Signals
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

            # ------- MAIN DIALOG CONSTRUCTOR ARGS ------- #
            self.dmain = MainDialog()
            self.actionMainTable.triggered.connect(self.main_display)
            

        def main_display(self):
            ''' Displays main dialog box'''
            self.dmain.facade = self.facade
            self.dmain.set_data()
            self.dmain.show()
        
        @QtCore.pyqtSlot(object)
        def update_data_model(self, dataobject):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)
            

        # ----------- START SESSION DIALOG CODE ----- #
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
        # --------- END SITE DIALOG CODE ----------#

    return UiMainWindow()

def test_dialog_site(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()
