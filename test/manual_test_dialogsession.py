#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtCore, QtGui, QtWebKit
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development" +
        "\\test\\")
os.chdir(rootpath)

from Views import ui_mainrefactor as mw
from Views import ui_dialog_session as dsess
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI import class_modelviewpandas as view


@pytest.fixture
def MainWindow():
    class SessionDialog(QtGui.QDialog, dsess.Ui_Dialog):
        '''
        Dialog box prompts the user to inpute
        unique metadata relating to the file that
        will be loaded. Also select and load file into
        rawdata viewer
        '''
        raw_data_model = QtCore.pyqtSignal(object)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            # Attributes
            self.metaini = None
            self.fileini = None
            self.verify = None

            # User facade composed from main window
            self.facade = None

            # Signal
            self.btnVerifyMeta.clicked.connect(self.meta_handler)
            self.btnSelectFile.clicked.connect(self.file_handler)
            self.btnCancel.clicked.connect(self.close)
            self.btnSaveClose.clicked.connect(self.close)
            
            # Status Message boxes
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox

        def meta_handler(self):
            '''
            Method to pass the user input about metadata to the mainwindow
            (where the facade class is instantiated).
            '''
            entries = {
                'globalid': int(self.lnedGlobalId.text().strip()),
                'metaurl': self.lnedMetadataUrl.text().strip(),
                'lter': self.cboxLTERloc.currentText().strip()
            }
            self.metaini = ini.InputHandler(
                name='metacheck', tablename=None,
                lnedentry=entries, verify=self.verify)

            self.facade.input_register(self.metaini)

            try:
                print(self.metaini.lnedentry['metaurl'])
                self.facade.meta_verify()
                self.message.about(self, 'Status', 'Entries recorded')

            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Invalid entries: ' + str(e))
                raise LookupError('Invalid metadata entries')
            
        def file_handler(self):
            '''
            Method to pass  the user input about the file to load
            '''
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
            headers = self.ckHeader.isChecked()
            self.fileini = ini.InputHandler(
                name='fileoptions', tablename=None,
                rbtns=rbtn, lnedentry=lned, filename=name,
                checks=headers
            )
            self.facade.input_register(self.fileini)

            try:
                self.facade.load_data()

                rawdatamodel = view.PandasTableModel(
                    self.facade._data)
                self.raw_data_model.emit(rawdatamodel)
                
            except Exception as e:
                self.filetypeReceive.emit(str(e))

        @QtCore.pyqtSlot(object)
        def info_updates(self, message):
            self.message.about(self, 'Status', message)

    class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
        '''
        The main window class will serve to gather all informatoin
        from Dialog boxes, actions, and instantiate classes
        that are required to perform the necessary lower level logic
        (i.e. implement a Facade, Commander, MetaVerifier, etc.
        '''

        raw_data_received = QtCore.pyqtSignal(object)
        
        def __init__(self, parent=None):
            super().__init__(parent)
            # attributes
            self.setupUi(self)
            self.facade = face.Facade()
            self.dsession = SessionDialog()

            # Dialog boxes for user feedback
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox

            # Custom signals
            self.dsession.raw_data_model.connect(
                self.update_data_model)
            
            # actions
            self.actionStart_Session.triggered.connect(
                self.session_display)
            
            self.mdiArea.addSubWindow(self.subwindow_2)
            self.mdiArea.addSubWindow(self.subwindow_1)
            
        @QtCore.pyqtSlot(object)
        def update_data_model(self, dataobject):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)
            self.raw_data_received.emit('Data loaded')

        def session_display(self):
            ''' Displays the Site Dialog box'''
            self.dsession.show()
            self.dsession.facade = self.facade
    return UiMainWindow()

def test_session_dialog(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()

