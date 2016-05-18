#!usr/bin/env python
from PyQt4 import QtGui, QtCore, QtWebKit
import pandas as pd
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_mainrefactor as mw
import ui_dialog_session as dsession
import ui_dialog_site as dsite
import ui_dialog_main as dmain
import ui_dialog_taxa as dtaxa
import ui_dialog_time as dtime
import ui_dialog_obs as dobs
import ui_dialog_covariate as dcov
import class_userfacade as face
import class_inputhandler as ini
import class_modelviewpandas as view


if sys.platform == 'darwin':
    os.chdir(
        '/Users/bibsian/Dropbox/database-development/data/')
elif sys.platform == 'win32':
    os.chdir(
        'C:\\Users\\MillerLab\\Dropbox\\database-development\\data')


class SiteDialog(QtGui.QDialog, dsite.Ui_Dialog):
    '''
    Dialog pop up that promts the user to input_manager
    information regarding sites. When completed the certain
    tool bar options will be enabled.
    '''
    sitelocSent = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.siteini = None

        self.btnSiteID.clicked.connect(self.site_handler)

    def site_handler(self):
        pass

    def site_confirm(self):
        pass

class SessionDialog(QtGui.QDialog, dsession.Ui_Dialog):
    '''
    Dialog box prompts the user to inpute
    unique metadata relating to the file that
    will be loaded. Also select and load file into
    rawdata viewer
    '''
    metarecordSent = QtCore.pyqtSignal(object)
    filetypeSent = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Attributes
        self.metaini = None
        self.fileini = None

        # Signal
        self.btnVerifyMeta.clicked.connect(self.meta_handler)
        self.btnSelectFile.clicked.connect(self.file_handler)
        self.btnSaveClose.clicked.connect(self.close)
        self.btnCancel.clicked.connect(self.close)
        
        # Status Message boxes
        self.error = QtGui.QErrorMessage()
        self.message = QtGui.QMessageBox

    def meta_handler(self):
        '''
        Method to pass the user input about metadata to the mainwindow
        (where the facade class is instantiated).
        '''
        sender = self.sender()
        if sender == self.btnVerifyMeta:
            entries = {
                'globalid': int(self.lnedGlobalId.text().strip()),
                'metaurl': self.lnedMetadataUrl.text().strip(),
                'lter': self.cboxLTERloc.currentText().strip()
            }
            self.metaini = ini.InputHandler(
                name='metacheck', tablename=None,
                lnedentry=entries)
            assert self.metaini.name is not None
            self.metarecordSent.emit(self.metaini)
        else:
            pass

    @QtCore.pyqtSlot(str)
    def meta_confirm(self, windowmessage):
        self.message.about(self, 'Status', windowmessage)

    def file_handler(self):
        '''
        Method to pass  the user input about the file to load
        '''
        sender = self.sender()
        if sender == self.btnSelectFile:
            lned = {
                'sheet': self.lnedExcelSheet.text().strip(),
                'delim': self.lnedDelimiter.text().strip(),
                'tskip': self.lnedSkipTop.text().strip(),
                'bskip': self.lnedSkipBottom.text().strip()
            }
            rbtn = {
                'csv': self.rbtnCsv.isChecked(),
                'xlsx': self.rbtnExcel.isChecked(),
                'txt': self.rbtnTxt.isChecked()
            }
            name = QtGui.QFileDialog.getOpenFileName(
                self, 'Select File')

            self.fileini = ini.InputHandler(
                name='fileoptions', tablename=None,
                rbtns=rbtn, lnedentry=lned, filename=name
            )

            assert self.fileini.name is not None
            self.filetypeSent.emit(self.fileini)

    @QtCore.pyqtSlot(object)
    def file_confirm(self, windowmessage):
        self.message.about(self, 'Status', windowmessage)


class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
    '''
    The main window class will serve to gather all informatoin
    from Dialog boxes, actions, and instantiate classes
    that are required to perform the necessary lower level logic
    (i.e. implement a Facade, Commander, MetaVerifier, etc.
    '''

    metarecordReceive = QtCore.pyqtSignal(str)
    filetypeReceive = QtCore.pyqtSignal(str)
    metadatafile = pd.read_csv(
        'meta_file_test.csv', encoding='iso-8859-11')

    def __init__(self, parent=None):
        super().__init__(parent)
        # attributes
        self.setupUi(self)
        self.facade = face.Facade()
        self.dsession = SessionDialog()
        self.dsite = SiteDialog()

        # Custom Signals from dialogs
        self.dsession.metarecordSent.connect(self.session_manager)
        self.dsession.filetypeSent.connect(self.session_manager)

        self.metarecordReceive.connect(
            self.dsession.meta_confirm)
        self.filetypeReceive.connect(
            self.dsession.meta_confirm)

        # Dialog boxes for user feedback
        self.error = QtGui.QErrorMessage()
        self.message = QtGui.QMessageBox

        # actions
        self.actionStart_Session.triggered.connect(
            self.session_display)
        self.actionSiteTable.triggered.connect(
            self.site_display)

        # Persistent views
        metadatamodel = view.PandasTableModel(self.metadatafile)
        self.tblViewMeta.setModel(metadatamodel)

    def session_display(self):
        ''' Open the session dialog box'''
        self.dsession.show()

    def site_display(self):
        ''' Open the site dialog box'''
        self.dsite.show()

    @QtCore.pyqtSlot(object)
    def session_manager(self, dataobject):
        '''
        Methods to display the Session dialog box and initiate
        functionality
        '''
        if dataobject.name == 'metacheck':
            print('In metacheck blocks')
            self.facade.input_register(dataobject)
            try:
                self.facade.meta_verify()
                self.metarecordReceive.emit('Input recorded')
                self.webView.load(
                    QtCore.QUrl(dataobject.lnedentry['metaurl']))
                
            except Exception as e:
                self.metarecordReceive.emit(str(e))
    
        elif dataobject.name == 'fileoptions':
            print('In fileoptions block')
            self.facade.input_register(dataobject)
            try:
                self.facade.load_data()
                self.filetypeReceive.emit('Data loaded')
                datamodel = view.PandasTableModel(self.facade._data)
                self.tblViewRaw.setModel(datamodel)

            except Exception as e:
                self.filetypeReceive.emit(str(e))

    def site_manager(self):
        '''
        Methods to display the Site diaglog box and initiate
        it's functionality
        '''
        pass

