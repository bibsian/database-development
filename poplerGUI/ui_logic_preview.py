from PyQt4 import QtGui
from poplerGUI import ui_dialog_table_preview as uiprev

class TablePreview(QtGui.QDialog, uiprev.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnCancel.clicked.connect(self.close)
