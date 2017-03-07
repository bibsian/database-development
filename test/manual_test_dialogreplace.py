import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
import sys,os
from Views import ui_dialog_replacevalue as dreplacevalue
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
def ReplaceValueDialog(meta_handle_1_count, file_handle_1_count):
    class ReplaceValueDialog(QtGui.QDialog, dreplacevalue.Ui_Dialog):
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
            self.replacevaluelned = {}
            
            # Place holder: Data Model/ Data model view
            self.replacevaluemodel = None
            self.viewEdit = view.PandasTableModelEdit(None)
            # Placeholders: Data tables
            self.replacevaluetable = None

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
            self.replacevaluelned = {
                'column_name':
                self.lnedColumnname.text().strip(),
                'value_from':
                self.lnedFrom.text(),
                'value_to':
                self.lnedTo.text().strip(),
                'all_columns': self.ckAllcolumns.isChecked()
            }
            self.replacevalueini = ini.InputHandler(
                name='replacevalue',
                lnedentry=self.replacevaluelned
            )
            self.facade.input_register(self.replacevalueini)
            self.facade.create_log_record('replacevalue')
            self._log = self.facade._tablelog['replacevalue']

            if self.previous_click is True:
                self.viewEdit = view.PandasTableModelEdit(None)
            else:
                pass

            try:
                if self.replacevaluelned['all_columns'] is True:
                    self.replacevaluetable = self.facade._data.replace(
                        {
                            self.replacevaluelned['value_from']:
                            self.replacevaluelned['value_to']
                        }
                    )
                else:
                    columntochange = self.replacevaluelned['column_name']
                    assert (columntochange is not '') is True
                    self.replacevaluetable = self.facade._data.replace(
                        {
                            columntochange: {
                                self.replacevaluelned['value_from']:
                                self.replacevaluelned['value_to']
                            }
                        }
                    )
                self.previous_click = True
            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Could not replace values: ' + str(e))

            hlp.write_column_to_log(
                self.replacevaluelned, self._log, 'replacevalue')

            if sender is self.btnPreview:
                self.viewEdit.set_data(
                    self.replacevaluetable)
                self.preview.tabviewPreview.setModel(
                    self.viewEdit)
                self.preview.show()
            elif sender is self.btnSaveClose:
                self.facade._data = self.replacevaluetable
                self.update_data.emit('update')
                self.close()

    return ReplaceValueDialog()

def test_dialog_site(qtbot, ReplaceValueDialog):
    ReplaceValueDialog.show()
    qtbot.addWidget(ReplaceValueDialog)

    qtbot.stopForInteraction()
