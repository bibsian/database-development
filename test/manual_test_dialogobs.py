#! /usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui
from collections import OrderedDict
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"
    
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"

    
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)
from Views import ui_dialog_obs as obs
from poplerGUI import ui_logic_preview as prev
from poplerGUI import class_modelviewpandas as view
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_helpers as hlp

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
        rootpath + end + 'test' + end +
        'Datasets_manual_test' + end + 
        'raw_data_test_1.csv')

    return fileinput

@pytest.fixture
def sitehandle():
    lned = {'study_site_key': 'site'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
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
                'site'].drop_duplicates().values.tolist()
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
            self.tablename = None
            self.table = None

            # Update boxes/preview box
            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()
            self.preview = prev.TablePreview()

        def submit_change(self):
            sender = self.sender()
            self.obslned = OrderedDict((
                ('spatial_replication_level_2', self.lnedRep2.text()),
                ('spatial_replication_level_3', self.lnedRep3.text()),
                ('spatial_replication_level_4', self.lnedRep4.text()),
                ('structure', self.lnedStructure.text()),
                ('trt_label', self.lnedTreatment.text()),
                ('unitobs', self.lnedRaw.text())
            ))

            self.obsckbox = OrderedDict((
                ('spatial_replication_level_2', self.ckRep2.isChecked()),
                ('spatial_replication_level_3', self.ckRep3.isChecked()),
                ('spatial_replication_level_4', self.ckRep4.isChecked()),
                ('structure', self.ckStructure.isChecked()),
                ('trt_label', self.ckTreatment.isChecked()),
                ('unitobs', self.ckRaw.isChecked())
            ))


            self.table = {
                'count_table': self.ckCount.isChecked(),
                'biomass_table': self.ckBiomass.isChecked(),
                'density_table': self.ckDensity.isChecked(),
                'percent_cover_table': self.ckPercentcover.isChecked(),
                'individual_table': self.ckIndividual.isChecked() 
            }

            available = [
                x for x,y in zip(
                    list(self.obslned.keys()), list(
                        self.obsckbox.values()))
                if y is True
            ]

            self.tablename = [
                x for x, y in
                zip(list(self.table.keys()), list(self.table.values()))
                if y is True
            ][0]

            rawini = ini.InputHandler(
                name='rawinfo',
                tablename= self.tablename,
                lnedentry= hlp.extract(self.obslned, available),
                checks=self.obsckbox)



            self.facade.input_register(rawini)
            self.facade.create_log_record(self.tablename)
            self._log = self.facade._tablelog[self.tablename]

            
            try:
                self.rawdirector = self.facade.make_table('rawinfo')
                print('obs table build: ', self.rawdirector)
                assert self.rawdirector._availdf is not None

            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Column(s) not identified')
                raise AttributeError(
                    'Column(s) not identified: ' + str(e))


            self.obstable = self.rawdirector._availdf.copy()
            self.obsmodel = self.viewEdit(self.obstable)
            if sender is self.btnPreview:
                self.preview.tabviewPreview.setModel(self.obsmodel)
                self.preview.show()
            elif sender is self.btnSaveClose:
                hlp.write_column_to_log(
                    self.obslned, self._log, self.tablename)                
                self.close()

        
    return ObsDialog()
def test_dialog_site(qtbot, ObsDialog):
    ObsDialog.show()
    qtbot.addWidget(ObsDialog)

    qtbot.stopForInteraction()
