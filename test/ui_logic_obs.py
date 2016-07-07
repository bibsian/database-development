#!/usr/bin/env python
from PyQt4 import QtGui
from collections import OrderedDict
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from poplerGUI import ui_dialog_obs as obs
from poplerGUI import ui_logic_preview as prev
from logiclayer import class_helpers as hlp


class ObsDialog(QtGui.QDialog, obs.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.facade = None

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
            ('unitobs', self.lnedRaw.text())
        ))
        # Log input (put in after test)
        self.facade._colinputlog['rawinfo'] = self.obslned
        self.obsckbox = OrderedDict((
            ('sp_rep2_label', self.ckRep2.isChecked()),
            ('sp_rep3_label', self.ckRep3.isChecked()),
            ('sp_rep4_label', self.ckRep4.isChecked()),
            ('structure', self.ckStructure.isChecked()),
            ('individ', self.ckIndividual.isChecked()),
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
            self.taxadirector = self.facade.make_table('rawinfo')
            assert self.taxadirector._availdf is not None
            
        except Exception as e:
            print(str(e))
            self._log.debug(str(e))
            self.error.showMessage(
                'Column(s) not identified')
            raise AttributeError('Column(s) not identified')

        self.obstable = self.taxadirector._availdf.copy()
        self.obsmodel = self.viewEdit(self.obstable)
        if sender is self.btnPreview:
            self.preview.tabviewPreview.setModel(self.obsmodel)
            self.preview.show()
        elif sender is self.btnSaveClose:
            # Log input (put in after test)
            self.facade.push_tables['rawtable'] = self.obstable
            hlp.write_column_to_log(
                self.obslned, self._log, 'rawtable')                
            self.close()
