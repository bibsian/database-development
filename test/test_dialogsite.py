#!/usr/bin/env python
import pytest
import pytestqt
import pandas as pd
from PyQt4 import QtGui, QtCore
from collections import OrderedDict
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_logic_session as logicsess
import class_userfacade as face
import class_inputhandler as ini
import class_helpers as hlp
import class_flusher as flsh
import ui_dialog_site as dsite
import ui_mainrefactor as mw
import class_modelviewpandas as view
import config as orm


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
            self.rawdataog = None
            self.sitetabledata = None

            # Placeholders:
            # Queried Site Table from database
            # List of site factor levels that are present in database
            # Orms to populate Site Table information into database
            self.sitedbtable = None
            self.queryupdate = None

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
            self.sitedbtablemodel = None
            self.sitequerymodel = None

            #  Updated site factor level list
            self.sitemodlist = None

            # User facade composed from main window
            self.facade = None

            # Table Director to build site table from
            # Builder classes
            self.sitedirector = None
            self.siteloc = {'siteid': None}

            # Status Message
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox

            # Signals and slots
            self.btnSiteID.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.save_close)
            self.btnSkip.clicked.connect(self.close)
            self.btnUpdate.clicked.connect(self.update_data)

        def submit_change(self):
            '''
            Method to change factor levels of the raw
            data frame displayed on the MainWindow
            when the factor levels are modified by users.

            Additionally populates Site orms (self.siteorms)
            with final data and adds it to the orm.session

            More tabs in teh MainWindow are enabled once
            this dialog box is completed
            '''
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
            self.facade._valueregister['siteid'] = self.lnedSiteID.text(
                ).strip()
            self.message.about(
                self, 'Status', 'Information recorded')

            # Creating site table, initiating, logging
            # and register site levels with facade
            self.sitedirector = self.facade.make_table('siteinfo')
            self.facade.register_site_levels(
                self.sitedirector._availdf[
                    'siteid'].values.tolist())

            # Setting original data
            self.rawdataog = (
                self.sitedirector._availdf.sort_values(
                    by='siteid'))
            self.sitetablemodel = self.viewEdit(
                self.rawdataog)
            self.listviewSiteLabels.setModel(
                self.sitetablemodel)

            # Setting query table for site list data
            try:
                lterid = self.facade._valueregister['lterid']
                qsitecondition = self.sitetablemodel.data(
                    None, QtCore.Qt.UserRole)
                self.queryupdate = qsitecondition[
                    'siteid'].values.tolist()
                dbsites = orm.session.query(
                    orm.Sitetable).order_by(
                        orm.Sitetable.siteid).filter(
                        orm.Sitetable.siteid.in_(
                            self.queryupdate)).filter(
                                orm.Sitetable.lterid == lterid)
                self.sitedbtable = pd.read_sql(
                    dbsites.statement, dbsites.session.bind)
                self.sitequerymodel = self.view(
                    self.sitedbtable.sort_values(by='siteid'))
                self.tabviewDbSiteQuery.setModel(
                    self.sitequerymodel)

                # Setting updated table for site list
                # i.e. removing sites from list already present
                # in database
                if not self.sitedbtable.values.tolist():
                    # True if list is empty
                    pass
                else:
                    remove = self.rawdataog['siteid'].isin(
                        self.sitedbtable['siteid'].values.tolist())
                    self.rawdata = self.rawdataog[~remove]
                    self.sitedbtablemodel= self.viewEdit(
                        self.rawdataog[~remove])
                    self.listviewSiteLabels.setModel(
                        self.sitedbtablemodel)

            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Could not update site tables')
                raise LookupError(e)

        def update_data(self):
            '''
            Method to dynamically update the list of site
            information to be pushed to the database.
            These methods include dynamically updating
            query results as well as saving all modifications
            to site level names in persisten data
            if changed during the user interaction.
            '''
            lterid = self.facade._valueregister['lterid']

            site_data_director = self.facade.make_table('siteinfo')

            # Setting original data, site list, and dictionary
            original_data = site_data_director._availdf.copy()
            self.facade.push_tables['sitetable'] = original_data
            original_site_list = original_data[
                    'siteid'].values.tolist()
            original_site_list.sort()
            self._log.info('original site list: ', original_site_list)

            original_site_ordered = []
            for i in original_site_list:
                original_site_ordered.append((i, i))
            site_dict = OrderedDict(original_site_ordered)

            # Setting query data, sitelist
            dbquery = orm.session.query(
                orm.Sitetable).order_by(
                    orm.Sitetable.siteid).filter(
                            orm.Sitetable.lterid == lterid)

            database_data = pd.read_sql(
                dbquery.statement, dbquery.session.bind)
            database_site_list = database_data[
                'siteid'].values.tolist()
            self._log.info('database_site_list: ', database_site_list)

            # Setting database data, sitelist
            updated_data = self.sitedbtablemodel.data(
                None, QtCore.Qt.UserRole)
            updated_site_list = updated_data[
                'siteid'].values.tolist()
            self._log.info('updated_site_list: ', updated_site_list)

            user_modified_sites = [
                x for x in list(site_dict.keys())
                if x not in database_site_list and
                x not in updated_site_list
            ]
            self._log.info('user_modified_sites: ', user_modified_sites)

            not_in_db_change_site_to = [
                x for x in updated_site_list
                if x not in list(site_dict.keys()) and
                x not in original_site_list
            ]
            [
                not_in_db_change_site_to.append(x)
                for x in database_site_list
                if x not in list(site_dict.keys()) and
                x not in updated_site_list
            ]    
            self._log.info(
                'not_in_db_change_site_to: ',
                set(not_in_db_change_site_to))

            self._log.info(
                'about to enter modified sites list loop: ',
                user_modified_sites)
            for j, site_i in enumerate(
                    list(set(not_in_db_change_site_to))):
                sites_not_updated = [
                    x for x in list(site_dict.keys())
                    if x not in user_modified_sites
                ]
                self._log.info('site_i, not update: ',
                      site_i, sites_not_updated)
                self.facade.replace_levels(
                    'siteinfo', [site_i], sites_not_updated)
            self.submit_change()

        def save_close(self):
            '''
            Method to log data including logging whether all the 
            site information for a dataset 
            is already in the database (program logs nulls).
            '''
            lterid = self.facade._valueregister['lterid']
            print(lterid)
            try:
                if self.sitedbtablemodel is None:
                    self.sitedbtable = self.sitetablemodel.data(
                        None, QtCore.Qt.UserRole)
                else:
                    self.sitedbtable = self.sitedbtablemodel.data(
                        None, QtCore.Qt.UserRole)
                    print('sitedbtable: ', self.sitedbtable)

                if len(self.sitedbtable) == 0:
                    self.sitedbtable = self.sitedbtable.append(
                        pd.DataFrame(
                            {
                                'siteid':'NULL',
                                'lat': 'nan',
                                'lng': 'nan',
                                'descript': 'NULL'
                            }, index=[0])
                    )
                
                lterid_df = hlp.produce_null_df(
                    1, ['lterid'], len(self.sitedbtable), 'SBC')
                print(lterid_df)
                self.sitedbtable = pd.concat(
                    [self.sitedbtable, lterid_df]
                    , axis=1).reset_index(drop=True)
                print(self.sitedbtable)

            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    'Site column not set')
                raise AttributeError('Site column not set')

            if (len(self.sitedbtable) == 1):
                self._log.info('Skipping database transaction')
                pass
            else:
                self._log.info('Making database transaction')
                try:
                    
                    site_flush = flsh.Flusher(
                        self.sitedbtable, 'sitetable',
                        'siteid', self.facade._valueregister['lterid'])
                    ck = site_flush.database_check(
                        self.facade._valueregister['sitelevels'])                
                    if ck is True:
                        site_flush.go()
                    else:
                        raise AttributeError

                except Exception as e:
                    print(str(e))
                    self._log.debug(str(e))
                    raise AttributeError(
                        'Could not map to database')

            hlp.write_column_to_log(
                self.sitelned, self._log, 'sitetable_c')

            oldsitetable = hlp.produce_null_df(
                len(self.sitedbtable.columns),
                self.sitedbtable.columns.values.tolist(),
                len(self.sitedbtable),
                'nan'
            )
            hlp.updated_df_values(
                oldsitetable, self.sitedbtable, self._log, 'sitetable'
            )

            self.site_unlocks.emit(self.facade._data)
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

            # ------ SESSION DIALOG CONSTRUCTOR ARGS ----- #
            # Dialog boxes for user feedback
            self.dsession = logicsess.SessionDialog()
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox
            # Custom signals
            self.dsession.raw_data_model.connect(
                self.update_data_model)
            self.dsession.webview_url.connect(
                self.update_webview)
            # actions
            self.actionStart_Session.triggered.connect(
                self.session_display)

        def update_data_model(self):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)

        @QtCore.pyqtSlot(object)
        def update_webview(self, url):
            self.webView.load(QtCore.QUrl(url))

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

