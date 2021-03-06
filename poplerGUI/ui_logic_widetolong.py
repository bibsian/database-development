#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
from Views import ui_dialog_widetolong as dwidetolong
from pandas import wide_to_long
from poplerGUI import ui_logic_preview as tprev
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI import class_inputhandler as ini

class WidetoLongDialog(QtGui.QDialog, dwidetolong.Ui_Dialog):
    '''
    Logic to deal with changing dataframe from wide to long
    format
    '''
    update_data = QtCore.pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Place holders for user inputs
        self.widetolonglned = {}
        # Place holder: Data Model/ Data model view
        self.widetolongmodel = None
        self.viewEdit = view.PandasTableModel
        # Placeholders: Data tables
        self.widetolongtable = None
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
        self.widetolonglned = {
            'value_columns': hlp.string_to_list(self.lnedValuecolumns.text()),
            'datatype_name': self.cboxDatatypecolumn.currentText(),
            'panel_data': self.ckPaneldata.isChecked()
        }

        
        self.widetolongini = ini.InputHandler(
            name='widetolong',
            lnedentry=self.widetolonglned
        )

        self.facade.input_register(self.widetolongini)
        self.facade.create_log_record('widetolong')
        self._log = self.facade._tablelog['widetolong']

        try:
            if self.widetolonglned['panel_data'] is False:
                self.widetolongtable = hlp.wide_to_long(
                    self.facade._data,
                    value_columns=self.widetolonglned['value_columns'],
                    value_column_name=self.widetolonglned['datatype_name']
                )
            else:
                temp = self.facade._data.copy()
                temp['id'] = temp.index
                self.widetolongtable = wide_to_long(
                    temp,
                    self.widetolonglned['value_columns'],
                    i="id", j=self.widetolonglned['datatype_name'])
                self.widetolongtable[
                    self.widetolonglned['datatype_name']] = self.widetolongtable.index.get_level_values(
                        self.widetolonglned['datatype_name'])
                self.widetolongtable.reset_index(drop=True, inplace=True)
        except Exception as e:
            print(str(e))
            self.error.showMessage('Could not melt data: ' + str(e))

        try:
            assert self.widetolonglned['datatype_name'] != 'NULL'
        except Exception as e:
            print(str(e))
            self.error.showMessage(
                'Invalid datatype column: ', str(e))
            return

        if sender is self.btnPreview:
            self.widetolongmodel = view.PandasTableModel(
                self.widetolongtable)
            self.preview.tabviewPreview.setModel(
                self.widetolongmodel)
            self.preview.show()
        elif sender is self.btnSaveClose:
            hlp.write_column_to_log(
                self.widetolonglned, self._log, 'widetolong')
            self.facade._data = self.widetolongtable
            self.update_data.emit('wide_to_long_mod')
            self.close()
