#! /usr/bin/env python
from collections import namedtuple
import os
import datetime as tm
from pandas import merge, concat, DataFrame, read_csv
from poplerGUI.logiclayer.class_metaverify import MetaVerifier
from poplerGUI.logiclayer.class_commanders import (
    LoadDataCommander, DataCommandReceiver,
    CommandInvoker, MakeProxyCommander, MakeProxyReceiver,
    CareTakerCommand, CareTakerReceiver)
from poplerGUI.logiclayer.class_helpers import UniqueReplace, check_registration
from poplerGUI.logiclayer.class_tablebuilder import (
    SiteTableBuilder, TableDirector, MainTableBuilder,
    TaxaTableBuilder, RawTableBuilder, UpdaterTableBuilder)
from poplerGUI.logiclayer import class_logconfig as log
from poplerGUI.logiclayer import class_flusher as flsh
from poplerGUI.logiclayer import class_merger as mrg
from poplerGUI.logiclayer.class_helpers import updated_df_values
from poplerGUI.logiclayer.datalayer import config as orm

all = ['Facade']

class Facade:
    '''
    This is the facade class to handle the interaction
    between the user inputs.

    Names of user input instances should be one of the following.
    Note, each name corresponds to unique block in the 
    facade class.

    # ---Program start--- #
    'fileoptions' = Handle session creation and data verification
    'metacheck' = Handles metadata verification

    # ---Data Modifications--- #
    'replace'


    # ---Table Concatenation--- #
    'sitetable'
    'taxatable'
    'rawtable'
    'climatesitetable'
    'climaterawtable'
    'timetable'
    'editdata'
    'dbquery'
    'dbpush'
    'dataproxy'
    'replace'

    Note:
    The class attribute 'input_manager' contains the 
    file caretaker (sessioncaretaker) and command 
    invoker (sessioninvoker). Everything preceeding
    it is setup requried to instantiate those classes
    '''        
    carecommand = CareTakerCommand(CareTakerReceiver())

    sessioninvoker = CommandInvoker(carecommand)
    sessioninvoker.load_file_caretaker()
    sessioncaretaker = carecommand._caretaker

    manager = namedtuple(
        'maanger', 'caretaker invoker')
    input_manager = manager(
        sessioncaretaker, sessioninvoker)

    def __init__(self):
        '''
        Initialize facade with a dictionary to track
        user inputs (for logging and session management).
        Class instances will be register with the 
        input dictionary. 

        A commandinvoker will be populating during
        the use of the program, tracking command histories

        In addtion a filecaretaker will be instantiated
        when a raw data file is loaded. This will help track
        changes to data
        '''
        self.clsinstance = None
        self._inputs = {}
        self._valueregister = {
            'globalid': None,
            'lterid': None,
            'siteid':None,
            'sitelevels': None
        }
        self._data = None
        self._dbtabledict = {
            'sitetable': SiteTableBuilder(),
            'maintable': MainTableBuilder(),
            'taxatable': TaxaTableBuilder(),
            'timetable': None,
            'rawtable': RawTableBuilder(),
            'covartable': None,
            'updatetable': UpdaterTableBuilder()
        }

        self._datamerged = {
            'raw_main': None,
            'raw_main_taxa': None
        }

        self._tablelog = {
            'sitetable': None,
            'maintable': None,
            'maintable_update': None,
            'timetable': None,
            'taxatable': None,
            'rawtable': None,
            'covartable': None,
            'climatesite': None,
            'climateobs': None
        }

        self._colinputlog = {
            'siteinfo': None,
            'maininfo': None,
            'taxainfo': None,
            'timeinfo': None,
            'rawinfo': None,
            'covarinfo': None
        }

        self.push_tables = {
            'sitetable': None,
            'maintable': None,
            'taxatable': None,
            'timetable': None,
            'rawtable': None,
            'covariates': None
        }

        self.pushtables = None
        self.sitepushed = None
        self.mainpushed = None
        self.taxapushed = None
        self.rawpushed = None

    def make_proxy_helper(self, data, label):
        proxycmd = MakeProxyCommander(
            MakeProxyReceiver(), data.reset_index(
                ), label)            
        self.input_manager.invoker.perform_commands = proxycmd
        self.input_manager.invoker.make_proxy_data()
        self.input_manager.caretaker.save_to_memento(
            proxycmd._proxy.create_memento())
        self._data = (
            self.input_manager.caretaker.restore_memento(
                label))
        print('Proxy Created')

    def input_register(self, clsinstance):
        '''
        Sets user instantiated classes into the facade
        _input dictionary.
        All other operations performed
        by the program will take the _inputs dictionary
        within methods to direct the behavior of the program
        '''
        self.clsinstance = clsinstance
        try:
            self._inputs[self.clsinstance.name] = self.clsinstance
        except:
            raise AttributeError(
                'Wrong class input for program facade.')

    def meta_verify(self):
        '''
        Adapter method:
        Takes 'fileoption' input and MetaVerifier class
        for logic checks.
        '''
        check_registration(self, 'metacheck')

        verifier = MetaVerifier(self._inputs['metacheck'])
        
        if self._inputs['metacheck'].verify is None:
            pass
        else:
            verifier._meta = read_csv((
                str(os.getcwd()) + 
                '/Datasets_manual_test/meta_climate_test.csv'),
                encoding='iso-8859-11')

        try:
            assert verifier.verify_entries()
        except Exception as e:
            raise AttributeError(str(e))

        self._valueregister['globalid'] = (
            self._inputs['metacheck'].lnedentry['globalid'])
        self._valueregister['lterid'] = (
            self._inputs['metacheck'].lnedentry['lter'])

        print('Input verified')


    def load_data(self):
        ''' Using commander classes to peform the following
        commands. Note All commands are executed by the
        self.input_manager attribute. This meas all
        commands are registered with the invoker and all
        loaded data is regeristered with the file caretaker

        1) Load Data via the LoadDataCommand (register with
        invoker and registed data loaded with file caretaker)

        2) Generate proxy data from MakeProxyCommander (
        register command with invoker and register proxy
        data with file caretaker)

        return a proxy of the original dataset loaded.

        '''
        try:
            assert self._inputs[
                'fileoptions'].filename is not None
        except:
            raise AttributeError('No file selected to load.')

        filecmd = LoadDataCommander(
            DataCommandReceiver(), self._inputs['fileoptions'])
        self.input_manager.invoker.perform_commands = filecmd            
        self.input_manager.invoker.load_file_process()

        dfile = filecmd._loadfileinst
        self.input_manager.caretaker.save_to_memento(
            dfile.create_memento())
        dfile.set_data(
            self.input_manager.caretaker, 'original')

        self.make_proxy_helper(dfile._data, 'proxydf')

        return self._data

    def register_site_levels(self, sitelevels):
        try:
            assert isinstance(sitelevels, list)
        except Exception as e:
            print(str(e))
            raise TypeError('Site levels input is not a list')

        sitelevels.sort()
        self._valueregister['sitelevels'] = sitelevels

    def view_unique(self, inputname):

        check_registration(self, inputname)    
        repinst = UniqueReplace(
            self._data, self._inputs[inputname])
        return repinst.get_levels()

    def replace_entry(self, inputname):
        ''' 
        Method to pass input to helper class and replace
        values in the dataframe.
        '''

        try:
            assert self._inputs[inputname].name == inputname
        except Exception as e:
            print(str(e))
            raise ValueError('Input Not Register')

        repinst = UniqueReplace(
            self._data, self._inputs[inputname])
        datamod = repinst.replace_values()

        self.make_proxy_helper(datamod, inputname)
        return self._data

    def replace_levels(self, inputname, modlist, removed=None):
        '''
        Method to replace factor levels with a user
        modified list of levels
        '''
        check_registration(self, inputname)

        replaceinst = UniqueReplace(
            self._data, self._inputs[inputname])
        replaceinst.get_levels()
        datamod = replaceinst.replace_levels(modlist, removed)
        self._data = datamod
        self.make_proxy_helper(datamod, inputname)

        return self._data

    def create_log_record(self, tablename):
        try:
            globalid = self._inputs['metacheck'].lnedentry['globalid']
            filename = os.path.split(
                self._inputs[
                    'fileoptions'].filename)[1]
            dt = (str(
                tm.datetime.now()).split()[0]).replace("-", "_")
        except Exception as e:
            print(str(e))
            raise AttributeError(
                'Global ID and data file not set')

        self._tablelog[tablename] =(
            log.configure_logger('tableformat',(
                'Logs_UI/{}_{}_{}_{}.log'.format(
                    globalid, tablename,filename,dt))))

    def make_table(self, inputname):
        '''
        Method to take user inputs and create dataframes
        that contain informatoin that will be pushed into 
        the database. The formating of the tables is handled by
        class_tablebuilder.py module.

        Additionally logging of table specific informatoin
        is initiated here.
        '''
        uniqueinput = self._inputs[inputname]
        tablename = self._inputs[inputname].tablename
        globalid = self._inputs['metacheck'].lnedentry['globalid']
        sitecol = self._inputs['siteinfo'].lnedentry['siteid']
        uqsitelevels = self._valueregister['sitelevels']

        director = TableDirector()           
        builder = self._dbtabledict[tablename]
        director.set_user_input(uniqueinput)
        director.set_builder(builder)

        if tablename != 'maintable':
            director.set_data(self._data)
        else:
            metaverify = MetaVerifier(self._inputs['metacheck'])
            metadata = metaverify._meta
            director.set_data(metadata.iloc[globalid-1,:])

        director.set_globalid(globalid)
        director.set_siteid(sitecol)
        director.set_sitelevels(uqsitelevels)

        return director.get_database_table()

    def merge_push_data(self):
        '''
        This method merges all tables from the user input
        to create commits the necessary joins for
        populating foreign keys
        '''
        if self.pushtables is None:
            pass
        else:
            return

        for i, item in enumerate(self.push_tables.values()):
            try:
                if list(self.push_tables.keys())[i] == 'sitetable':
                    pass
                else:
                    assert (item is not None) is True
            except Exception as e:
                print(str(e))
                raise AttributeError(
                    'Not all data tables have been completed: ' +
                    str(e))

        # Stored Variables required for merges
        globalid = self._valueregister['globalid']
        lter = self._valueregister['lterid']
        siteid = self._valueregister['siteid']
        sitelevels = self._valueregister['sitelevels']
        rawdata = self._data

        # User created database tables
        sitetable = self.push_tables['sitetable']
        maintable = self.push_tables['maintable']
        print(maintable)
        orm.convert_types(maintable, orm.maintypes)
        taxatable = self.push_tables['taxatable']
        print('taxatable (facade): ', taxatable)
        timetable = self.push_tables['timetable']
        rawtable = self.push_tables['rawtable']
        covartable = self.push_tables['covariates']
        print('rawtable (facade): ', rawtable)

        session = orm.Session()
        orm.convert_types(maintable, orm.maintypes)
        if (self.sitepushed is None) and (sitetable is not None):
            try:
                sitetable.replace(
                    {'NaN': -99999}, inplace=True)

                flsh.flush(
                    sitetable,
                    'sitetable',
                    self._tablelog['sitetable'],
                    lter, session)
                self.sitepushed = True
            except Exception as e:
                print(str(e))
                self._tablelog['sitetable'].debug(str(e))
                raise ValueError(
                    'Site abbreviations already in database ' +
                    'from an different LTER. Please modify ' +
                    'abbreviations. ' + str(e))
        else:
            pass
        if self.mainpushed is None:
            try:
                flsh.flush(
                    maintable,
                    'maintable',
                    self._tablelog['maintable'],
                    lter, session)
                self.mainpushed = True
            except Exception as e:
                print(str(e))
                self._tablelog['maintable'].debug(str(e))
                raise ValueError(
                    'Main table data will not upload. ' + str(e))
        else:
            pass

        # Merging Maintable data to rawdata (post maindata commit) 
        q1 = mrg.Merger(globalid)
        mainquery = q1.query_database('maintable', sitelevels)
        rawmain_merge = merge(
            rawdata, mainquery,
            left_on=siteid, right_on='siteid', how='left')
        self._datamerged['raw_main'] = rawmain_merge
        print('merge main: ', rawmain_merge)
        print('merge main col: ', rawmain_merge.columns)
        print('merge main: ', rawmain_merge.index.values.tolist())
        print('merge main siteid: ', rawmain_merge.siteid.values.tolist())
        print('merge mainsite og: ', rawmain_merge[siteid].values.tolist())

        # Editing taxa columns for raw-taxa merge
        taxa_formated_cols = list(
            self._inputs['taxainfo'].lnedentry.keys())
        taxa_formated_cols.append(siteid)
        taxa_og_cols = list(
            self._inputs['taxainfo'].lnedentry.values())
        taxa_og_cols.append(siteid)
        print('taxa col format: ', taxa_formated_cols)
        print('taxa col og: ', taxa_og_cols)

        # Merged raw data with taxatable data (via a main merge)
        rawtaxa_merge = merge(
            taxatable, rawmain_merge,
            how='inner',
            left_on=taxa_formated_cols, right_on=taxa_og_cols   
        )
        print(
            'rawtaxamerge col (facade): ' +
            ' '.join(rawtaxa_merge.columns.values.tolist()))

        rawtaxa_merge['m_index'] = rawtaxa_merge['index']
        rawtaxa_merge.sort_values('m_index', inplace=True)
        print('merge main/taxa: ', rawtaxa_merge)
        print('merge main/taxa col: ', rawtaxa_merge.columns)
        print('merge m/t index: ', rawtaxa_merge['index'].values.tolist())
        print('merge m/t siteid: ', rawtaxa_merge.siteid.values.tolist())
        print('merge m/t site og: ', rawtaxa_merge[siteid].values.tolist())
        print(siteid)            
        print('taxatable: ', taxatable)

        # Appended taxatable with lter_proj_site's
        taxa_all_columns = taxatable.columns.values.tolist()
        taxa_all_columns.append('lter_proj_site')
        taxa_all_columns.remove(siteid)
        print('taxa all col: ', taxa_all_columns)
        taxapush = rawtaxa_merge[
            taxa_all_columns].drop_duplicates().reset_index(
                drop=True)        
        print('taxapush: ', taxapush)
        print('taxapush col: ', taxapush.columns)

        if self.taxapushed is None:
            try:
                flsh.flush(
                    taxapush,
                    'taxatable',
                    self._tablelog['taxatable'],
                    lter, session)

            except Exception as e:
                print(str(e))
                self._tablelog['taxatable'].debug(str(e))
                raise ValueError(
                    'Taxa table data will not upload: ' + str(e))
            self.taxapushed = True

        else:
            pass
        print('past taxa push')            
        # Making list of lter_proj_site's to filter our taxatable query
        lter_proj_sites = list(set(taxapush['lter_proj_site']))
        taxaquery = q1.query_database('taxatable', lter_proj_sites)
        # Appending taxatable columns for taxamerge with
        # taxaquery (this gets us taxaid's) i.e. full
        # rawdata/database primary keys merge
        taxa_formated_cols.remove(siteid)
        taxa_og_cols.remove(siteid)
        taxa_formated_cols.append('lter_proj_site')
        taxa_og_cols.append('lter_proj_site')

        # Full data/database primary keys merge
        rawmerge = merge(
            rawtaxa_merge, taxaquery,
            left_on=taxa_og_cols, right_on=taxa_formated_cols,
            how='left')
        self._datamerged['raw_main_taxa'] = rawmerge
        print('rawmerge: ', rawmerge)
        print('rawmerge col: ', rawmerge.columns.values.tolist())
        print('rawmerge index: ', rawmerge['m_index'])

        director = TableDirector()
        self._inputs['rawinfo'].foreignmergeddata = True
        print('input: ', self._inputs['rawinfo'].foreignmergeddata)

        director.set_user_input(self._inputs['rawinfo'])
        director.set_builder(self._dbtabledict['rawtable'])
        director.set_data(rawmerge)            
        director.set_globalid(globalid)
        director.set_siteid(siteid)
        director.set_sitelevels(sitelevels)
        rawdatabuild = director.get_database_table()
        rawtable = rawdatabuild._availdf

        print('rawtable (facade build): ', rawtable)
        print('rawtable col (facade build: ', rawtable.columns.values.tolist())

        rawpush = concat([
            rawtable, timetable, covartable], axis=1)

        print('rawpush: ', rawpush)
        print('rawpush col: ', rawpush.columns.values.tolist())

        if self.rawpushed is None:
            try:
                rawpush[
                    'unitobs'].fillna(-99999, inplace=True)

                flsh.flush(
                    rawpush,
                    'rawtable',
                    self._tablelog['rawtable'],
                    lter, session)

            except Exception as e:
                print(str(e))
                self._tablelog['rawtable'].debug(str(e))
                raise ValueError(
                    'Raw table data will not upload: ' + str(e))

            self.rawpushed = True
        else:
            pass
        self.pushtables = True

    def update_main(self):
        timetable = self.push_tables['timetable']
        rawmergedf_all = self._datamerged['raw_main_taxa']

        if 'year' in rawmergedf_all.columns.values.tolist():
            rawmergedf_all = rawmergedf_all.drop('year', axis=1)
        else:
            pass

        rawmergedf_all = concat(
            [rawmergedf_all, timetable], axis=1)
        print(rawmergedf_all)
        print(rawmergedf_all.columns)
        print('past rawtable')
        siteloc = self._valueregister['siteid']
        print(siteloc)
        print('past siteloc')
        rawlabel = self._inputs['rawinfo'].lnedentry
        print(rawlabel)
        rawloc = self._inputs['rawinfo'].checks
        print(rawloc)
        print('past raw label')
        # Created table of main columns that need
        # to be updated
        sitelevels = self._valueregister['sitelevels']
        updaterdirector = self.make_table('updateinfo')
        updatetable_null = updaterdirector._availdf.copy()
        updatetable = updaterdirector._availdf.copy()
        print(updatetable)
        print('made updated table')

        ##### Generating derived data #####            
        # Study Start and End year
        # Site Start and End year
        yr_all= []
        for i,item in enumerate(sitelevels):
            yr_list = rawmergedf_all[
                rawmergedf_all['siteid'] == item][
                    'year'].values.tolist()

            yr_list.sort()
            [yr_all.append(x) for x in yr_list]
            updatetable.loc[
                updatetable.siteid == item,
                'sitestartyr'] = yr_list[0]

            updatetable.loc[
                updatetable.siteid == item,
                'siteendyr'] = yr_list[-1]

            updatetable.loc[
                updatetable.siteid == item,
                'totalobs'] = len(yr_list)

            updatetable.loc[
                updatetable.siteid == item,
                'siteendyr'] = yr_list[-1]
        print('past site years')

        yr_all.sort()
        updatetable.loc[:, 'studystartyr'] = yr_all[0]
        updatetable.loc[:, 'studyendyr'] = yr_all[-1]
        print('past study year')

        # Unique Taxa units    
        taxa_col_list = [
            'sppcode', 'kingdom', 'phylum', 'clss', 'ordr',
            'family', 'genus', 'species']
        taxa_col_list_y = [x + '_y' for x in taxa_col_list]
        taxa_col_list_y.append('siteid')
        taxauniquedf = rawmergedf_all[
            taxa_col_list_y].drop_duplicates()
        taxa_site_count = DataFrame(
            {'count': taxauniquedf.groupby(
                'siteid').size()}).reset_index()
        updatetable[
            'uniquetaxaunits'] = taxa_site_count['count']
        print(updatetable)
        print('past unique taxa count')

        # Spt_rep unique levels
        updatetable.loc[:, 'sp_rep1_label'] = siteloc
        updatetable.loc[:, 'sp_rep1_uniquelevels'] = 1

        updated_cols = updatetable.columns.values.tolist()
        print(updated_cols)
        print('past updating columns')
        label_index = [
            x for x,y in
            zip(list(rawloc.keys()),list(rawloc.values()))
            if y is False]

        for i, label in enumerate(label_index):
            og_col_name = list(rawlabel.values())[i]
            updatetable.loc[
                :, label] = og_col_name
            for j, site in enumerate(sitelevels):
                levelcount = []
                uqleveldf = rawmergedf_all[
                    rawmergedf_all[siteloc] == site][
                        og_col_name].copy()
                levelcount.append(
                    len(uqleveldf.unique()))

                col = list(rawlabel.keys())[i]
                print(col)
                updated_col_name = col
                if 'sp' in col:
                    updated_col_name = col.replace(
                        't', '') + '_uniquelevels'
                elif 'trt_label' in col:
                    updated_col_name = col.replace(
                        'trt_label', '') + 'num_treatments'
                print('UPDATED!!!!!: ', updated_col_name)

                updatetable.loc[
                    updatetable.siteid ==
                    site, updated_col_name] = levelcount[0]
        print('past spatial replication')

        updatetable_merge = merge(
            updatetable,
            rawmergedf_all[['lter_proj_site', 'siteid']],
            on='siteid',
            how='outer').drop_duplicates().reset_index(drop=True)
        print('updatetable_merge: ', updatetable_merge)

        updatetable_null.drop(
            'siteid', axis=1, inplace=True)
        compare_columns = updatetable_null.columns.values.tolist()
        updatemerged = updatetable_merge[compare_columns]
        updatenull = updatetable_null[compare_columns]

        print(updatetable_merge.columns)
        print(updatetable_null.columns)
        print(updatetable_merge)
        print(updatetable_null)
        print('past updating dataframe')

        self.create_log_record('maintable_update')
        updated_df_values(
            updatenull, updatemerged,
            self._tablelog['maintable_update'], 'maintable'
        )

        # Creating orms for updating tables: Must be done
        # AFTER COMMITTING SITE AND MAIN TABLE INFORMATION
        mainupdates = {}

        try:
            orm.convert_types(updatetable_merge, orm.maintypes)
        except Exception as e:
            print(str(e))
            self._tablelog['maintable'].debug(str(e))

        print('converting types')

        try:
            session = orm.Session()
            for i in range(len(updatetable_merge)):
                mainupdates[i] = session.query(
                    orm.Maintable).filter(
                        orm.Maintable.lter_proj_site == updatetable_merge[
                            'lter_proj_site'].iloc[i]).one()
                session.add(mainupdates[i])

            print('Past setting orms')
            for i in range(len(updatetable_merge)):
                dbupload = updatetable_merge.loc[
                    i, updatetable_merge.columns].to_dict()
                for key in dbupload.items():
                    setattr(
                        mainupdates[i], key[0], key[1])
                    session.add(mainupdates[i])
            print('Past updating records')
            session.flush()
            session.commit()
        except Exception as e:
            print(str(e))
            self._tablelog['maintable'].debug(str(e))
            session.rollback()
            del session
