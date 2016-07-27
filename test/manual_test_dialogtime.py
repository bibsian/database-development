#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
from collections import OrderedDict
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
from test import ui_dialog_time as uitime
from test import ui_logic_preview as tprev
from test import class_modelviewpandas as view
from test.logiclayer import class_userfacade as face
from test.logiclayer import class_timeparse as tmpa
from test.logiclayer import class_helpers as hlp


@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 8,
        'metaurl': ('http://sbc.test.rice.com'),
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
        filename='Datasets_manual_test/raw_data_test_2.csv')

    return fileinput

@pytest.fixture
def sitehandle():
    lned = {'siteid': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle

@pytest.fixture
def taxahandle():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('phylum', 'TAXON_PHYLUM'),
        ('class', 'TAXON_CLASS'),
        ('order', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('phylum', True),
        ('class', True),
        ('order', True),
        ('family', True),
        ('genus', True),
        ('species', True) 
    ))

    taxacreate = {
        'taxacreate': False
    }
    
    available = [
        x for x,y in zip(
            list(taxalned.keys()), list(
                taxackbox.values()))
        if y is True
    ]
    
    taxaini = ini.InputHandler(
        name='taxainput',
        tablename='taxatable',
        lnedentry= hlp.extract(taxalned, available),
        checks=taxacreate)
    return taxaini


@pytest.fixture
def TimeDialog(sitehandle, filehandle, metahandle, taxahandle):
    class TimeDialog(QtGui.QDialog, uitime.Ui_Dialog):
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
            self.facade.input_register(taxahandle)


            # Place holders for user inputs
            self.timelned = {}
            # Place holder: Data Model/ Data model view
            self.timemodel = None
            self.viewEdit = view.PandasTableModelEdit
            # Placeholders: Data tables
            self.timetable = None
            # Placeholder for maindata Orms
            self.timeorms = {}

            # Actions
            self.btnPreview.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnCancel.clicked.connect(self.close)

            # Update boxes/preview box
            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()
            self.preview = tprev.TablePreview()

        def submit_change(self):
            sender = self.sender()
            self.timelned = {
                'dayname': self.lnedDay.text(),
                'dayform': self.cboxDay.currentText(),
                'monthname': self.lnedMonth.text(),
                'monthform': self.cboxMonth.currentText(),
                'yearname': self.lnedYear.text(),
                'yearform': self.cboxYear.currentText(),
                'jd': self.ckJulian.isChecked(),
                'mspell': self.ckMonthSpelling.isChecked()
            }
            print('dict: ', self.timelned)
            for i, item in enumerate(self.timelned.values()):
                print('dict values: ', list(self.timelned.keys())[i], item)

            # Input handler
            self.timeini = ini.InputHandler(
                name='timeinfo', tablename='timetable',
                lnedentry=self.timelned)
            self.facade.input_register(self.timeini)

            # Initiating time parser class
            self.timetable = tmpa.TimeParse(
                self.facade._data, self.timelned)

            # Logger
            self.facade.create_log_record('timetable')
            self._log = self.facade._tablelog['timetable']            

            try:
                # Calling formater method
                timeview =self.timetable.formater().copy()
            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Could not format dates - ' +
                    'Check entries for errors'
                )
                raise ValueError(
                    'Could not format dates - ' +
                    'Check entries for errors')
            self.facade._valueregister['sitelevels']
            
            if sender is self.btnPreview:
                timeview = timeview.applymap(str)
                self.timemodel = self.viewEdit(timeview)
                self.preview.tabviewPreview.setModel(self.timemodel)
                self.preview.show()

            elif sender is self.btnSaveClose:
                hlp.write_column_to_log(
                    self.timelned, self._log, 'timetable'
                )
                try:
                    timeview = timeview.applymap(int)
                    self.facade.push_tables['timetable'] = (
                        timeview)
                    assert timeview is not None
                except Exception as e:
                    print(str(e))
                    self._log.debug(str(e))
                    self.error.showMessage(
                        'Could not convert data to integers')
                    raise TypeError(
                        'Could not convert data to integers')
                self.close()

    return TimeDialog()

def test_dialog_site(qtbot, TimeDialog):
    TimeDialog.show()
    qtbot.addWidget(TimeDialog)

    qtbot.stopForInteraction()
