from PyQt4 import QtGui
import class_inputhandler as ini
import class_modelviewpandas as view
import config as orm
import ui_dialog_taxa as uitax
from collections import OrderedDict
import ui_log_preview as tprev
import helpers as hlp

class TaxaDialog(QtGui.QDialog, uitax.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.facade = None
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
        self.preview = tprev.PreviewDialog()

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
            self.taxadirector = self.facade.make_table('taxainfo')
        except Exception as e:
            print(str(e))
            self.error.showMessage(
                'Column not identified')
            return

        self._log = self.facade._tablelog['taxatable']
        self.taxatable = self.taxadirector._availdf.copy()
        self.taxamodel = self.viewEdit(self.taxatable)

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
                orm.session.flush()

                # Populating the all
                # other fields for taxa orms
                for i in range(len(self.taxatable)):
                    upload = self.taxatable.loc[
                        i, self.taxatable.columns].to_dict()
                    for key in upload.items():
                        setattr(
                            self.taxaorms[i], key[0], key[1])
                orm.session.flush()

            except Exception as e:
                print(str(e))
                raise ValueError('Could not commit orm')

            self.close()
