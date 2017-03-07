#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
from collections import OrderedDict
import sys,os
from poplerGUI import class_inputhandler as ini
from Views import ui_dialog_addsitecolumn as addcol
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
        'metaurl': (
            'http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.18'
        ),
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
def AddSiteColumnDialog(sitehandle, filehandle, metahandle, taxahandle):
    class AddSiteColumnDialog(QtGui.QDialog, addcol.Ui_Dialog):
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

            self.sitelabel = None
            
            # Actions
            self.btnAddsite.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnCancel.clicked.connect(self.close)

            # Update boxes/preview box
            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()

        def submit_change(self):
            sender = self.sender()
            self.addsitecolumn = {
                'addsite': self.lnedAddsite.text()
            }

            # Input handler
            self.addsiteini = ini.InputHandler(
                name='addsite',
                lnedentry=self.addsitecolumn)
            self.facade.input_register(self.addsiteini)

            self.sitelabel = self.addsitecolumn['addsite']

            # Logger
            self.facade.create_log_record('addsite')
            self._log = self.facade._tablelog['addsite']            

            if sender is self.btnAddsite:
                try:
                    self.facade._data['site_added'] = self.sitelabel
                    self.message.about(self, 'Status', 'Site column added')
                except Exception as e:
                    print(str(e))
                    self._log.debug(str(e))
                    self.error.showMessage(
                        'Could create column for sites: ' + str(e)
                    )
                    raise ValueError(
                        'Could create column for sites: ' + str(e)
                    )
            if sender is self.btnSaveClose:
                hlp.write_column_to_log(
                    self.addsitecolumn, self._log, 'addsite'
                )
                try:
                    assert 'site_added' in self.facade._data.columns.values.tolist()
                except Exception as e:
                    print(str(e))
                    raise AttributeError(str(e))
                    self.error.showMessage(
                        'Could not add site column: ' + str(e)
                    )
                self.close()
            elif sender is self.btnCancel:
                self.close()

    return AddSiteColumnDialog()

def test_dialog_site(qtbot, AddSiteColumnDialog):
    AddSiteColumnDialog.show()
    qtbot.addWidget(AddSiteColumnDialog)

    qtbot.stopForInteraction()