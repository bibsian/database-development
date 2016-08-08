#! /usr/bin/env python
from PyQt4 import QtGui, QtCore
from pandas import read_sql, DataFrame, concat
from poplerGUI import ui_dialog_site as dsite
from poplerGUI import ui_logic_sitechange as chg
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer.datalayer import config as orm

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
            self.facade._data[
                self.siteloc['siteid']] = self.facade._data[
                    self.siteloc['siteid']].astype(str)
                
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
            site_in_db['siteid'].drop_duplicates(inplace=True)
            displayed_data = self.rawdata[
                ~self.siteloc['siteid'].isin(
                    site_in_db)].copy()
            displayed_data.drop_duplicates(inplace=True)
            self.sitetablemodel = self.viewEdit(displayed_data)
            self.listviewSiteLabels.setModel(self.sitetablemodel)

    def update_data(self):
        changed_df = self.sitetablemodel.data(
            None, QtCore.Qt.UserRole)
        changed_site_list = changed_df[
            'siteid'].drop_duplicates().values.tolist()

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
            '''
            Updating view in case spelling changes were made
            '''
            site_display_df = changed_df.drop_duplicates()
            print('Site display droped: ', site_display_df)
            self.sitetablemodel = self.viewEdit(site_display_df)
            self.listviewSiteLabels.setModel(self.sitetablemodel)
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
        changed_site_list = changed_df[
            'siteid'].drop_duplicates().values.tolist()

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
                s_not_in_databaase)].drop_duplicates()
        print('site df (val): ', site_display_df)

        self.sitetablemodel = self.viewEdit(site_display_df)
        self.listviewSiteLabels.setModel(self.sitetablemodel)

        self._log.debug(
            'sitelevels (validated block)' + ' '.join(
                self.sitelevels))

        self.sitelevels = self.sitetablemodel.data(
            None, QtCore.Qt.UserRole)['siteid'].values.tolist()
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
        site_unsorted = self.facade._data[
            self.siteloc[
                'siteid']].drop_duplicates().values.tolist()
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

