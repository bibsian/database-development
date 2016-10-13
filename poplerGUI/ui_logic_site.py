#! /usr/bin/env python
from PyQt4 import QtGui, QtCore
from pandas import read_sql, DataFrame, concat
from Views import ui_dialog_site as dsite
from poplerGUI import ui_logic_sitechange as chg
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer.datalayer import config as orm

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
        else:
            pass

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

        # Registering information to facade class
        self.siteini = ini.InputHandler(
            name='siteinfo', tablename='study_site_table',
            lnedentry=self.sitelned)
        self.facade.input_register(self.siteini)
        self.facade._valueregister['study_site_key'] = self.siteloc[
            'study_site_key']
        
        self.message.about(self, 'Status', 'Information recorded')

        # Making study_site_table
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

        # Registing info
        self.sitelevels = self.facade._valueregister['sitelevels']
        self._log.debug(
            'sitelevels (submit): ' + ' '.join(self.sitelevels))

        if not self.saved:
            # Setting Table Model View if this dialog box
            # has NOT been used and information has NOT been stored
            self.sitetablemodel = self.viewEdit(self.rawdata)
            self.listviewSiteLabels.setModel(self.sitetablemodel)
        else:
            # Setting table Model View if the dialog box has
            # been used and info has been saved
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
        # Handling and log any user changes
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
                self.facade._data[self.siteloc['study_site_key']].replace(
                    {self.sitelevels[i]: item.rstrip()},
                    inplace=True)
        except Exception as e:
            print(str(e))
            self._log.debug(str(e))
            self.error.showMessage(
                'could not alter levels: ' + str(e))

        # Query to check is study sites are in db
        session = orm.Session()
        sitecheck = session.query(
            orm.study_site_table.__table__).order_by(
                orm.study_site_table.study_site_key)
        session.close()
        sitecheckdf = read_sql(
            sitecheck.statement, sitecheck.session.bind)

        # Conditionals to make sure that no results were
        # returned or not and sets check object (checker)
        print('checker df: ', sitecheckdf)
        if sitecheckdf is not None:
            if len(sitecheckdf) == 0:
               checker = True
            else:
                # If there are matches for study sites
                # make a list of match names to be promt user
                # with
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

        # If there are matches and user confirms they
        # are the same site's in the database then accept
        # changes and query site id's again to make sure
        # no more shared study sites are left
        if checker == True:
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
        ''' 
        Class to double check study sites after accepting that
        study sites are shared
        '''
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
        '''
        Method to save the study_site_table as it is seen
        by the user (matching sites that were accepted by user 
        are removed from the saved table because it will be pushed)
        '''
        update_message = QtGui.QMessageBox.question(
            self,'Message', 'Did you update records?',
            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if update_message == QtGui.QMessageBox.No:
            return
        else:
            pass

        # Retrieve study_site_table data from user view
        save_data = self.sitetablemodel.data(
            None, QtCore.Qt.UserRole)
        self.save_data = save_data.drop_duplicates()
        print('saved data (initial): ', self.save_data)
        self.facade.register_site_levels(
            self.facade._data[
                self.siteloc[
                    'study_site_key']].drop_duplicates().values.tolist())

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
