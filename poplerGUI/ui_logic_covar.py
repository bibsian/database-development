#!/usr/bin/env python
from PyQt4 import QtGui
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as views
from poplerGUI import ui_logic_preview as tprev
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_dictionarydataframe as ddf
from Views import ui_dialog_covariate as covar

class CovarDialog(QtGui.QDialog, covar.Ui_Dialog):
    '''
    Class to handler the user input into the covariates
    dialog box i.e. verify inputs and format data.
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Attributes
        self.covarlned = {'columns': None}
        self.covarini = None
        self._log = None
        self.covardata = None
        self.covarmodel = None


        # Signals/slots
        self.btnColumns.clicked.connect(self.submit_change)
        self.btnPreview.clicked.connect(self.submit_change)
        self.btnSaveClose.clicked.connect(self.submit_change)
        self.btnCancel.clicked.connect(self.close)

        # Pop up widgets
        self.message = QtGui.QMessageBox
        self.error = QtGui.QErrorMessage()
        self.preview = tprev.TablePreview()

    def submit_change(self):
        sender = self.sender()
        self.covarlned['columns'] = hlp.string_to_list(
            self.lnedColumns.text()
        )

        self.covarini = ini.InputHandler(
            name='covarinfo', tablename='covartable',
            lnedentry=self.covarlned)

        self.facade.input_register(self.covarini)
        self.facade.create_log_record('covartable')
        self._log = self.facade._tablelog['covartable']

        if self.covarlned['columns'][0] == '':
            print('in pass')
            pass
        else:
            try:
                self.facade._data[self.covarlned['columns']]
            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Column names not valid: Check spacing ' +
                    'and headers.')
                raise ValueError('Column names are incorrect')

        try:
            self.covardata = ddf.DictionaryDataframe(
                self.facade._data, self.covarlned['columns']
            ).convert_records()
        except Exception as e:
            print(str(e))
            self._log.debug(str(e))
            self.error.showMessage('Could not concatenate columns')
            raise TypeError('Could not concatenate columns')

        self.facade.push_tables['covariates'] = self.covardata

        if sender is self.btnColumns:
            self.message.about(self, 'Status', 'Columns recorded')
        elif sender is self.btnPreview:
            self.covarmodel = views.PandasTableModelEdit(
                self.covardata)
            self.preview.tabviewPreview.setModel(self.covarmodel)
            self.preview.show()
        elif sender is self.btnSaveClose:
            hlp.write_column_to_log(
                self.covarlned, self._log, 'covartable')
            self.close()
