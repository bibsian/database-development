#!usr/bin/env python
from PyQt4 import QtGui, QtCore
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_mainrefactor as mw
import ui_logic_session as sesslogic
import ui_logic_site as sitelogic
import ui_logic_main as mainlogic
import class_userfacade as face
import class_modelviewpandas as view


if sys.platform == 'darwin':
    os.chdir(
        '/Users/bibsian/Dropbox/database-development/test/')
elif sys.platform == 'win32':
    os.chdir(
        'C:\\Users\\MillerLab\\Dropbox\\database-development\\test')


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
        
        # Actions
        self.actionSiteTable.triggered.connect(self.site_display)
        self.actionStart_Session.triggered.connect(
            self.session_display)
        self.actionMainTable.triggered.connect(self.main_display)

        # Custom Signals
        self.dsite.changed_data.connect(self.update_data_model)
        self.dsite.site_unlocks.connect(self.site_complete_enable)
        self.dsession.raw_data_model.connect(
            self.update_data_model)
        self.dsession.webview_url.connect(
            self.update_webview)

        # Dialog boxes for user feedback
        self.error = QtGui.QErrorMessage()
        self.message = QtGui.QMessageBox


    @QtCore.pyqtSlot(object)
    def update_data_model(self, dataobject):
        newdatamodel = view.PandasTableModel(self.facade._data)
        self.tblViewRaw.setModel(newdatamodel)
        self.dsite.facade = self.facade

    @QtCore.pyqtSlot(object)
    def update_webview(self, url):
        self.webView.load(QtCore.QUrl(url))


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


    def session_display(self):
        ''' Displays the Site Dialog box'''
        self.dsession.show()
        self.dsession.facade = self.facade

    def main_display(self):
        ''' Displays main dialog box'''
        self.dmain.facade = self.facade
        self.dmain.set_data()
        self.dmain.show()
