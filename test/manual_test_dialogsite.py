#!/usr/bin/env python
import pytest
import pytestqt
from pandas import read_sql, DataFrame, concat
from PyQt4 import QtGui, QtCore
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)
from poplerGUI import ui_logic_sitechange as chg
from poplerGUI import ui_logic_session as logicsess
from Views import ui_dialog_site as dsite
from Views import ui_mainrefactor as mw
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view

from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer.datalayer import config as orm


@pytest.fixture
def MainWindow():
    class SiteDialog(QtGui.QDialog, dsite.Ui_Dialog):

        site_unlocks = QtCore.pyqtSignal(object)

        def __init__(self,  parent=None):
            super().__init__(parent)
            self.setupUi(self)

            # Placeholders
            # user input for dialog box
            # logging class
            self.siteini = None
            self._log = None
            self._data = None
            self.sitelned = None

            # Placeholders:
            # Site Table from Raw data
            # and Site Table after edits
            self.rawdata = None
            self.sitetabledata = None
            self.sitelevels = None
            self.sitelevels_updated = None

            # Place holder for sqlalchemy Orms
            self.siteorms = {}

            # Viewer Classes (editable and not)
            self.viewEdit = view.PandasTableModelEdit
            self.view = view.PandasTableModel

            # Placeholders for data model classes for viewers:
            # Original data model
            # Database query model
            # Data model if updated from query
            self.sitetablemodel = None
            self.sitequerymodel = None
            self.querycheck = None
            # User facade composed from main window
            self.facade = None
            self.lter = None

            # Table Director to build site table from
            # Builder classes
            self.sitedirector = None
            self.siteloc = {'study_site_key': None}
            self.saved = []
            # Status Message
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox
            self.preview_validate = chg.TablePreview()
            self.preview_validate.btnAccept.clicked.connect(
                self.validated)
            self.preview_validate.btnCancel.clicked.connect(
                self.preview_validate.close)

            # Signals and slots
            self.btnSiteID.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.save_close)
            self.btnSkip.clicked.connect(self.close)
            self.btnUpdate.clicked.connect(self.update_data)
            self.previous_save = False
            
        def submit_change(self):

            self.lter = self.facade._valueregister['lterid']

            # Registering information to facade class
            self.sitelned = {'study_site_key': self.lnedSiteID.text().strip()}
            self.siteloc['study_site_key'] = self.lnedSiteID.text().strip()
            self.facade.create_log_record('study_site_table')        
            self._log = self.facade._tablelog['study_site_table']

            try:
                self.facade._data[
                    self.siteloc['study_site_key']] = self.facade._data[
                    self.siteloc['study_site_key']].astype(str)

            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    self.siteloc['study_site_key'] +
                    ' not in dataframe')
                raise KeyError(
                    self.siteloc['study_site_key'] +
                    ' not in dataframe')

            self.siteini = ini.InputHandler(
                name='siteinfo', tablename='study_site_table',
                lnedentry=self.sitelned)
            self.facade.input_register(self.siteini)
            self.facade._valueregister['study_site_key'] = self.siteloc[
                'study_site_key']
            self.message.about(self, 'Status', 'Information recorded')

            if not self.saved:
                self.sitedirector = self.facade.make_table('siteinfo')
                self.rawdata = (
                    self.sitedirector._availdf.sort_values(by='study_site_key'))
            else:
                self.update()

            # Make table and Register site levels with facade 
            self.facade.register_site_levels(
                self.rawdata['study_site_key'].drop_duplicates().
                values.tolist())

            # Performing query
            self.sitelevels = self.facade._valueregister['sitelevels']
            self._log.debug(
                'sitelevels (submit): ' + ' '.join(self.sitelevels))
            
            if not self.saved:
                # Setting Table Model View
                self.sitetablemodel = self.viewEdit(self.rawdata)
                self.listviewSiteLabels.setModel(self.sitetablemodel)
            else:
                session = orm.Session()
                sitecheck = session.query(
                    orm.study_site_table.study_site_key).order_by(
                        orm.study_site_table.study_site_key)
                session.close()
                sitecheckdf = read_sql(
                    sitecheck.statement, sitecheck.session.bind)
                site_in_db = sitecheckdf['study_site_key'].values.tolist()
                site_in_db['study_site_key'].drop_duplicates(inplace=True)
                displayed_data = self.rawdata[
                    ~self.siteloc['study_site_key'].isin(
                        site_in_db)].copy()
                displayed_data.drop_duplicates(inplace=True)
                self.sitetablemodel = self.viewEdit(displayed_data)
                self.listviewSiteLabels.setModel(self.sitetablemodel)

        def update_data(self):
            changed_df = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)
            changed_site_list = changed_df[
                'study_site_key'].drop_duplicates().values.tolist()

            self._log.debug(
                'changed_site_list: ' + ' '.join(changed_site_list))
            self._log.debug('sitelevels list: ' + ' ' +
                            ' '.join(self.sitelevels))

            try:
                for i,item in enumerate(changed_site_list):
                    self.facade._data.replace(
                        {self.sitelevels[i]: item.rstrip()},
                        inplace=True)
            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'could not alter levels: ' + str(e))

            session = orm.Session()
            sitecheck = session.query(
                orm.study_site_table).order_by(
                    orm.study_site_table.study_site_key).filter(
                        orm.study_site_table.lterid ==
                        self.facade._valueregister['lterd'])
            session.close()
            sitecheckdf = read_sql(
                sitecheck.statement, sitecheck.session.bind)


            print('checker df: ', sitecheckdf)
            if sitecheckdf is not None:
                if len(sitecheckdf) == 0:
                   checker = True
                else:
                    records_entered = sitecheckdf[
                        'study_site_key'].values.tolist()

                    check = [
                        x for x in
                        list(set(records_entered)) if
                        x in changed_site_list]
                    print('check list: ', check)
                    print('test check: ', len(check) == 0)
                    checker = (len(check) == 0)
            else:
                checker = True

            print('checker status: ', checker)
            if checker == True:
                '''
                Updating view in case spelling changes were made
                '''
                site_display_df = changed_df.drop_duplicates()
                print('Site display droped: ', site_display_df)
                self.sitetablemodel = self.viewEdit(site_display_df)
                self.listviewSiteLabels.setModel(self.sitetablemodel)
            else:
                check_view = view.PandasTableModel(
                    sitecheckdf[sitecheckdf['study_site_key'].isin(check)])
                self.preview_validate.tabviewPreview.setModel(
                    check_view)
                self.sitequerymodel = check_view
                self.tabviewDbSiteQuery.setModel(self.sitequerymodel)
                self.sitelevels = changed_site_list
                self.preview_validate.show()


        def validated(self):
            self.preview_validate.close()

            changed_df = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)
            changed_site_list = changed_df[
                'study_site_key'].drop_duplicates().values.tolist()

            query_match = self.sitequerymodel.data(
                    None, QtCore.Qt.UserRole)
            site_q_list = query_match['study_site_key'].values.tolist()

            s_not_in_databaase = [
                x for x in changed_site_list if x not in site_q_list
            ]
            self._log.debug(
                's_not_in_databaase: ' + ' '.join(s_not_in_databaase))

            site_display_df = changed_df[
                changed_df['study_site_key'].isin(
                    s_not_in_databaase)].drop_duplicates()
            print('site df (val): ', site_display_df)

            self.sitetablemodel = self.viewEdit(site_display_df)
            self.listviewSiteLabels.setModel(self.sitetablemodel)

            self._log.debug(
                'sitelevels (validated block)' + ' '.join(
                    self.sitelevels))

            self.sitelevels = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)['study_site_key'].values.tolist()
            self._log.debug(
                'sitelevels (updated)' + ' '.join(self.sitelevels))
            self.querycheck = 'Checked'

        def save_close(self):
            update_message = QtGui.QMessageBox.question(
                self,'Message', 'Did you update records?',
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if update_message == QtGui.QMessageBox.No:
                return
            else:
                pass

            save_data = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)
            self.save_data = save_data.drop_duplicates()
            print('saved data (initial): ', self.save_data)
            # Updating  site levels
            self.facade.register_site_levels(
                self.facade._data[
                    self.siteloc[
                        'study_site_key']].drop_duplicates().values.tolist())

            if len(self.save_data) == 0:
                self.save_data= self.save_data.append(
                    DataFrame(
                        {
                            'study_site_key':'NULL',
                            'lat': 'nan',
                            'lng': 'nan',
                            'descript': 'NULL'
                        }, index=[0])
                )
            else:
                pass

            lterid_df = hlp.produce_null_df(
                1, ['lterid'], len(self.save_data), self.lter)
            print(lterid_df)

            self.save_data = concat(
                [self.save_data, lterid_df]
                , axis=1).reset_index(drop=True)
            print('Pushed dataset: ', self.save_data)
            self.facade.push_tables['study_site_table'] = self.save_data

            hlp.write_column_to_log(
                self.sitelned, self._log, 'study_site_table_c')

            oldsitetable = hlp.produce_null_df(
                len(self.save_data.columns),
                self.save_data.columns.values.tolist(),
                len(self.save_data),
                'nan'
            )
            hlp.updated_df_values(
                oldsitetable, self.save_data, self._log, 'study_site_table'
            )

            self.site_unlocks.emit(self.facade._data)
            site_unsorted = self.facade._data[
                self.siteloc[
                    'study_site_key']].drop_duplicates().values.tolist()
            site_unsorted.sort()
            self.sitelevels = site_unsorted

            self._log.debug(
                'facade site levels' +
                ' '.join(self.facade._valueregister['sitelevels']))

            self._log.debug(
                'sitelevels (Save Block): ' +
                ' '.join(self.sitelevels))

            self.saved.append(1)
            self.close()



    class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
        '''
        The main window class will serve to gather all informatoin
        from Dialog boxes, actions, and instantiate classes
        that are required to perform the necessary lower level logic
        (i.e. implement a Facade, Commander, MetaVerifier, etc.
        '''

        def __init__(self, parent=None):
            super().__init__(parent)
            # attributes
            self.setupUi(self)

            # ------- SITE DIALOG CONSTRUCTOR ARGS ----- #
            self.facade = face.Facade()
            self.dsite = SiteDialog()
            # Actions
            self.actionSiteTable.triggered.connect(self.site_display)
            # Custom Signals
            self.dsite.site_unlocks.connect(self.site_complete_enable)
            self.dsite.update_data
            
            # ------ SESSION DIALOG CONSTRUCTOR ARGS ----- #
            # Dialog boxes for user feedback
            self.dsession = logicsess.SessionDialog()
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox
            # Custom signals
            self.dsession.raw_data_model.connect(
                self.update_data_model)
            # actions
            self.actionStart_Session.triggered.connect(
                self.session_display)


        def update_data_model(self):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)
            

        def session_display(self):
            ''' Displays the Site Dialog box'''
            self.dsession.show()
            self.dsession.facade = self.facade
        # ------- END SESSION DIAGLOG CODE --------#

        # -------- START SITE DIALOG CODE ---------#

        @QtCore.pyqtSlot(object)
        def site_complete_enable(self, datamod):
            ''' 
            Method to enable actions for display dialog 
            boxes that corresond to different database tables
            '''
            self.actionMainTable.setEnabled(True)
            self.actionTaxaTable.setEnabled(True)
            self.actionTimeFormat.setEnabled(True)
            self.actionRawTable.setEnabled(True)
            self.actionCovariates.setEnabled(True)
            self.update_data_model()

        def site_display(self):
            ''' Displays the Site Dialog box'''
            self.dsite.show()
            self.dsite.facade = self.facade

    return UiMainWindow()

    
def test_dialog_site(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()

