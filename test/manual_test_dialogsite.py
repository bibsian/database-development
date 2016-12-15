#!/usr/bin/env python
import pytest
import pytestqt
from pandas import read_sql, DataFrame, concat, read_csv, to_numeric
from PyQt4 import QtGui, QtCore
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    end = "\\"
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
        '''
        This class contains the logic for dealing with the
        dialog box for study sites. Users must fill out this
        dialog box in order to move onto the rest of the tables
        '''

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
            self.site_table_data_to_upload_to_db = None
            self.sitetabledata = None
            self.sitelevels_submit_block = None
            self.sitelevels_change_block = None
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
            self.updated_from_query_matches = False
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
            self.btnChange.clicked.connect(self.change_site_label)
            self.btnUpdate.clicked.connect(self.update_data)
            self.previous_save = False
            
        def submit_change(self):

            self.lter = self.facade._valueregister['lterid']
            # Pull data from the study site form and check for
            # column match
            self.sitelned = {'study_site_key': self.lnedSiteID.text().strip()}
            self.siteloc['study_site_key'] = self.lnedSiteID.text().strip()

            try:
                self.facade.create_log_record('study_site_table')
                self._log = self.facade._tablelog['study_site_table']

            except Exception as e:
                print(str(e))
                self.error.showMessage(
                    'Session information was not verified.' +
                    ' Go to the session form and verify data: ' +
                    str(e)
                )

            if self.ckCreate.isChecked() is True:
                self.facade._data[self.siteloc[
                    'study_site_key']] = self.siteloc['study_site_key']
                self.facade._data['og_study_site_key'] = self.siteloc['study_site_key']

            else:
                pass

            try:
                self.facade._data[
                    self.siteloc['study_site_key']] = self.facade._data[
                        self.siteloc['study_site_key']].astype(str)
                self.facade._data['og_study_site_key'] = self.facade._data[
                        self.siteloc['study_site_key']].copy()
            except Exception as e:
                print(str(e))
                self._log.debug(str(e))
                self.error.showMessage(
                    self.siteloc['study_site_key'] +
                    ' not in dataframe')
                raise KeyError(
                    self.siteloc['study_site_key'] +
                    ' not in dataframe')

            # Registering information to facade class
            self.siteini = ini.InputHandler(
                name='siteinfo', tablename='study_site_table',
                lnedentry=self.sitelned)
            self.facade.input_register(self.siteini)
            self.facade._valueregister['study_site_key'] = self.siteloc[
                'study_site_key']
            self.message.about(self, 'Status', 'Information recorded')

            # Making study_site_table

            self.sitedirector = self.facade.make_table('siteinfo')
            self.site_table_data_to_upload_to_db = (
                self.sitedirector._availdf)


            self.facade.register_site_levels(
                self.facade._data[self.siteloc['study_site_key']].drop_duplicates().values.tolist()
            )
            # Registing info
            self.sitelevels_submit_block = self.site_table_data_to_upload_to_db['study_site_key']
            self._log.debug(
                'sitelevels (submit): ' + ' '.join(self.sitelevels_submit_block))

            # Setting Table Model View if this dialog box
            # has NOT been used and information has NOT been stored
            self.sitetablemodel = self.viewEdit(self.site_table_data_to_upload_to_db.copy())
            self.listviewSiteLabels.setModel(self.sitetablemodel)
            self.listviewSiteLabels.resizeColumnsToContents()


        def change_site_label(self):
            ''' Method to facilitate the renaming of site labels that
            are obvious errors (due to caps, spaces, etc)'''
            # Handling and log any user changes
            changed_df = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)
            print('changed site list in change block: ', changed_df)
            changed_site_list = changed_df[
                'study_site_key'].values.tolist()
            self._log.debug(
                'changed_site_list: ' + ' '.join(changed_site_list))
            self._log.debug('sitelevels list: ' + ' ' +
                            ' '.join(self.sitelevels_submit_block))

            if (
                    len(self.sitelevels_submit_block) == len(changed_site_list)
            ):
                try:

                    print(
                        'sitelevels before replace: ',
                        self.facade._data[self.siteloc['study_site_key']].drop_duplicates()
                    )


                    index = [
                        i for i,x in
                        enumerate(self.sitelevels_submit_block) if
                        x != changed_site_list[i]
                    ]

                    change_from = [
                        self.sitelevels_submit_block[i] for i in index]
                    change_to = [
                        changed_site_list[i] for i in index]
                    
                    change_dictionary = dict(
                        zip(change_from, change_to))

                    
                    # Replace labels with new ones
                    self.facade._data[self.siteloc['study_site_key']].replace(
                        change_dictionary,
                        inplace=True)

                    print(
                        'sitelevels after replace: ',
                        self.facade._data[self.siteloc['study_site_key']].drop_duplicates()
                    )

                    self.sitedirector = self.facade.make_table('siteinfo')
                    self.site_table_data_to_upload_to_db = (
                        self.sitedirector._availdf)

                    print('checking if update from query matches is T/F')
                    if self.updated_from_query_matches == False:
                        # Make table and Register site levels with facade
                        self.facade.register_site_levels(
                            self.facade._data[self.siteloc[
                                'study_site_key']].drop_duplicates().values.tolist())
                    else:
                        pass

                    self.sitelevels_submit_block = self.site_table_data_to_upload_to_db[
                        'study_site_key'].values.tolist()
                    # Adjusting view
                    print('Arriving at view set in change block')
                    self.sitetablemodel = self.viewEdit(
                        self.site_table_data_to_upload_to_db)
                    self.listviewSiteLabels.setModel(self.sitetablemodel)
                    self.listviewSiteLabels.resizeColumnsToContents()

                except Exception as e:
                    print(str(e))
                    self._log.debug(str(e))
                    self.error.showMessage(
                        'could not alter levels: ' + str(e))
            else:
                self.error.showMessage(
                    'Site levels changes cannot be made: Restart site entries.'
                )

        def update_data(self):
            '''
            Method to check whether the study sites (study_site_key)
            have already been uploaded into the database; either from
            the same LTER or different LTER's.

            If there are matches it updates the query view table class
            AND prompts the user to check if the sites about to be
            entered are exactly the same site as in the db (so
            studies can be joined by similar LTER study site locations)

            Note, if the user changes one of the site names, this
            method will account for that before the 'check' begins
            '''
            
            # Query to check is study sites are in db
            session = orm.Session()
            sitecheck = session.query(
                orm.study_site_table.__table__).order_by(
                    orm.study_site_table.study_site_key).filter(
                        orm.study_site_table.study_site_key.in_(
                            self.sitelevels_submit_block)
                    )
            session.close()
            site_df_from_query = read_sql(
                sitecheck.statement, sitecheck.session.bind)

            # Conditionals to make sure that no results were
            # returned or not and sets check object (checker)
            # First conditional is in case the database is empty
            # and/or query returns None
            print('checker df: ', site_df_from_query)
            if site_df_from_query is not None:
                if site_df_from_query.empty is True:
                    no_site_matches_from_db = True
                else:
                    # If there are matches for study sites
                    # make a list of match names to be promt user
                    # with
                    no_site_matches_from_db = False
                    site_matches_from_db = site_df_from_query[
                        'study_site_key'].values.tolist()
            else:
                no_site_matches_from_db = True
            print('no_site_matches_from_db status: ', no_site_matches_from_db)

            # If there are matches and user confirms they
            # are the same site's in the database then accept
            # changes and query site id's again to make sure
            # no more shared study sites are left
            if no_site_matches_from_db == True:
                self.sitetablemodel = self.viewEdit(
                    self.site_table_data_to_upload_to_db.applymap(str))
                self.listviewSiteLabels.setModel(self.sitetablemodel)

            else:
                query_matches_view = view.PandasTableModel(
                    site_df_from_query[site_df_from_query['study_site_key'].isin(
                        site_matches_from_db)])
                self.preview_validate.tabviewPreview.setModel(
                    query_matches_view)
                self.sitequerymodel = query_matches_view
                self.tabviewDbSiteQuery.setModel(self.sitequerymodel)
                self.tabviewDbSiteQuery.resizeColumnsToContents()
                self.preview_validate.show()

        def validated(self):
            ''' 
            Class to double check study sites after accepting that
            study sites are shared
            '''
            
            self.preview_validate.close()
            self.preview_validate.close()

            # Queried df
            site_matches_from_db = self.sitequerymodel.data(
                None, QtCore.Qt.UserRole)
            old_site_list = self.sitelevels_submit_block
            self.sitelevels_updated = [
                x for x in old_site_list
                if x not in
                site_matches_from_db['study_site_key'].values.tolist()]
            print('site levels in updated block: ', self.sitelevels_updated)
            
            # Site table view df
            changed_df = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)
            site_display_df = changed_df[
                changed_df['study_site_key'].isin(
                    self.sitelevels_updated)].drop_duplicates()
            print('site df (val): ', site_display_df)
            self.sitetablemodel = self.viewEdit(site_display_df)
            self.listviewSiteLabels.setModel(self.sitetablemodel)
            self.listviewSiteLabels.resizeColumnsToContents()
            self.updated_from_query_matches = True
            self._log.debug(
                'sitelevels (validated block)' + ' '.join(
                    self.sitelevels_submit_block))
            self._log.debug(
                'sitelevels (updated)' + ' '.join(self.sitelevels_updated))


        def save_close(self):
            '''
            Method to save the study_site_table as it is seen
            by the user (matching sites that were accepted by user 
            are removed from the saved table because it will be pushed)
            '''
            self.updated_from_query_matches = False

            # Retrieve study_site_table data from user view
            self.save_data = self.sitetablemodel.data(
                None, QtCore.Qt.UserRole)

            self.save_query = self.sitequerymodel.data(
                None, QtCore.Qt.UserRole)
            
            # If there are no site because they are already
            # in the database then create an empty dataframe
            if len(self.save_data) == 0:
                self.save_data= self.save_data.append(
                    DataFrame(
                        {
                            'study_site_key':'NULL',
                            'lat_study_site': 'nan',
                            'lng_study_site': 'nan',
                            'descript': 'NULL'
                        }, index=[0])
                )
            else:
                pass

            # Append dataframe with current LTER 
            lterid_df = hlp.produce_null_df(
                1, ['lter_table_fkey'], len(self.save_data), self.lter)
            print(lterid_df)
            self.save_data = concat(
                [self.save_data, lterid_df]
                , axis=1).reset_index(drop=True)


            #Convert types and strip stings
            numeric_cols = ['lat_study_site', 'lng_study_site']
            self.save_data[
                self.save_data.columns.difference(numeric_cols)] = self.save_data[
                    self.save_data.columns.difference(numeric_cols)].applymap(str)
            self.save_data[
                self.save_data.columns.difference(numeric_cols)] = self.save_data[
                    self.save_data.columns.difference(numeric_cols)].applymap(
                        lambda x: x.strip())
            self.save_data[numeric_cols] = to_numeric(
                self.save_data[numeric_cols], errors='coerce')

            print('Pushed dataset: ', self.save_data)
            self.facade.push_tables['study_site_table'] = self.save_data

            # Helpers to keep track of user changes to site names
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

            # Signal to confim this form has been completed and
            # user can move on to other tables
            self.site_unlocks.emit(self.facade._data)
            self._log.debug(
                'facade site levels' +
                ' '.join(self.facade._valueregister['sitelevels']))
            self._log.debug(
                'siteleves Query Saved ' +
                ' '.join(self.save_query['study_site_key'].values.tolist()))
            self._log.debug(
                'sitelevels (Save Block): ' +
                ' '.join(self.save_data['study_site_key'].values.tolist()))
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

            self.mdiArea.addSubWindow(self.subwindow_2)
            self.mdiArea.addSubWindow(self.subwindow_1)

            metadf = read_csv(
                rootpath + end + 'data' + end +
                'Cataloged_Data_Current_sorted.csv', encoding='iso-8859-11')
            metamodel = view.PandasTableModel(
                metadf[
                    ['global_id', 'lter', 'title', 'site_metadata']
                ]
            )
            self.tblViewMeta.setModel(metamodel)


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
