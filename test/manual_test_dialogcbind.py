import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = '/'
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    end = '\\'
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)
from Views import ui_dialog_cbind as dcbind
from poplerGUI import ui_logic_preview as tprev
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI import class_inputhandler as ini

@pytest.fixture
def CbindDialog(meta_handle_1_count, file_handle_1_count):
    class CbindDialog(QtGui.QDialog, dcbind.Ui_Dialog):
        '''
        User Logic to deal with split a column from one into two based
        on user supplied separator (currently regex does not work)
        '''
        update_data = QtCore.pyqtSignal(object)
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            # Facade set up
            self.facade = face.Facade()
            self.facade.input_register(meta_handle_1_count)
            self.facade.meta_verify()
            self.facade.input_register(file_handle_1_count)
            self.facade.load_data()

            self.previous_click = False
            # Place holders for user inputs
            self.cbindlned = {}
            # Place holder: Data Model/ Data model view
            self.cbindmodel = None
            self.viewEdit = view.PandasTableModelEdit(None)
            # Placeholders: Data tables
            self.cbindtable = None
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
            self.cbindlned = {
                'column_1':
                self.lnedColumn1.text().strip(),
                'column_2':
                self.lnedColumn2.text().strip()
            }
            self.cbindini = ini.InputHandler(
                name='cbind',
                lnedentry=self.cbindlned
            )
            self.facade.input_register(self.cbindini)
            self.facade.create_log_record('cbind')
            self._log = self.facade._tablelog['cbind']

            if self.previous_click is True:
                self.viewEdit = view.PandasTableModelEdit(None)
            else:
                pass

            try:
                self.cbindtable = hlp.cbind(
                    self.facade._data,
                    self.cbindlned['column_1'],
                    self.cbindlned['column_2']
                )
            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Could combine column values: ' + str(e))

            hlp.write_column_to_log(
                self.cbindlned, self._log, 'cbind')

            if sender is self.btnPreview:
                self.viewEdit.set_data(
                    self.cbindtable)
                self.preview.tabviewPreview.setModel(
                    self.viewEdit)
                self.preview.show()
            elif sender is self.btnSaveClose:
                self.facade._data = self.cbindtable
                self.update_data.emit('update')
                self.close()

    return CbindDialog()

def test_dialog_site(qtbot, CbindDialog):
    CbindDialog.show()
    qtbot.addWidget(CbindDialog)

    qtbot.stopForInteraction()
