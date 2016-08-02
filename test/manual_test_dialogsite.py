#!/usr/bin/env python
import pytest
import pytestqt
from pandas import read_sql, DataFrame, concat
from PyQt4 import QtGui, QtCore
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development" +
        "\\test\\")
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath)))
os.chdir(rootpath)
from test import ui_logic_sitechange as chg
from test import ui_logic_session as logicsess
from test import ui_dialog_site as dsite
from test import ui_mainrefactor as mw
from test import class_inputhandler as ini
from test import class_modelviewpandas as view

from test.logiclayer import class_helpers as hlp
from test.logiclayer import class_userfacade as face
from test.logiclayer.datalayer import config as orm


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
            self.siteloc = {'siteid': None}
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
            self.sitelned = {'siteid': self.lnedSiteID.text().strip()}
            self.siteloc['siteid'] = self.lnedSiteID.text().strip()
            self.facade.create_log_record('sitetable')        
            self._log = self.facade._tablelog['sitetable']

            try:
                self.facade._data[self.siteloc['siteid']]

            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    self.siteloc['siteid'] +
                    ' not in dataframe')
                raise KeyError(
                    self.siteloc['siteid'] +
                    ' not in dataframe')

            self.siteini = ini.InputHandler(
                name='siteinfo', tablename='sitetable',
                lnedentry=self.sitelned)
            self.facade.input_register(self.siteini)
            self.facade._valueregister['siteid'] = self.siteloc[
                'siteid']
            self.message.about(self, 'Status', 'Information recorded')

            if not self.saved:
                self.sitedirector = self.facade.make_table('siteinfo')
                self.rawdata = (
                    self.sitedirector._availdf.sort_values(by='siteid'))
            else:
                self.update()

            # Make table and Register site levels with facade 
            self.facade.register_site_levels(
                self.rawdata['siteid'].drop_duplicates().
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
                    orm.Sitetable.siteid).order_by(
                        orm.Sitetable.siteid)
                session.close()
                sitecheckdf = read_sql(
                    sitecheck.statement, sitecheck.session.bind)
                site_in_db = sitecheckdf['siteid'].values.tolist()

                self.sitetablemodel = self.viewEdit(
                    self.rawdata[~self.siteloc['siteid'].isin(
                        site_in_db)])
                self.listviewSiteLabels.setModel(self.sitetablemodel)

        def update_data(self):
            changed_df = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)
            changed_site_list = changed_df['siteid'].values.tolist()


            self._log.debug(
                'changed_site_list: ' + ' '.join(changed_site_list))
            self._log.debug('sitelevels list: ' + ' ' +
                            ' '.join(self.sitelevels))

            if len(changed_df) == 0:
                pass
            else:
                if len(self.sitelevels) == 0:
                    pass
                else:
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
                orm.Sitetable).order_by(
                    orm.Sitetable.siteid).filter(
                        orm.Sitetable.lterid ==
                        self.facade._valueregister['lterid'])
            session.close()
            sitecheckdf = read_sql(
                sitecheck.statement, sitecheck.session.bind)
            
            
            print('checker df: ', sitecheckdf)
            if sitecheckdf is not None:
                if len(sitecheckdf) == 0:
                   checker = True
                else:
                    records_entered = sitecheckdf[
                        'siteid'].values.tolist()
                    
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
                pass
            else:
                check_view = view.PandasTableModel(
                    sitecheckdf[sitecheckdf['siteid'].isin(check)])
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
            changed_site_list = changed_df['siteid'].values.tolist()


            query_match = self.sitequerymodel.data(
                    None, QtCore.Qt.UserRole)
            site_q_list = query_match['siteid'].values.tolist()

            s_not_in_databaase = [
                x for x in changed_site_list if x not in site_q_list
            ]
            self._log.debug(
                's_not_in_databaase: ' + ' '.join(s_not_in_databaase))

            site_display_df = changed_df[
                changed_df['siteid'].isin(
                    s_not_in_databaase)]
            print('site df (val): ', site_display_df)
            self.sitetablemodel = self.viewEdit(site_display_df)
            self.listviewSiteLabels.setModel(self.sitetablemodel)

            self.sitelevels = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)['siteid'].values.tolist()
            self._log.debug(
                'sitelevels (updated)' + ' '.join(self.sitelevels))
            self.querycheck = 'Checked'

        def save_close(self):
            self.update_data()
            
            session = orm.Session()
            sitecheck = session.query(
                orm.Sitetable.siteid).order_by(
                    orm.Sitetable.siteid)
            session.close()
            sitecheckdf = read_sql(
                sitecheck.statement, sitecheck.session.bind)

            changed_df = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)
            changed_site_list = changed_df['siteid'].values.tolist()

            final_check = [
                x for x in changed_site_list
                if x not in self.sitelevels]
            
            if len(final_check) == 0:
                pass
            else:
                try:
                    for i,item in enumerate(changed_site_list):
                        self.facade._data.replace(
                            {self.sitelevels[i]: item.rstrip()},
                            inplace=True)
                    self.preview_validate.show()

                except Exception as e:
                    print(str(e))
                    self._log.debug(str(e))
                    self.error.showMessage(
                        'could not alter levels (save block): ' +
                        str(e))

            if sitecheckdf is not None:
                if len(sitecheckdf) == 0:
                   checker = True
                else:
                    records_entered = sitecheckdf[
                        'siteid'].values.tolist()
                    check = [
                        x for x in
                        list(set(records_entered)) if
                        x in changed_site_list]
                    checker = (len(check) == 0)
            else:
                checker = True

            if checker is True:
                pass
            else:
                self._log.debug('SiteId present under different LTER')
                self.error.showMessage(
                    'Site abbreviations already in database ' +
                    'from an different LTER. Please modify ' +
                    'site abbreviations.')
                raise AttributeError(
                    'SiteID already present under different LTER')

            self.save_data = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)

            # Updating  site levels
            self.facade.register_site_levels(
                self.facade._data[
                    self.siteloc[
                        'siteid']].drop_duplicates().values.tolist())

            if len(self.save_data) == 0:
                self.save_data= self.save_data.append(
                    DataFrame(
                        {
                            'siteid':'NULL',
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
            self.facade.push_tables['sitetable'] = self.save_data

            hlp.write_column_to_log(
                self.sitelned, self._log, 'sitetable_c')

            oldsitetable = hlp.produce_null_df(
                len(self.save_data.columns),
                self.save_data.columns.values.tolist(),
                len(self.save_data),
                'nan'
            )
            hlp.updated_df_values(
                oldsitetable, self.save_data, self._log, 'sitetable'
            )

            self.site_unlocks.emit(self.facade._data)
            self._log.debug(
                'facade site levels' +
                ' '.join(self.facade._valueregister['sitelevels']))


            self.sitedirector = self.facade.make_table('siteinfo')
            self.rawdata = (
                self.sitedirector._availdf.sort_values(by='siteid'))
            self.facade.register_site_levels(
                self.rawdata['siteid'].drop_duplicates().
                values.tolist())
            self.sitelevels = self.facade._valueregister['sitelevels']

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

