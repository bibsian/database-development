#! /usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui
from collections import OrderedDict
import sys,os
from Views import ui_dialog_climateobs as climobs
from poplerGUI import ui_logic_preview as prev
from poplerGUI import class_modelviewpandas as view
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_helpers as hlp
rootpath = os.path.dirname(os.path.dirname( __file__ ))
end = os.path.sep
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)


@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 1,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.18'),
        'lter': 'SBC'}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=True)
    return metainput

@pytest.fixture
def filehandle():
    ckentry = {}
    rbtn = {'.csv': False, '.txt': False,
            '.xlsx': True}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        verify='climatesite',
        filename=
        str(os.getcwd()) + '/Datasets_manual_test/' +
        'climate_precip.txt')

    return fileinput

@pytest.fixture
def sitehandle():
    lned = {'siteid': 'site_a'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle
    
@pytest.fixture
def ClimateObsDialog(sitehandle, filehandle, metahandle):
    class ClimateObsDialog(QtGui.QDialog, climobs.Ui_Dialog):
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

            ))

            self.obsckbox = OrderedDict((

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

        
    return ClimateObsDialog()
def test_dialog_site(qtbot, ClimateObsDialog):
    ObsDialog.show()
    qtbot.addWidget(ObsDialog)

    qtbot.stopForInteraction()
