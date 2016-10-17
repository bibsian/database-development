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
from Views import ui_dialog_splitcolumn as dsplitcolumn
from poplerGUI import ui_logic_preview as tprev
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI import class_inputhandler as ini

@pytest.fixture
def SplitColumnDialog(meta_handle_1_count, file_handle_wide_to_long,
        site_handle_wide_to_long):
    class SplitColumnDialog(QtGui.QDialog, dsplitcolumn.Ui_Dialog):
        '''
        User Logic to deal with split a column from one into two based
        on user supplied separator (currently regex does not work)
        '''
        update_data = QtCore.pyqtSignal(object)
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            # Facade set up for the taxa dialog
            # box. These inputs will have been already
                # logged in the computer in order to
            # reach this phase
            self.facade = face.Facade()
            self.facade.input_register(meta_handle_1_count)
            self.facade.meta_verify()
            self.facade.input_register(file_handle_wide_to_long)
            self.facade.load_data()
            self.facade.input_register(site_handle_wide_to_long)
            sitelevels = self.facade._data[
                self.facade._inputs['siteinfo'].lnedentry['study_site_key']
                ].drop_duplicates().values.tolist()
            self.facade.register_site_levels(sitelevels)

            # Place holders for user inputs
            self.splitcolumnlned = {}
            
            # Place holder: Data Model/ Data model view
            self.splitcolumnmodel = None
            self.viewEdit = view.PandasTableModel
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
                'value_columns':
                hlp.string_to_list(self.lnedValuecolumns.text()),
                'datatype_name': self.cboxDatatypecolumn.currentText()
            }
            self.splitcolumnini = ini.InputHandler(
                name='splitcolumn',
                lnedentry=self.splitcolumnlned
            )
            self.facade.input_register(self.splitcolumnini)
            self.facade.create_log_record('splitcolumn')
            self._log = self.facade._tablelog['splitcolumn']

            try:
                self.splitcolumntable = hlp.wide_to_long(
                    self.facade._data,
                    value_columns=self.splitcolumnlned['value_columns'],
                    value_column_name=self.splitcolumnlned['datatype_name']
                )
            except Exception as e:
                print(str(e))
                self.error.showMessage('Could not melt data: ', str(e))

            try:
                assert self.splitcolumnlned['datatype_name'] != 'NULL'
            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Invalid datatype column: ', str(e))
                return

            hlp.write_column_to_log(
                self.splitcolumnlned, self._log, 'splitcolumn')

            if sender is self.btnPreview:
                self.splitcolumnmodel = view.PandasTableModel(
                    self.splitcolumntable)
                self.preview.tabviewPreview.setModel(
                    self.splitcolumnmodel)
                self.preview.show()
            elif sender is self.btnSaveClose:
                self.facade._data = self.splitcolumntable
                self.update_data.emit('update')
                self.close()

    return SplitColumnDialog()

def test_dialog_site(qtbot, SplitColumnDialog):
    SplitColumnDialog.show()
    qtbot.addWidget(SplitColumnDialog)

    qtbot.stopForInteraction()
