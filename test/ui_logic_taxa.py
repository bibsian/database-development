from PyQt4 import QtGui
import pandas as pd
import class_inputhandler as ini
import class_modelviewpandas as view
import config as orm
import ui_dialog_taxa as uitax
from collections import OrderedDict
import ui_dialog_table_preview as uiprev
import helpers as hlp


class TablePreview(QtGui.QDialog, uiprev.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnCancel.clicked.connect(self.close)

class TaxaDialog(QtGui.QDialog, uitax.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

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
        for i,item in enumerate(self.taxaini.lnedentry):
            self.taxatable.rename(
                columns={self.taxatable.columns[i]:item},
                inplace=True)
        self.taxamodel = self.viewEdit(self.taxatable)
        if sender is self.btnTaxasubmit:
            self.preview = TablePreview()
            self.preview.tabviewPreview.setModel(self.taxamodel)
            self.preview.show()
        elif sender is self.btnSaveClose:
            try:
                if self.taxaorms.values() is not None:
                    self.taxaorms = {}
                else:
                    pass
                # ---- This block is dedicated to mergeing 
                # ---- data from the database to get foreign
                # ---- keys correct. Merging, projid's onto
                # ---- the raw data, then onto the taxa data
                globalid = self.facade._valueregister['globalid']
                siteloc = self.facade._inputs[
                    'siteinfo'].lnedentry['siteid']
                sitelevels = self.facade._valueregister[
                    'sitelevels']                    
                projids = orm.session.query(
                    orm.Maintable).order_by(
                        orm.Maintable.siteid).filter(
                            orm.Maintable.siteid.in_(sitelevels)
                            ).filter(
                                orm.Maintable.metarecordid ==
                                globalid)
                qmaindf = pd.read_sql(
                    projids.statement, projids.session.bind)
                rawmerge = pd.merge(
                    self.facade._data, qmaindf,
                    left_on=siteloc,
                    right_on='siteid', how='left')
                rawtaxacol = [
                    x for x in list(self.taxalned.values())
                    if x != '']

                rawtaxacol.append('projid')
                rawtaxacol.append(siteloc)
                taxadflist = []
                for i in sitelevels:
                    taxadflist.append(
                        rawmerge[rawmerge['siteid']==i].loc[
                            :, rawtaxacol[:]])

                taxamerge = taxadflist[0]
                for i,item in enumerate(taxadflist):
                    if i == 0:
                        pass
                    else:
                        taxamerge = pd.concat(
                            [taxamerge, item], axis=0).reset_index(
                                drop=True)

                rawtaxacol.remove('projid')
                self.available.append(siteloc)
                taxaall = pd.merge(
                    taxamerge, self.taxatable,
                    left_on=rawtaxacol,
                    right_on=self.available, how='left')
                taxaall = taxaall.drop_duplicates()
                taxaall = taxaall.reset_index(drop=True)

                alltaxacols = list(self.taxalned.keys())
                alltaxacols.insert(0, 'projid')
                alltaxacols.append('authority')

                for i in range(len(taxaall)):
                    self.taxaorms[i] = orm.Taxatable(
                        projid=taxaall.loc[i, 'projid'])
                    orm.session.add(self.taxaorms[i])
                for i in range(len(taxaall)):
                    upload = taxaall.loc[i, alltaxacols].to_dict()
                    for key in upload.items():
                        setattr(self.taxaorms[i], key[0], key[1])

                # ----- End Merging block
                # ----- TRY TO TURN INTO CLASS

            except Exception as e:
                print(str(e))
                raise ValueError('Could not commit orm')

            self.close()
