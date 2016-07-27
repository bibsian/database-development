#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
from poplerGUI import ui_dialog_session as dsess
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view

class SessionDialog(QtGui.QDialog, dsess.Ui_Dialog):
    '''
    Dialog box prompts the user to inpute
    unique metadata relating to the file that
    will be loaded into the database. Pass this information
    into the mainwindow once it has been verified as 
    correct/raw data file is uploaded.

    Any input generated from this table get directed to the user
    facade class.
    '''
    raw_data_model = QtCore.pyqtSignal(object)
    webview_url = QtCore.pyqtSignal(object)

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
        Method to verify the user input regarding the metadata
        record (globalid/url) they'll be working from.
        Url is passed to main window up verification.Note,
        take user input and wraps it in a InputHandler class.
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
            self.webview_url.emit(
                self.metaini.lnedentry['metaurl'])
            self.message.about(self, 'Status', 'Entries recorded')

        except Exception as e:
            print(str(e))
            self.error.showMessage('Invalid entries')
            raise LookupError('Invalid metadata entries')

    def file_handler(self):
        '''
        Method to pass the user input about the file to load.
        Note this is only tested for CSV file: Still have
        to run more test to make it more flexible. Note,
        takes user input and wraps it in a InputHandler class.
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
            raise IOError('Could not load data')

    @QtCore.pyqtSlot(object)
    def info_updates(self, message):
        ''' 
        Method to display message updates from mainwindow
        '''
        self.message.about(self, 'Status', message)
