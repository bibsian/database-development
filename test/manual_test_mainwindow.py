#! /usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
from pandas import read_csv
import subprocess
import sys,os
import unicodedata
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Dropbox/database-development/" +
        "test/")
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")

from test import ui_mainrefactor as mw
from test import ui_logic_session as sesslogic
from test import ui_logic_site as sitelogic
from test import ui_logic_main as mainlogic
from test import ui_logic_taxa as taxalogic
from test import ui_logic_time as timelogic
from test import ui_logic_obs as rawlogic
from test import ui_logic_covar as covarlogic
from test.logiclayer import class_userfacade as face
from test import class_modelviewpandas as view
from test import class_inputhandler as ini

if sys.platform == 'darwin':
    os.chdir(
        '/Users/bibsian/Dropbox/database-development/test/')
elif sys.platform == 'win32':
    os.chdir(
        'C:\\Users\\MillerLab\\Dropbox\\database-development\\test\\')

@pytest.fixture
def MainWindow():
    class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
        '''
        The main window class will serve to manage the display
        of various dialog boxes, the facade class, model-viewer
        tables, and menu actions.
        '''

        def __init__(self, parent=None):
            super().__init__(parent)
            # attributes
            self.setupUi(self)
            self.facade = face.Facade()
            self.dsite = sitelogic.SiteDialog()
            self.dsession = sesslogic.SessionDialog()
            self.dmain = mainlogic.MainDialog()
            self.dtaxa = taxalogic.TaxaDialog()
            self.dtime = timelogic.TimeDialog()
            self.draw = rawlogic.ObsDialog()
            self.dcovar = covarlogic.CovarDialog()

            # Actions
            self.actionSiteTable.triggered.connect(self.site_display)
            self.actionStart_Session.triggered.connect(
                self.session_display)
            self.actionEnd_Session.triggered.connect(
                self.end_session)
            self.actionMainTable.triggered.connect(self.main_display)
            self.actionTaxaTable.triggered.connect(self.taxa_display)
            self.actionTimeFormat.triggered.connect(self.time_display)
            self.actionRawTable.triggered.connect(self.obs_display)
            self.actionCovariates.triggered.connect(self.covar_display)
            self.actionCommit.triggered.connect(self.commit_data)


            self.mdiArea.addSubWindow(self.subwindow_2)
            self.mdiArea.addSubWindow(self.subwindow_1)
            
            # Custom Signals
            self.dsite.site_unlocks.connect(self.site_complete_enable)
            self.dsession.raw_data_model.connect(
                self.update_data_model)

            # Dialog boxes for user feedback
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox

            metadf = read_csv('Datasets_manual_test/meta_file_test.csv')
            metamodel = view.PandasTableModel(metadf)
            self.tblViewMeta.setModel(metamodel)

        def update_data_model(self):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)
            self.dsite.facade = self.facade

        @QtCore.pyqtSlot(object)
        def update_webview(self, url):
            print(url)
            
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

        def session_display(self):
            ''' Displays the Site Dialog box'''
            self.dsession.show()
            self.dsession.facade = self.facade

        def main_display(self):
            ''' Displays main dialog box'''
            self.dmain.facade = self.facade
            self.dmain.set_data()
            self.dmain.show()

        def taxa_display(self):
            ''' Display the Taxa Dialog box'''
            self.dtaxa.facade = self.facade
            self.dtaxa.show()

        def time_display(self):
            ''' Display the Time Dialog box'''
            self.dtime.facade = self.facade
            self.dtime.show()

        def obs_display(self):
            ''' Display the Raw Obs Dialog box'''
            self.draw.facade = self.facade
            self.draw.show()

        def covar_display(self):
            '''Display the Raw Obs Dialog box'''
            self.dcovar.facade = self.facade
            self.dcovar.show()

        def commit_data(self):
            commithandle = ini.InputHandler(
                name='updateinfo', tablename='updatetable')
            self.facade.input_register(commithandle)
            try:
                self.facade.merge_push_data()
                self.facade.update_main()
                self.actionCommit.setEnabled(False)
                self.message.about(
                    self, 'Status', 'Database transaction complete')
            except Exception as e:
                print(str(e))
                self.facade._tablelog['maintable'].debug(str(e))
                self.error.showMessage(
                    'Datbase transaction error: ' + str(e) +
                    '. May need to alter site abbreviations.')
                raise ValueError(str(e))

        def end_session(self):
            subprocess.call(
                "python" + " poplerGUI_run_main.py", shell=True)
            self.close()

    return UiMainWindow()


def test_dialog_site(qtbot, MainWindow):
    MainWindow.show()

    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()
