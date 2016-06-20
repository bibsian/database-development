from PyQt4 import QtGui
import ui_dialog_table_preview as dprev


class PreviewDialog(QtGui.QDialog, dprev.Ui_Dialog):
    '''
    Dialog box prompts the user to inpute
    unique metadata relating to the file that
    will be loaded. Also select and load file into
    rawdata viewer
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnCancel.clicked.connect(self.close)
