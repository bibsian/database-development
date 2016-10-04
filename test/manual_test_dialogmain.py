#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
from pandas import read_sql
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from Views import ui_mainrefactor as mw
from Views import ui_dialog_main as dmainw
from poplerGUI import ui_logic_session as logicsess
from poplerGUI import ui_logic_site as logicsite
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_helpers as hlp

@pytest.fixture
def MainWindow():
    class MainDialog(QtGui.QDialog, dmainw.Ui_Dialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            self.facade = None
            
            self.mainini = ini.InputHandler(
                name='maininfo', tablename='project_table')

            # Place holder: Data Model/ Data model view
            self.mainmodel = None
            self.viewEdit = view.PandasTableModelEdit

            # Placeholders: Data tables
            self.project_table = None
            self.project_tablemod = None

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
            if self.project_tablemod is None:
                self.facade.input_register(self.mainini)
                self.maindirector = self.facade.make_table('maininfo')
                self.facade.create_log_record('project_table')
                self._log = self.facade._tablelog['project_table']
                self.project_table = self.maindirector._availdf.copy()
                self.project_table = self.project_table.reset_index(
                    drop=True)
            else:
                self.project_table = self.mainmodel.data(
                    None, QtCore.Qt.UserRole).reset_index(drop=True)

            self.mainmodel = self.viewEdit(self.project_table)
            self.tabviewMetadata.setModel(self.mainmodel)

        def submit_change(self):
            self.project_tablemod = self.mainmodel.data(
                None, QtCore.Qt.UserRole).reset_index(drop=True)
            self.facade.push_tables['project_table'] = self.project_tablemod
            print('retrieved edited data')
            print('main mod: ', self.project_tablemod)
            self._log.debug(
                'project_table mod: ' +
                ' '.join(self.project_tablemod.columns.values.tolist()))

            try:
                session = orm.Session()
                maincheck = session.query(
                    orm.project_table.proj_metadata_key).order_by(
                        orm.project_table.proj_metadata_key)
                maincheckdf = read_sql(
                    maincheck.statement, maincheck.session.bind)
                metaid_entered = maincheckdf[
                    'proj_metadata_key'].values.tolist()
                print(metaid_entered)
                print(self.facade._valueregister['globalid'])
                if self.facade._valueregister[
                        'globalid'] in metaid_entered:
                    self.message.about(
                        self, 'Status',
                        'Metarecord ID is already present in database')
                    return
                else:
                    pass

                orm.convert_types(self.project_table, orm.project_types)
                orm.convert_types(self.project_tablemod, orm.project_types)

                hlp.updated_df_values(
                    self.project_table, self.project_tablemod,
                    self._log, 'project_table')
                self.close()

            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Global Id already present in database: ' + str(e))
                raise AttributeError(
                    'Global Id already present in database')
            

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
        
        def update_data_model(self):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)

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
            self.update_data_model()

        def site_display(self):
            ''' Displays the Site Dialog box'''
            self.dsite.show()
            self.dsite.facade = self.facade

        # --------- END SITE DIALOG CODE ----------#

    return UiMainWindow()

        # ----------- START SESSION DIALOG CODE ----- #
def test_dialog_site(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()
