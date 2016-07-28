from PyQt4 import QtGui
from poplerGUI import ui_dialog_sitechange as uichange

class TablePreview(QtGui.QDialog, uichange.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
