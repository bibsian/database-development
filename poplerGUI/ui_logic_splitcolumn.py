#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
from Views import ui_dialog_splitcolumn as dsplitcolumn
from poplerGUI import ui_logic_preview as tprev
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI import class_inputhandler as ini


class SplitColumnDialog(QtGui.QDialog, dsplitcolumn.Ui_Dialog):
    '''
    User Logic to deal with split a column from one into two based
    on user supplied separator (currently regex does not work)
    '''
    update_data = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.previous_click = False
        # Place holders for user inputs
        self.splitcolumnlned = {}
        # Place holder: Data Model/ Data model view
        self.splitcolumnmodel = None
        self.viewEdit = view.PandasTableModelEdit(None)
        # Placeholders: Data tables
        self.splitcolumntable = None
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
        self.splitcolumnlned = {
            'column_name':
            self.lnedColumnname.text().strip(),
            'split_column_by':
            self.lnedSplitcolumnby.text()
        }
        print('split inputs: ', self.splitcolumnlned)
        self.splitcolumnini = ini.InputHandler(
            name='splitcolumn',
            lnedentry=self.splitcolumnlned
        )
        self.facade.input_register(self.splitcolumnini)
        self.facade.create_log_record('splitcolumn')
        self._log = self.facade._tablelog['splitcolumn']
        if self.previous_click is True:
            self.viewEdit = view.PandasTableModelEdit(None)
        else:
            pass

        try:
            self.splitcolumntable = hlp.split_column(
                self.facade._data,
                self.splitcolumnlned['column_name'],
                self.splitcolumnlned['split_column_by']
            )
            self.previous_click = True
            hlp.write_column_to_log(
                self.splitcolumnlned, self._log, 'splitcolumn')
        except Exception as e:
            print(str(e))
            self.error.showMessage(
                'Could not split column: ' + str(e))

        if sender is self.btnPreview:
            self.viewEdit.set_data(
                self.splitcolumntable)
            self.preview.tabviewPreview.setModel(
                self.viewEdit)
            self.preview.show()
        elif sender is self.btnSaveClose:
            self.facade._data = self.splitcolumntable
            self.update_data.emit('update')
            self.close()
