from PyQt4 import QtGui
from poplerGUI import class_inputhandler as ini
from Views import ui_dialog_addsitecolumn as addcol
from poplerGUI.logiclayer import class_helpers as hlp

class AddSiteColumnDialog(QtGui.QDialog, addcol.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Facade set up for the taxa dialog
        # box. These inputs will have been already
        # logged in the computer in order to
        # reach this phase
        self.sitelabel = None
        self.facade = None
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
