#!/usr/bin/env python
import pytest
import pytestqt
import pandas as pd
from PyQt4 import QtGui, QtCore
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

            self.error = QtGui.QErrorMessage()
        def set_data(self):
            '''
            Method to register user input with facade,
            request the formated table from the facade,
            invoke the logger,
            set the data model,
            set the data model viewer
            '''
            self.facade.input_register(self.mainini)
            self.maindirector = self.facade.make_table('maininfo')
            self._log = self.facade._tablelog['maintable']
            self.maintable = self.maindirector._availdf.copy()
            self.mainmodel = self.viewEdit(self.maintable)
            self.tabviewMetadata.setModel(self.mainmodel)

        def submit_change(self):
            self.maintablemod = self.mainmodel.data(
                None, QtCore.Qt.UserRole)
            print('retrieved edited data')
            print(self.maintable['siteid'])
            print(self.maintablemod['siteid'])

            try:
                print('before types coversion')
                print(self.maintablemod.dtypes)
                orm.convert_types(self.maintablemod, orm.maintypes)
                print('after type conversion')
                print(self.maintablemod.dtypes)
                print('orm maintypes')
                print(orm.maintypes)
                
                for i in range(len(self.maintablemod)):
                    self.mainorms[i] = orm.Maintable(
                        siteid=self.maintablemod.loc[i,'siteid'])
                    orm.session.add(self.mainorms[i])

                print('In orm block')
                for i in range(len(self.maintablemod)):
                    dbupload = self.maintablemod.loc[
                        i,self.maintablemod.columns].to_dict()
                    for key in dbupload.items():
                        setattr(self.mainorms[i], key[0], key[1])
                orm.session.commit()
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
