from PyQt4 import QtGui, QtCore
from pandas import read_sql
from poplerGUI import ui_dialog_main as dmainw
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from logiclayer import class_helpers as hlp
from logiclayer.datalayer import config as orm

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
        if self.maintablemod is None:
            self.facade.input_register(self.mainini)
            self.maindirector = self.facade.make_table('maininfo')
            self.facade.create_log_record('maintable')
            self._log = self.facade._tablelog['maintable']
            self.maintable = (
                self.maindirector._availdf.copy().reset_index(
                    drop=True))

        else:
            self.maintable = self.mainmodel.data(
                None, QtCore.Qt.UserRole).reset_index()

        self.mainmodel = self.viewEdit(self.maintable)
        self.tabviewMetadata.setModel(self.mainmodel)

    def submit_change(self):
        self.maintablemod = self.mainmodel.data(
            None, QtCore.Qt.UserRole).reset_index(drop=True)
        self.facade.push_tables['maintable'] = self.maintablemod
        self._log.debug(
            'maintable mod: ' +
            ' '.join(self.maintablemod.columns.values.tolist()))
        try:
            session = orm.Session()
            maincheck = session.query(
                orm.Maintable.metarecordid).order_by(
                    orm.Maintable.metarecordid)
            maincheckdf = read_sql(
                maincheck.statement, maincheck.session.bind)
            metaid_entered = maincheckdf[
                'metarecordid'].values.tolist()
            if self.facade._valueregister[
                    'globalid'] in metaid_entered:
                self.message.about(
                    self, 'Status',
                    'Metarecord ID is already present in database')
                return
            else:
                pass

            orm.convert_types(self.maintable, orm.maintypes)
            orm.convert_types(self.maintablemod, orm.maintypes)            
            hlp.updated_df_values(
                self.maintable, self.maintablemod,
                self._log, 'maintable')
            self.close()

        except Exception as e:
            print(str(e))
            self.error.showMessage(
                'Global Id already present in database')
            raise AttributeError(
                'Global Id already present in database')
