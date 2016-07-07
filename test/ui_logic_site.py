#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
from pandas import read_sql, DataFrame, concat
from poplerGUI import ui_dialog_site as dsite
from poplerGUI import ui_logic_sitechange as chg
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from poplerGUI.logiclayer import class_helpers as hlp
from logiclayer.datalayer import config as orm

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

        # User facade composed from main window
        self.facade = None
        self.lter = None
        # Table Director to build site table from
        # Builder classes
        self.sitedirector = None
        self.siteloc = {'siteid': None}

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

        # Make table and Register site levels with facade 
        self.sitedirector = self.facade.make_table('siteinfo')
        self.rawdata = (
            self.sitedirector._availdf.sort_values(by='siteid'))
        self.facade.register_site_levels(
            self.rawdata['siteid'].drop_duplicates().
            values.tolist())

        # Performing query
        self.sitelevels = self.facade._valueregister['sitelevels']
        self._log.debug(
            'sitelevels (submit): ' + ' '.join(self.sitelevels))
        session = orm.Session()
        site_query = (
            session.query(orm.Sitetable).
            order_by(orm.Sitetable.siteid).
            filter(orm.Sitetable.siteid.in_(self.sitelevels)).
            filter(orm.Sitetable.lterid == self.lter))
        session.close()
        site_query_df = read_sql(
            site_query.statement, site_query.session.bind)
        self.sitequerymodel = self.view(
            site_query_df.sort_values(by='siteid'))
        self.tabviewDbSiteQuery.setModel(
            self.sitequerymodel)

        if site_query_df is None:
            s_query_list = []
        else:
            s_query_list = site_query_df['siteid'].values.tolist()
        self._log.debug(
            'site query (submit): ' + ' '.join(s_query_list))

        s_in_databaase = [
            x for x in self.sitelevels if x in s_query_list
        ]
        self._log.debug(
            'sites in db (submit): ' + ' '.join(s_in_databaase))

        if not s_in_databaase:
            self._log.debug('No sites in database')
            self.sitelevels_updated = self.rawdata[
                'siteid'].values.tolist()
            site_display_df = self.rawdata

        else:
            self._log.debug('Sites in database')
            self.sitelevels_updated = [
                x for x in self.sitelevels
                if x not in s_in_databaase
            ]
            site_display_df = self.rawdata[
                self.rawdata['siteid'].isin(
                    self.sitelevels_updated)] 

        self._log.debug(
            'sitelevels_updated (submit block): ' +
            ' '.join(self.sitelevels_updated))

        # Setting Table Model View
        self.sitetablemodel = self.viewEdit(site_display_df)
        self.listviewSiteLabels.setModel(self.sitetablemodel)
        self.facade.push_tables['sitetable'] = self.rawdata
        self.btnSiteID.setEnabled(False)


    def update_data(self):
        changed_df = self.sitetablemodel.data(
            None, QtCore.Qt.UserRole)
        changed_site_list = changed_df['siteid'].values.tolist()

        self._log.debug(
            'changed_site_list: ' + ' '.join(changed_site_list))

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
            self.validated()
        else:
            check_view = view.PandasTableModel(
            sitecheckdf[sitecheckdf['siteid'].isin(check)])
            self.preview_validate.tabviewPreview.setModel(
                check_view)
            self.preview_validate.show()

    def validated(self):
        self.preview_validate.close()
        changed_df = self.sitetablemodel.data(
            None, QtCore.Qt.UserRole)

        changed_site_list = changed_df['siteid'].values.tolist()

        for i,item in enumerate(changed_site_list):
            self.facade._data.replace(
                {self.sitelevels_updated[i]: item.rstrip()},
                inplace=True)

        self.rawdata = self.facade.make_table(
            'siteinfo')._availdf.sort_values('siteid')

        self.sitelevels = self.rawdata['siteid'].values.tolist()
        session = orm.Session()
        site_query = (
            session.query(orm.Sitetable).
            order_by(orm.Sitetable.siteid).
            filter(orm.Sitetable.siteid.in_(self.sitelevels)).
            filter(orm.Sitetable.lterid == self.lter))
        session.close()
        site_query_df = read_sql(
            site_query.statement, site_query.session.bind)
        s_query_list = site_query_df['siteid'].values.tolist()

        self.sitequerymodel = self.view(
            site_query_df.sort_values(by='siteid'))
        self.tabviewDbSiteQuery.setModel(
            self.sitequerymodel)
        s_in_databaase = [
            x for x in self.sitelevels if x in s_query_list
        ]

        if not s_in_databaase:
            self._log.debug('No sites in database (update)')
            self.sitelevels_updated = self.rawdata[
                'siteid'].values.tolist()
            site_display_df = changed_df[
                changed_df['siteid'].isin(
                    self.sitelevels_updated)]

        else:
            self._log.debug('Sites in database (update)')
            self.sitelevels_updated = [
                x for x in self.sitelevels
                if x not in s_in_databaase
            ]
            site_display_df = changed_df[
                changed_df['siteid'].isin(
                    self.sitelevels_updated)]

        self._log.debug(
            'updated_site_list (update block): ' +
            ' '.join(self.sitelevels_updated))


        # Setting Table Model View
        self.sitetablemodel = self.viewEdit(site_display_df)
        self.listviewSiteLabels.setModel(self.sitetablemodel)
        self.facade.push_tables['sitetable'] = self.rawdata
        self.btnSiteID.setEnabled(False)

        # Updating  site levels
        self.facade.register_site_levels(
            self.facade._data[
                self.siteloc[
                    'siteid']].drop_duplicates().values.tolist())

    def save_close(self):
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
        print(self.save_data)
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
        self.close()
