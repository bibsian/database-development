#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_dialog_taxa as uitax
import ui_dialog_table_preview as uiprev
import class_dialogpreview as prev
import class_inputhandler as ini
import class_userfacade as face
import class_modelviewpandas as view
import class_helpers as hlp
import config as orm
from collections import OrderedDict

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
def TablePreview():
    class TablePreview(QtGui.QDialog, uiprev.Ui_Dialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.btnCancel.clicked.connect(self.close)
    return TablePreview

@pytest.fixture
def TaxaDialog(sitehandle, filehandle, metahandle, TablePreview):
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
            self.facade.meta_verify()
            self.facade.input_register(filehandle)
            self.facade.load_data()
            self.facade.input_register(sitehandle)
            sitelevels = self.facade._data[
                'SITE'].drop_duplicates().values.tolist()
            self.facade.register_site_levels(sitelevels)

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
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnCancel.clicked.connect(self.close)

            # Update boxes/preview box
            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()
            self.preview = prev.PreviewDialog()

        def submit_change(self):
            '''
            Method to take user input for the taxa
            dialog box, pass the information to the user facade,
            create the taxa table, and then rename colums
            as necessary.
            '''
            sender = self.sender()
            self.taxalned = OrderedDict((
                ('sppcode', self.lnedSppCode.text().strip()),
                ('kingdom', self.lnedKingdom.text().strip()),
                ('phylum', self.lnedPhylum.text().strip()),
                ('clss', self.lnedClass.text().strip()),
                ('order', self.lnedOrder.text().strip()),
                ('family', self.lnedFamily.text().strip()),
                ('genus', self.lnedGenus.text().strip()),
                ('species', self.lnedSpp.text().strip())
            ))
            self.taxackbox = OrderedDict((
                ('sppcode', self.ckSppCode.isChecked()),
                ('kingdom', self.ckKingdom.isChecked()),
                ('phylum', self.ckPhylum.isChecked()),
                ('clss', self.ckClass.isChecked()),
                ('order', self.ckOrder.isChecked()),
                ('family', self.ckFamily.isChecked()),
                ('genus', self.ckGenus.isChecked()),
                ('species', self.ckSpp.isChecked())
            ))
            self.taxacreate = {
                'taxacreate': self.ckCreateTaxa.isChecked()
            }
            
            self.available = [
                x for x,y in zip(
                    list(self.taxalned.keys()), list(
                        self.taxackbox.values()))
                if y is True
            ]
            
            self.taxaini = ini.InputHandler(
                name='taxainfo',
                tablename='taxatable',
                lnedentry=hlp.extract(self.taxalned, self.available),
                checks=self.taxacreate
            )
            self.facade.input_register(self.taxaini)
            try:
                print('about to make taxa table')
                self.taxadirector = self.facade.make_table('taxainfo')


            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Column not identified')

            self._log = self.facade._tablelog['taxatable']
            try:
                self.taxatable = self.taxadirector._availdf.copy()
                self.taxamodel = self.viewEdit(self.taxatable)
            except Exception as e:
                print(str(e))
                
            
            if sender is self.btnTaxasubmit:
                self.preview.tabviewPreview.setModel(self.taxamodel)
                self.preview.show()
            elif sender is self.btnSaveClose:
                try:

                    # Instantiating taxa orms
                    for i in range(len(self.taxatable)):
                        self.taxaorms[i] = orm.Taxatable(
                            projid=self.taxatable.loc[i, 'projid'])
                        orm.session.add(self.taxaorms[i])
                    orm.session.commit()

                    # Populating the all
                    # other fields for taxa orms
                    for i in range(len(self.taxatable)):
                        upload = self.taxatable.loc[
                            i, self.taxatable.columns].to_dict()
                        for key in upload.items():
                            setattr(
                                self.taxaorms[i], key[0], key[1])
                    orm.session.commit()

                except Exception as e:
                    print(str(e))
                    raise ValueError('Could not commit orm')

                self.close()
                
    return TaxaDialog()

def test_dialog_site(qtbot, TaxaDialog):
    TaxaDialog.show()
    qtbot.addWidget(TaxaDialog)

    qtbot.stopForInteraction()
