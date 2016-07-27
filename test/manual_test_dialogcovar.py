#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)
from test import class_inputhandler as ini
from test import class_userfacade as face
from test import class_modelviewpandas as views
from test import ui_dialog_covariate as covar
from test import ui_logic_preview as tprev

from test.logiclayer import class_helpers as hlp
from test.logiclayer import class_dictionarydataframe as ddf

@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 2,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.17'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def filehandle():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename='raw_data_test.csv')

    return fileinput

@pytest.fixture
def sitehandle():
    lned = {'siteid': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle

@pytest.fixture
def CovarDialog(metahandle, filehandle, sitehandle):
    class CovarDialog(QtGui.QDialog, covar.Ui_Dialog):
        '''
        Class to handler the user input into the covariates
        dialog box i.e. verify inputs and format data.
        '''
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            # Facade set up for the taxa dialog
            # box. These inputs will have been already
            # logged in the computer in order to
            # reach this phase
            self.facade = face.Facade()
            self.facade.input_register(metahandle)
            self.facade.meta_verify()
            self.facade.input_register(filehandle)
            self.facade.load_data()
            self.facade.input_register(sitehandle)
            sitelevels = self.facade._data[
                'SITE'].drop_duplicates().values.tolist()
            self.facade.register_site_levels(sitelevels)

            # Attributes
            self.covarlned = {'columns': None}
            self.covarini = None
            self._log = None
            self.covardata = None
            self.covarmodel = None

            
            # Signals/slots
            self.btnColumns.clicked.connect(self.submit_change)
            self.btnPreview.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnCancel.clicked.connect(self.close)

            # Pop up widgets
            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()
            self.preview = tprev.TablePreview()

        def submit_change(self):
            sender = self.sender()
            self.covarlned['columns'] = hlp.string_to_list(
                self.lnedColumns.text()
            )

            self.covarini = ini.InputHandler(
                name='covarinfo', tablename='covartable',
                lnedentry=self.covarlned)
            
            self.facade.input_register(self.covarini)
            self.facade.create_log_record('covartable')
            self._log = self.facade._tablelog['covartable']

            try:
                self.facade._data[self.covarlned['columns']]
            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Column names not valid: Check spacing ' +
                    'and headers.')
                raise ValueError('Column names are incorrect')

            try:
                self.covardata = ddf.DictionaryDataframe(
                    self.facade._data, self.covarlned['columns']
                ).convert_records()
            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage('Could not concatenate columns')
                raise TypeError('Could not concatenate columns')

            self.facade.push_tables['covariates'] = self.covardata
            
            if sender is self.btnColumns:
                self.message.about(self, 'Status', 'Columns recorded')
            elif sender is self.btnPreview:
                self.covarmodel = views.PandasTableModelEdit(
                    self.covardata)
                self.preview.tabviewPreview.setModel(self.covarmodel)
                self.preview.show()
            elif sender is self.btnSaveClose:
                hlp.write_column_to_log(
                    self.covarlned, self._log, 'covartable')
                self.close()

    return CovarDialog()

def test_covardialog(qtbot, CovarDialog):
    CovarDialog.show()
    qtbot.addWidget(CovarDialog)
    qtbot.stopForInteraction()

