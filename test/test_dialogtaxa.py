#!/usr/bin/env python
import pytest
import pytestqt
import pandas as pd
from PyQt4 import QtGui, QtCore
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_dialog_taxa as uitax
import class_dialogpreview as prev
import class_inputhandler as ini
import class_userfacade as face
import class_modelviewpandas as view
import class_helpers as hlp
import config as orm


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
def TaxaDialog(sitehandle, filehandle, metahandle):
    class TaxaDialog(QtGui.QDialog, uitax.Ui_Dialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            # Facade set up for the taxa dialog
            # box. These inputs will have been already
            # logged in the computer in order to
            # reach this phase
            self.facade = face.Facade()
            self.facade.input_register(metahandle)
            self.meta_verify()
            self.facade.input_register(filehandle)
            self.load_data
            self.facade.input_register(sitehandle)
            sitelevels = face._data[
                'SITE'].drop_duplicates().values.tolist()
            face.register_site_levels(sitelevels)

            # Place holders for user inputs
            self.taxalned = {}
            self.taxackbox = {}
            self.taxacreate = {}
            self.available = None
            self.null = None
            # Place holder: Data Model/ Data model view
            self.taxamodel = None
            self.viewEdit = view.PandasTableModelEdit
            # Placeholders: Data tables
            self.taxatable = None
            # Placeholder: Director (table builder), log
            self.taxadirector = None
            self._log = None
            # Placeholder for maindata Orms
            self.taxaorms = {}
            # Actions
            self.btnTaxasubmit.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.close)
            self.btnCancel.clicked.connect(self.close)

            # Update boxes/preview box
            self.error = QtGui.QErrorMessage()
            self.preview = prev.PreviewDialog()

        def submit_change(self):
            self.taxalned = {
                'sppcode': self.lnedSppCode.text().strip(),
                'kingdom': self.lnedKingdom.text().strip(),
                'phylum': self.lnedPhylum.text().strip(),
                'class': self.lnedClass.text().strip(),
                'order': self.lnedOdrder.text().strip(),
                'family': self.lnedFamily.text().strip(),
                'genus': self.lnedGenus.text().strip(),
                'species': self.lnedSpecies.text().strip()
            }

            self.taxackbox = {
                'sppcode': self.ckSppCode.isChecked(),
                'kingdom': self.ckKingdom.isChecked(),
                'phylum': self.ckPhylum.isChecked(),
                'class': self.ckClass.isChecked(),
                'order': self.ckOdrder.isChecked(),
                'family': self.ckFamily.isChecked(),
                'genus': self.ckGenus.isChecked(),
                'species': self.ckSpecies.isChecked()
            }

            self.taxacreate = {
                'taxacreate': self.ckCreateTaxa.isChecked()
            }

            self.available = [
                x for x,y in zip(
                    list(self.taxalned.keys()), list(
                        self.taxackbox.values()))
                if y is True
            ]

            self.null = [
                x for x,y in zip(
                    list(self.taxalned.keys()), list(
                        self.taxackbox.values()))
                if y is False
            ]

            self.taxaini = ini.InputHandler(
                name='taxainfo',
                tablename='taxatable',
                lnedentry=hlp.extract(self.taxalned, self.available),
                checks=self.taxacreate
            )
            
            self.facade.input_register(self.taxaini)
            self.taxadirector = self.facade.make_table('taxainfo')
            self._log = self.facade._tablelog['taxatable']
            self.taxatable = self.taxadirector._availdf.copy()
            self.taxamodel = self.viewEdit(self.taxatable)


            try:
                orm.convert_types(self.maintablemod, orm.taxatypes)
                
                for i in range(len(self.maintablemod)):
                    self.mainorms[i] = orm.Maintable(
                        siteid=self.maintablemod.loc[i,'siteid'])
                    orm.session.add(self.mainorms[i])

                print('In orm block')
                for i in range(len(self.maintablemod)):
                    dbupload = self.maintablemod.loc[
                        i,self.maintablemod.columns].to_dict()
                    for key in dbupload.items():
                        setattr(self.mainorms[i], key[0], key[1])
                orm.session.commit()
                self.close()
            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Incorrect datatypes on main table')
                raise AttributeError(
                    'Incorrect datatypes on maindata table')
    
