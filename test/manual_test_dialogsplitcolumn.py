import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
import sys,os
from Views import ui_dialog_splitcolumn as dsplitcolumn
from poplerGUI import ui_logic_preview as tprev
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI import class_inputhandler as ini
rootpath = os.path.dirname(os.path.dirname( __file__ ))
end = os.path.sep
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)

@pytest.fixture
def SplitColumnDialog(meta_handle_1_count, file_handle_split_columns):
    class SplitColumnDialog(QtGui.QDialog, dsplitcolumn.Ui_Dialog):
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
            self.facade.input_register(file_handle_split_columns)
            self.facade.load_data()

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
            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Could split column: ' + str(e))

            hlp.write_column_to_log(
                self.splitcolumnlned, self._log, 'splitcolumn')

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

    return SplitColumnDialog()

def test_dialog_site(qtbot, SplitColumnDialog):
    SplitColumnDialog.show()
    qtbot.addWidget(SplitColumnDialog)

    qtbot.stopForInteraction()
