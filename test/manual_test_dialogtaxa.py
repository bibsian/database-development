#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui
from collections import OrderedDict
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development")
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)
from Views import ui_dialog_taxa as uitax
from Views import ui_dialog_table_preview as uiprev
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer.datalayer import config as orm


    
@pytest.fixture
def TablePreview():
    class TablePreview(QtGui.QDialog, uiprev.Ui_Dialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.btnCancel.clicked.connect(self.close)
    return TablePreview

@pytest.fixture
def TaxaDialog(site_handle_free, file_handle_free, meta_handle_free, TablePreview):
    class TaxaDialog(QtGui.QDialog, uitax.Ui_Dialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            # Facade set up for the taxa dialog
            # box. These inputs will have been already
            # logged in the computer in order to
            # reach this phase
            self.facade = face.Facade()
            self.facade.input_register(meta_handle_free)
            self.facade.meta_verify()
            self.facade.input_register(file_handle_free)
            self.facade.load_data()
            self.facade.input_register(site_handle_free)
            sitelevels = self.facade._data[
                site_handle_free.lnedentry['study_site_key']].drop_duplicates().values.tolist()
            self.facade.register_site_levels(sitelevels)

            # Place holders for user inputs
            self.taxalned = {}
            self.taxackbox = {}
            self.taxacreate = {}
            self.available = None
            self.null = None
            self.saved = False
            # Place holder: Data Model/ Data model view
            self.taxamodel = None
            self.viewEdit = view.PandasTableModelEdit
            # Placeholders: Data tables
            self.taxa_table = None
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
            self.preview = TablePreview()

        def submit_change(self):
            '''
            Method to take user input for the taxa
            dialog box, pass the information to the user facade,
            create the taxa table, and then rename colums
            as necessary.
            '''
            sender = self.sender()
            self.taxalned = OrderedDict((
                ('common_name', self.lnedCommonname.text().strip()),
                ('sppcode', self.lnedSppCode.text().strip()),
                ('kingdom', self.lnedKingdom.text().strip()),
                ('subkingdom', self.lnedSubkingdom.text().strip()),
                ('infrakingdom', self.lnedInfrakingdom.text().strip()),
                ('superdivision', self.lnedSuperdivision.text().strip()),
                ('division', self.lnedDivision.text().strip()),
                ('subsubdivision', self.lnedSubdivision.text().strip()),
                ('superphylum', self.lnedSuperphylum.text().strip()),
                ('phylum', self.lnedPhylum.text().strip()),
                ('subphylum', self.lnedSubphylum.text().strip()),
                ('clss', self.lnedClass.text().strip()),
                ('subclass', self.lnedSubclass.text().strip()),
                ('ordr', self.lnedOrder.text().strip()),
                ('family', self.lnedFamily.text().strip()),
                ('genus', self.lnedGenus.text().strip()),
                ('species', self.lnedSpp.text().strip())
            ))

            self.taxackbox = OrderedDict((
                ('common_name', self.ckCommonname.isChecked()),
                ('sppcode', self.ckSppCode.isChecked()),
                ('kingdom', self.ckKingdom.isChecked()),
                ('subkingdom', self.ckSubkingdom.isChecked()),
                ('infrakingdom', self.ckInfrakingdom.isChecked()),
                ('superdivision', self.ckSuperdivision.isChecked()),
                ('division', self.ckDivision.isChecked()),
                ('subsubdivision', self.ckSubdivision.isChecked()),
                ('superphylum', self.ckSuperphylum.isChecked()),
                ('phylum', self.ckPhylum.isChecked()),
                ('subphylum', self.ckSubphylum.isChecked()),
                ('clss', self.ckClass.isChecked()),
                ('subclass', self.ckSubclass.isChecked()),
                ('ordr', self.ckOrder.isChecked()),
                ('family', self.ckFamily.isChecked()),
                ('genus', self.ckGenus.isChecked()),
                ('species', self.ckSpp.isChecked())
            ))

            # NEED TO IMPLEMNT METHODS TO CREATE COLUMNS FROM
            # USER INPUT (should be easy) !!!!!!!!!
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
                tablename='taxa_table',
                lnedentry=hlp.extract(self.taxalned, self.available),
                checks=self.taxacreate
            )
            self.facade.input_register(self.taxaini)
            self.facade.create_log_record('taxa_table')
            self._log = self.facade._tablelog['taxa_table']

            try:
                print('about to make taxa table')
                self.taxadirector = self.facade.make_table(
                    'taxainfo')
                assert self.taxadirector._availdf is not None

            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Column(s) not identified')
                raise AttributeError(
                    'Column(s) not identified: ' + str(e))

            self.taxa_table = self.taxadirector._availdf.copy()
            self.taxamodel = self.viewEdit(self.taxa_table)
            
            if sender is self.btnTaxasubmit:
                self.preview.tabviewPreview.setModel(self.taxamodel)
                self.preview.show()
            elif sender is self.btnSaveClose:
                # Convert to strings and strip
                self.taxa_table = self.taxa_table.applymap(str)
                self.taxa_table = self.taxa_table.applymap(lambda x: x.strip())

                self.facade.push_tables['taxa_table'] = self.taxa_table
                hlp.write_column_to_log(
                    self.taxalned, self._log, 'taxa_table')
                self.saved = True
                self.close()
                
    return TaxaDialog()

def test_dialog_site(qtbot, TaxaDialog):
    TaxaDialog.show()
    qtbot.addWidget(TaxaDialog)

    qtbot.stopForInteraction()

