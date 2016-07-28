#! /usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui
from collections import OrderedDict
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development" +
        "\\test\\")
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)
from test import ui_dialog_obs as obs
from test import ui_logic_preview as prev
from test import class_modelviewpandas as view
from test import class_inputhandler as ini
from test.logiclayer import class_userfacade as face
from test.logiclayer import class_helpers as hlp

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
        filename=
        str(os.getcwd()) + '/Datasets_manual_test/' +
        'raw_data_test_1.csv')

    return fileinput

@pytest.fixture
def sitehandle():
    lned = {'siteid': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle
    
@pytest.fixture
def ObsDialog(sitehandle, filehandle, metahandle):
    class ObsDialog(QtGui.QDialog, obs.Ui_Dialog):
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

            # Place holders for user inputs
            self.obslned = {}
            self.obsckbox = {}
            self.obsraw = {}
            self.available = None
            self.null = None
            # Place holder: Data Model/ Data model view
            self.obsmodel = None
            self.viewEdit = view.PandasTableModelEdit
            # Placeholders: Data tables
            self.obstable = None
            # Placeholder: Director (table builder), log
            self.obsdirector = None
            self._log = None
            # Placeholder for maindata Orms
            self.obsorms = {}
            # Actions
            self.btnPreview.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnCancel.clicked.connect(self.close)

            # Update boxes/preview box
            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()
            self.preview = prev.TablePreview()

        def submit_change(self):
            sender = self.sender()
            self.obslned = OrderedDict((
                ('spt_rep2', self.lnedRep2.text()),
                ('spt_rep3', self.lnedRep3.text()),
                ('spt_rep4', self.lnedRep4.text()),
                ('structure', self.lnedStructure.text()),
                ('individ', self.lnedIndividual.text()),
                ('trt_label', self.lnedTreatment.text()),
                ('unitobs', self.lnedRaw.text())
            ))

            self.obsckbox = OrderedDict((
                ('spt_rep2', self.ckRep2.isChecked()),
                ('spt_rep3', self.ckRep3.isChecked()),
                ('spt_rep4', self.ckRep4.isChecked()),
                ('structure', self.ckStructure.isChecked()),
                ('individ', self.ckIndividual.isChecked()),
                ('trt_label', self.ckTreatment.isChecked()),
                ('unitobs', False)
            ))

            available = [
                x for x,y in zip(
                    list(self.obslned.keys()), list(
                        self.obsckbox.values()))
                if y is False
            ]

            rawini = ini.InputHandler(
                name='rawinfo',
                tablename='rawtable',
                lnedentry= hlp.extract(self.obslned, available),
                checks=self.obsckbox)

            self.facade.input_register(rawini)
            self.facade.create_log_record('rawtable')
            self._log = self.facade._tablelog['rawtable']
            
            try:
                self.rawdirector = self.facade.make_table('rawinfo')
                assert self.rawdirector._availdf is not None

            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Column(s) not identified')
                raise AttributeError('Column(s) not identified')


            self.obstable = self.rawdirector._availdf.copy()
            self.obsmodel = self.viewEdit(self.obstable)
            if sender is self.btnPreview:
                self.preview.tabviewPreview.setModel(self.obsmodel)
                self.preview.show()
            elif sender is self.btnSaveClose:
                hlp.write_column_to_log(
                    self.obslned, self._log, 'rawtable')                
                self.close()

        
    return ObsDialog()
def test_dialog_site(qtbot, ObsDialog):
    ObsDialog.show()
    qtbot.addWidget(ObsDialog)

    qtbot.stopForInteraction()
