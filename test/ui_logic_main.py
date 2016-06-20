from PyQt4 import QtGui, QtCore
import ui_dialog_main as dmainw
import class_inputhandler as ini
import class_modelviewpandas as view
import config as orm

class MainDialog(QtGui.QDialog, dmainw.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.facade = None
        self.mainini = ini.InputHandler(
            name='maininfo', tablename='maintable')
        # Place holder: Data Model/ Data model view
        self.mainmodel = None
        self.viewEdit = view.PandasTableModelEdit
        # Placeholders: Data tables
        self.maintable = None
        self.maintablemod = None
        # Placeholder: Director (table builder), log
        self.maindirector = None
        self._log = None
        # Placeholder for maindata Orms
        self.mainorms = {}
        # Actions
        self.btnSaveClose.clicked.connect(self.submit_change)
        self.btnCancel.clicked.connect(self.close)

        self.error = QtGui.QErrorMessage()
    def set_data(self):
        '''
        Method to register user input with facade,
        request the formated table from the facade,
        invoke the logger,
        set the data model,
        set the data model viewer
        '''
        self.facade.input_register(self.mainini)
        self.maindirector = self.facade.make_table('maininfo')
        self._log = self.facade._tablelog['maintable']
        self.maintable = self.maindirector._availdf.copy()
        self.mainmodel = self.viewEdit(self.maintable)
        self.tabviewMetadata.setModel(self.mainmodel)

    def submit_change(self):
        self.maintablemod = self.mainmodel.data(
            None, QtCore.Qt.UserRole)
        print('retrieved edited data')
        print(self.maintable['siteid'])
        print(self.maintablemod['siteid'])

        try:
            orm.convert_types(self.maintablemod, orm.maintypes)
            for i in range(len(self.maintablemod)):
                self.mainorms[i] = orm.Maintable(
                    siteid=self.maintablemod.loc[i,'siteid'])
                orm.session.add(self.mainorms[i])
            orm.session.flush()
            for i in range(len(self.maintablemod)):
                dbupload = self.maintablemod.loc[
                    i,self.maintablemod.columns].to_dict()
                for key in dbupload.items():
                    setattr(self.mainorms[i], key[0], key[1])
            orm.session.flush()
            self.close()

        except Exception as e:
            print(str(e))
            self.error.showMessage(
                'Incorrect datatypes on main table')
            raise AttributeError(
                'Incorrect datatypes on maindata table')
