# This python script is going to be used catch the
# signals emitted on the Site Names and Coorinates Form
# and process the information
import sys
sys.path.insert(0,"C:\\Users\\MillerLab\\Dropbox\\"
                "database-development\\GUI\\qtdesigner\\"
                "integratedui_design\\")
import UiMainWindow as ui


class ViewSitesFromRawDataBtn(ui.UiMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
    
