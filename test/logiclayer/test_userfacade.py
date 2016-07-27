#! /usr/bin/env python

import pytest
from collections import namedtuple, OrderedDict
import datetime as tm
from pandas import merge, concat, DataFrame, read_csv, read_sql
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
    end = "\\"

from test.logiclayer.class_commanders import LoadDataCommander, DataCommandReceiver
from test.logiclayer.class_commanders import CommandInvoker
from test.logiclayer.class_commanders import MakeProxyCommander, MakeProxyReceiver
from test.logiclayer.class_commanders import CareTakerCommand, CareTakerReceiver
from test.logiclayer.class_metaverify import MetaVerifier

from test.logiclayer.class_helpers import (
    UniqueReplace, check_registration, extract, string_to_list,
    updated_df_values, produce_null_df)
from test.logiclayer.class_tablebuilder import (
    SiteTableBuilder, TableDirector, MainTableBuilder,
    TaxaTableBuilder, RawTableBuilder, UpdaterTableBuilder)

from test.logiclayer import class_dictionarydataframe as ddf
from test.logiclayer import class_timeparse as tparse
from test.logiclayer import class_logconfig as log
from test.logiclayer import class_flusher as flsh
from test.logiclayer import class_merger as mrg
from test.logiclayer.datalayer import config as orm

sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
from test.class_inputhandler import InputHandler

@pytest.fixture
def Facade():
    
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
                    rootpath +
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
            rawtable.replace({'NaN': -99999}, inplace=True)
            covartable = self.push_tables['covariates']
            print('rawtable (facade): ', rawtable)

            session = orm.Session()
            orm.convert_types(maintable, orm.maintypes)
            if self.sitepushed is None:
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
                        'abbreviations.')
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
            print('updatetable col: ', updatetable.columns)
            print('rawmergedf_all.columns: ', rawmergedf_all.columns)


            print('rawloc: ', rawloc)
            print('rawlabel: ', rawlabel)
            updated_cols = updatetable.columns.values.tolist()
            print(updated_cols)
            print('past updating columns')
            print('og_col_name: ', list(rawlabel.values()))

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
            print('past spatial and treatment replication')

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
    return Facade

@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 2,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.17'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def badmetahandle():
    lentry = {
        'globalid': 5,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.17'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput


@pytest.fixture
def filehandle():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end +
            'Datasets_manual_test/DataRawTestFile.csv'))

    return fileinput


@pytest.fixture
def replacehandle():
    lned = {'from': '-99999', 'to': 'NULL'}
    replaceinput = InputHandler(
        name='replace', lnedentry=lned)
    return replaceinput

@pytest.fixture
def sitehandle():
    lned = {'siteid': 'site'}
    sitehandle = InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle
    
def test_correct_userinput(metahandle, filehandle, Facade):
    '''
    Testing input_register command with a correctly enter
    metadata informatoin. Then trying to load a file
    without have given a fileopting input to the facade
    '''
    # Creating an instance of the facade class. This will
    # be instansiated within the User interface.
    face = Facade()
    # Registering input with the facade (metadata handler)
    face.input_register(metahandle)
    assert ('metacheck' in face._inputs.keys()) is True
    face.meta_verify()
    # Attempting to load data when there has been no
    # user inputs for loading a file
    with pytest.raises(AttributeError):
        face.load_data()


def test_incorrect_userinput(badmetahandle, Facade):
    '''
    Testing the input_register command with incorrect
    metadata inputs (should raise AttributeError)
    '''
    
    face = Facade()
    face.input_register(badmetahandle)
    with pytest.raises(AttributeError):
        face.meta_verify()

def test_file_loader(filehandle, Facade):
    '''
    Testing the file_load command of the facade class.

    NOTE ONLY TESTED FOR CSV FILES ****
    STILL NEED TO EXTEND BEHAVIOR FOR OTHER FILES***

    '''
    face = Facade()
    face.input_register(filehandle)
    face.load_data()
    assert isinstance(face._data, DataFrame)

def test_register_sitelevels(Facade):
    test = ['site1', 'site2']
    face = Facade()
    face.register_site_levels(test)
    assert (
        isinstance(face._valueregister['sitelevels'], list)) is True
    
def test_manipulate_data(filehandle, Facade, replacehandle):
    face = Facade()
    face.input_register(filehandle)
    face.load_data()

    face.input_register(replacehandle)
    face.replace_entry('replace')

    assert ('-99999' not in face._data.values) is True
    assert (int(-99999) not in face._data.values) is True

def test_view_unique(sitehandle, Facade, filehandle):
    face = Facade()
    face.input_register(filehandle)
    face.load_data()

    face.input_register(sitehandle)
    ulist = face.view_unique('siteinfo')

def test_replace_list(sitehandle, Facade, filehandle):
    sitehandle.name = 'replace_site_levels'
    face = Facade()
    face.input_register(filehandle)
    face.load_data()

    face.input_register(sitehandle)
    ulist = face.view_unique('replace_site_levels')
    print(ulist)
    print(type(ulist))
    modlist = ulist[sitehandle.lnedentry['siteid']].values.tolist()
    modlist[0] = 'changed'
    modlist.pop(0)
    print(modlist)
    face.replace_levels('replace_site_levels', ['changed'], modlist)
    print(face._data)
    assert (
        ulist.loc[0, sitehandle.lnedentry['siteid']]
        not in face._data.values) is True

def test_build_site(sitehandle, Facade, filehandle, metahandle):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)

    sitedirector = face.make_table('siteinfo')
    df = sitedirector._availdf
    assert (isinstance(df, DataFrame)) is True
    print(df)
    face.create_log_record('sitetable')
    face._tablelog['sitetable'].info('is this logging?')

@pytest.fixture
def main_input():
    main_input = InputHandler(
        name='maininfo', tablename='maintable')
    return main_input

def test_build_main(
        sitehandle, Facade, filehandle, metahandle, main_input):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)
    face.input_register(main_input)
    sitelevels = face._data['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    face.register_site_levels(sitelevels)
    
    maindirector = face.make_table('maininfo')
    df = maindirector._availdf
    print(df)
    assert (isinstance(df, DataFrame)) is True
    face.create_log_record('maintable')
    face._tablelog['maintable'].info('is this logging?')

@pytest.fixture
def taxa_user_input():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('phylum', 'TAXON_PHYLUM'),
        ('class', 'TAXON_CLASS'),
        ('ordr', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('phylum', True),
        ('class', True),
        ('ordr', True),
        ('family', True),
        ('genus', True),
        ('species', True) 
    ))

    taxacreate = {
        'taxacreate': False
    }
    
    available = [
        x for x,y in zip(
            list(taxalned.keys()), list(
                taxackbox.values()))
        if y is True
    ]
    
    taxaini = InputHandler(
        name='taxainfo',
        tablename='taxatable',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini
    
def test_build_taxa(
        sitehandle, Facade, filehandle, metahandle,
        taxa_user_input):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)
    face.input_register(taxa_user_input)
    sitelevels = face._data['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    face.register_site_levels(sitelevels)
    
    taxadirector = face.make_table('taxainfo')
    df = taxadirector._availdf
    print(df)
    assert (isinstance(df, DataFrame)) is True
    
@pytest.fixture
def raw_userinput():
    obslned = OrderedDict((
        ('spt_rep2', ''),
        ('spt_rep3', ''),
        ('spt_rep4', ''),
        ('structure', ''),
        ('individ', ''),
        ('trt_label', ''),
        ('unitobs', 'COUNT')
    ))
    
    obsckbox = OrderedDict((
        ('spt_rep2', True),
        ('spt_rep3', True),
        ('spt_rep4', True),
        ('structure', True),
        ('individ', True),
        ('trt_label', True),
        ('unitobs', False)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is False
    ]

    rawini = InputHandler(
        name='rawinfo',
        tablename='rawtable',
        lnedentry= extract(obslned, available),
        checks=obsckbox)
    return rawini

    
def test_build_raw(
        sitehandle, Facade, filehandle, metahandle,
        raw_userinput):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)
    face.input_register(raw_userinput)
    sitelevels = face._data['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    face.register_site_levels(sitelevels)
    
    rawdirector = face.make_table('rawinfo')
    df = rawdirector._availdf
    print(df)
    assert (isinstance(df, DataFrame)) is True

# TESTING THE PUSH METHODS
@pytest.fixture
def metahandle1():
    lentry = {
        'globalid': 7,
        'metaurl': ('http://and.test.rice.com'),
        'lter': 'AND'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def filehandle1():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end +
            'Datasets_manual_test/raw_data_test_1.csv'))

    return fileinput

@pytest.fixture
def sitehandle1():
    lned = {'siteid': 'SITE'}
    sitehandle = InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle

@pytest.fixture
def mainhandle1():
    main_input = InputHandler(
        name='maininfo', tablename='maintable')
    return main_input

@pytest.fixture
def taxahandle1():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('phylum', 'TAXON_PHYLUM'),
        ('clss', 'TAXON_CLASS'),
        ('ordr', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('phylum', True),
        ('clss', True),
        ('ordr', True),
        ('family', True),
        ('genus', True),
        ('species', True) 
    ))

    taxacreate = {
        'taxacreate': False
    }
    
    available = [
        x for x,y in zip(
            list(taxalned.keys()), list(
                taxackbox.values()))
        if y is True
    ]
    
    taxaini = InputHandler(
        name='taxainfo',
        tablename='taxatable',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini

@pytest.fixture
def timehandle1():
    d = {
        'dayname': 'DATE',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'DATE',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'DATE',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    timeini = InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini


@pytest.fixture
def obshandle1():
    obslned = OrderedDict((
        ('spt_rep2', ''),
        ('spt_rep3', ''),
        ('spt_rep4', ''),
        ('structure', ''),
        ('individ', ''),
        ('trt_label', 'DEPTH'),
        ('unitobs', 'COUNT')
    ))
    
    obsckbox = OrderedDict((
        ('sp_rep2_label', True),
        ('sp_rep3_label', True),
        ('sp_rep4_label', True),
        ('structure', True),
        ('individ', True),
        ('trt_label', False),
        ('unitobs', False)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is False
    ]

    rawini = InputHandler(
        name='rawinfo',
        tablename='rawtable',
        lnedentry= extract(obslned, available),
        checks=obsckbox)

    return rawini

@pytest.fixture
def covarhandle1():
    covarlned = {'columns': None}
    
    covarlned['columns'] = string_to_list(
        'DEPTH'
    )

    covarini = InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)

    return covarini

@pytest.fixture
def updatehandle1():
    update_input = InputHandler(
        name='updateinfo', tablename='updatetable')
    return update_input


# TESTED ON EMPTY DATABASE !!!!!!!!
def test_push_data_1(
        Facade, filehandle1, metahandle1, sitehandle1, mainhandle1,
        taxahandle1, obshandle1, timehandle1, covarhandle1,
        updatehandle1):

    facade = Facade()

    facade.input_register(metahandle1)
    facade.meta_verify()

    facade.input_register(filehandle1)
    facade.load_data()

    facade.input_register(sitehandle1)
    sitedirector = facade.make_table('siteinfo')
    sitetable = sitedirector._availdf
    facade.create_log_record('sitetable')
    lter = metahandle1.lnedentry['lter']
    ltercol = produce_null_df(1,['lterid'],len(sitetable),lter)
    sitetable = concat([sitetable, ltercol], axis=1)
    print('sitetable: ', sitetable)
    facade.push_tables['sitetable'] = sitetable

    siteid = sitehandle1.lnedentry['siteid']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    facade._valueregister['siteid'] = siteid

    facade.input_register(mainhandle1)
    maindirector = facade.make_table('maininfo')
    maintable = maindirector._availdf.copy().reset_index(drop=True)

    orm.convert_types(maintable, orm.maintypes)
    facade.push_tables['maintable'] = maintable
    facade.create_log_record('maintable')

    
    facade.input_register(taxahandle1)
    taxadirector = facade.make_table('taxainfo')
    taxatable = taxadirector._availdf
    facade.push_tables['taxatable'] = taxatable
    facade.create_log_record('taxatable')

    
    facade.input_register(timehandle1)
    timetable = tparse.TimeParse(
        facade._data, timehandle1.lnedentry).formater()
    facade.push_tables['timetable'] = timetable
    facade.create_log_record('timetable')

    
    facade.input_register(obshandle1)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf
    facade.push_tables['rawtable'] = rawtable
    facade.create_log_record('rawtable')

    
    facade.input_register(covarhandle1)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covarhandle1.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable
    facade.create_log_record('covartable')

    facade._valueregister['globalid'] = metahandle1.lnedentry['globalid']
    facade._valueregister['lter'] = metahandle1.lnedentry['lter']
    facade._valueregister['siteid'] = siteid


    facade.input_register(updatehandle1)    
    facade.merge_push_data()
    facade.update_main()


# TESTING THE PUSH METHODS
@pytest.fixture
def metahandle2():
    lentry = {
        'globalid': 8,
        'metaurl': ('http://sbc.test.rice.com'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def filehandle2():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end +
            'Datasets_manual_test/raw_data_test_2.csv'))

    return fileinput

@pytest.fixture
def sitehandle2():
    lned = {'siteid': 'SITE'}
    sitehandle = InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle

@pytest.fixture
def mainhandle2():
    main_input = InputHandler(
        name='maininfo', tablename='maintable')
    return main_input

@pytest.fixture
def taxahandle2():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('phylum', 'TAXON_PHYLUM'),
        ('clss', 'TAXON_CLASS'),
        ('ordr', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('phylum', True),
        ('clss', True),
        ('ordr', True),
        ('family', True),
        ('genus', True),
        ('species', True) 
    ))

    taxacreate = {
        'taxacreate': False
    }
    
    available = [
        x for x,y in zip(
            list(taxalned.keys()), list(
                taxackbox.values()))
        if y is True
    ]
    
    taxaini = InputHandler(
        name='taxainfo',
        tablename='taxatable',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini

@pytest.fixture
def timehandle2():
    d = {
        'dayname': 'DATE',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'DATE',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'DATE',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    timeini = InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini


@pytest.fixture
def obshandle2():
    obslned = OrderedDict((
        ('spt_rep2', 'PLOT'),
        ('spt_rep3', ''),
        ('spt_rep4', ''),
        ('structure', ''),
        ('individ', ''),
        ('trt_label', ''),
        ('unitobs', 'COUNT')
    ))
    
    obsckbox = OrderedDict((
        ('sp_rep2_label', False),
        ('sp_rep3_label', True),
        ('sp_rep4_label', True),
        ('structure', True),
        ('individ', True),
        ('trt_label', True),
        ('unitobs', False)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is False
    ]

    rawini = InputHandler(
        name='rawinfo',
        tablename='rawtable',
        lnedentry= extract(obslned, available),
        checks=obsckbox)

    return rawini

@pytest.fixture
def covarhandle2():
    covarlned = {'columns': None}
    
    covarlned['columns'] = string_to_list(
        'DEPTH'
    )

    covarini = InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)

    return covarini

@pytest.fixture
def updatehandle2():
    update_input = InputHandler(
        name='updateinfo', tablename='updatetable')
    return update_input


# TESTED ON EMPTY DATABASE !!!!!!!!
def test_push_data_2(
        Facade, filehandle2, metahandle2, sitehandle2, mainhandle2,
        taxahandle2, obshandle2, timehandle2, covarhandle2,
        updatehandle2):

    facade = Facade()

    facade.input_register(metahandle2)
    facade.meta_verify()

    facade.input_register(filehandle2)
    facade.load_data()

    facade.input_register(sitehandle2)
    sitedirector = facade.make_table('siteinfo')
    sitetable = sitedirector._availdf
    facade.create_log_record('sitetable')
    lter = metahandle2.lnedentry['lter']
    ltercol = produce_null_df(1,['lterid'],len(sitetable),lter)
    sitetable = concat([sitetable, ltercol], axis=1)
    print('sitetable: ', sitetable)
    facade.push_tables['sitetable'] = sitetable

    siteid = sitehandle2.lnedentry['siteid']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    facade._valueregister['siteid'] = siteid

    facade.input_register(mainhandle2)
    maindirector = facade.make_table('maininfo')
    maintable = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(maintable, orm.maintypes)
    facade.push_tables['maintable'] = maintable
    facade.create_log_record('maintable')

    
    facade.input_register(taxahandle2)
    taxadirector = facade.make_table('taxainfo')
    taxatable = taxadirector._availdf
    facade.push_tables['taxatable'] = taxatable
    facade.create_log_record('taxatable')
    
    facade.input_register(timehandle2)
    timetable = tparse.TimeParse(
        facade._data, timehandle2.lnedentry).formater()
    facade.push_tables['timetable'] = timetable
    facade.create_log_record('timetable')

    
    facade.input_register(obshandle2)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf
    facade.push_tables['rawtable'] = rawtable
    facade.create_log_record('rawtable')

    
    facade.input_register(covarhandle2)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covarhandle2.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable
    facade.create_log_record('covartable')

    facade._valueregister['globalid'] = metahandle2.lnedentry['globalid']
    facade._valueregister['lter'] = metahandle2.lnedentry['lter']
    facade._valueregister['siteid'] = siteid


    facade.input_register(updatehandle2)    
    facade.merge_push_data()
    facade.update_main()

@pytest.fixture
def df2():
    return read_csv(
        rootpath + end +
        'Datasets_manual_test/raw_data_test_2.csv')

def test_query2(df2, metahandle2, sitehandle2, taxahandle2, obshandle2):
    metadata_number = metahandle2.lnedentry['globalid']
    session = orm.Session()
    rawq2 = session.query(
        orm.Rawtable, orm.Taxatable).filter(
            orm.Rawtable.taxaid==orm.Taxatable.taxaid).join(
                orm.Maintable).filter(
                    orm.Maintable.metarecordid==metadata_number)
    session.close()
    rawdf2 = read_sql(rawq2.statement, rawq2.session.bind)
    print(rawdf2)
    print(df2)
    true_sites =df2[sitehandle2.lnedentry['siteid']].values.tolist()
    test_sites = rawdf2['spt_rep1'].values.tolist()
    assert (true_sites == test_sites) is True

    taxa_col_key = list(taxahandle2.lnedentry.items())
    true_taxa_col = [x[1] for x in taxa_col_key]
    test_taxa_col = [x[0] for x in taxa_col_key]

    true_taxa = df2[true_taxa_col].reset_index(drop=True)
    test_taxa = rawdf2[test_taxa_col].reset_index(drop=True)
    true_taxa.columns = test_taxa_col    
    assert_taxa = (true_taxa == test_taxa)
    assert all(assert_taxa.apply(all).values.tolist()) is True

    raw_col_key = list(obshandle2.lnedentry.items())
    true_raw_col = [x[1] for x in raw_col_key]
    test_raw_col = [x[0] for x in raw_col_key]
    print('test col: ', test_raw_col)
    
    true_raw = df2[true_raw_col].reset_index(drop=True)
    test_raw = rawdf2[test_raw_col].reset_index(drop=True)
    true_raw.columns = test_raw_col

    factor_list = ['spt_rep2', 'spt_rep3', 'spt_rep4']
    factor_in_df = [x for x in test_raw_col if x in factor_list]
    print(factor_in_df)
    for i,item in enumerate(factor_in_df):
        test_raw[test_raw_col[i]] = test_raw[
            test_raw_col[i]].astype(str)
        true_raw[item] = true_raw[item].astype(str)
    
    print(test_raw.dtypes)
    print(true_raw.dtypes)
    
    assert_raw = (true_raw == test_raw)
    print(assert_raw)
    assert all(assert_raw.apply(all).values.tolist()) is True

# TESTING THE PUSH METHODS
@pytest.fixture
def metahandle3():
    lentry = {
        'globalid': 9,
        'metaurl': ('http://sbc.2.test.rice.com'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def filehandle3():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end +
            'Datasets_manual_test/raw_data_test_3.csv'))

    return fileinput

@pytest.fixture
def sitehandle3():
    lned = {'siteid': 'site'}
    sitehandle = InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle

@pytest.fixture
def mainhandle3():
    main_input = InputHandler(
        name='maininfo', tablename='maintable')
    return main_input

@pytest.fixture
def taxahandle3():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('phylum', ''),
        ('clss', ''),
        ('ordr', ''),
        ('family', ''),
        ('genus', 'genus_test3'),
        ('species', 'species_test3') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('phylum', False),
        ('clss', False),
        ('ordr', False),
        ('family', False),
        ('genus', True),
        ('species', True) 
    ))

    taxacreate = {
        'taxacreate': True
    }
    
    available = [
        x for x,y in zip(
            list(taxalned.keys()), list(
                taxackbox.values()))
        if y is True
    ]
    
    taxaini = InputHandler(
        name='taxainfo',
        tablename='taxatable',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini

@pytest.fixture
def timehandle3():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'month',
        'monthform': 'mm',
        'yearname': 'year',
        'yearform': 'YYYY',
        'jd': False,
        'mspell': False
    }
    timeini = InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)


    return timeini


@pytest.fixture
def obshandle3():
    obslned = OrderedDict((
        ('spt_rep2', 'plot'),
        ('spt_rep3', 'quadrat'),
        ('spt_rep4', ''),
        ('structure', ''),
        ('individ', ''),
        ('trt_label', ''),
        ('unitobs', 'biomass')
    ))
    
    obsckbox = OrderedDict((
        ('sp_rep2_label', False),
        ('sp_rep3_label', False),
        ('sp_rep4_label', True),
        ('structure', True),
        ('individ', True),
        ('trt_label', True),
        ('unitobs', False)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is False
    ]

    rawini = InputHandler(
        name='rawinfo',
        tablename='rawtable',
        lnedentry= extract(obslned, available),
        checks=obsckbox)

    return rawini

@pytest.fixture
def covarhandle3():
    covarlned = {'columns': None}
    
    covarlned['columns'] = string_to_list(
        'temp'
    )

    covarini = InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)

    return covarini

@pytest.fixture
def updatehandle3():
    update_input = InputHandler(
        name='updateinfo', tablename='updatetable')
    return update_input


def test_push_data_3(
        Facade, filehandle3, metahandle3, sitehandle3, mainhandle3,
        taxahandle3, obshandle3, timehandle3, covarhandle3,
        updatehandle3):

    facade = Facade()

    facade.input_register(metahandle3)
    facade.meta_verify()

    facade.input_register(filehandle3)
    facade.load_data()

    facade.input_register(sitehandle3)
    sitedirector = facade.make_table('siteinfo')
    sitetable = sitedirector._availdf
    facade.create_log_record('sitetable')
    lter = metahandle3.lnedentry['lter']
    ltercol = produce_null_df(1,['lterid'],len(sitetable),lter)
    sitetable = concat([sitetable, ltercol], axis=1)
    print('sitetable: ', sitetable)
    facade.push_tables['sitetable'] = sitetable

    siteid = sitehandle3.lnedentry['siteid']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    facade._valueregister['siteid'] = siteid

    facade.input_register(mainhandle3)
    maindirector = facade.make_table('maininfo')
    maintable = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(maintable, orm.maintypes)
    facade.push_tables['maintable'] = maintable
    facade.create_log_record('maintable')

    
    facade.input_register(taxahandle3)
    taxadirector = facade.make_table('taxainfo')
    taxatable = taxadirector._availdf
    facade.push_tables['taxatable'] = taxatable
    facade.create_log_record('taxatable')
    
    facade.input_register(timehandle3)
    timetable = tparse.TimeParse(
        facade._data, timehandle3.lnedentry).formater()
    facade.push_tables['timetable'] = timetable
    facade.create_log_record('timetable')
    
    facade.input_register(obshandle3)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf
    facade.push_tables['rawtable'] = rawtable
    facade.create_log_record('rawtable')
    
    facade.input_register(covarhandle3)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covarhandle3.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable
    facade.create_log_record('covartable')

    facade._valueregister['globalid'] = metahandle3.lnedentry['globalid']
    facade._valueregister['lter'] = metahandle3.lnedentry['lter']
    facade._valueregister['siteid'] = siteid

    facade.input_register(updatehandle3)    
    facade.merge_push_data()
    facade.update_main()

@pytest.fixture
def df3():
    return read_csv(
        rootpath + end +
        'Datasets_manual_test/raw_data_test_3.csv')

def test_query3(df3, metahandle3, sitehandle3, taxahandle3, obshandle3):
    metadata_number = metahandle3.lnedentry['globalid']
    session = orm.Session()
    rawq3 = session.query(
        orm.Rawtable, orm.Taxatable).filter(
            orm.Rawtable.taxaid==orm.Taxatable.taxaid).join(
                orm.Maintable).filter(
                    orm.Maintable.metarecordid==metadata_number)
    session.close()
    rawdf3 = read_sql(rawq3.statement, rawq3.session.bind)
    print(rawdf3)
    print(df3)
    true_sites =df3[sitehandle3.lnedentry['siteid']].values.tolist()
    test_sites = rawdf3['spt_rep1'].values.tolist()
    assert (true_sites == test_sites) is True

    # Taxa colums were created in program
    # and not in original dataset
    raw_col_key = list(obshandle3.lnedentry.items())
    true_raw_col = [x[1] for x in raw_col_key]
    test_raw_col = [x[0] for x in raw_col_key]
    print('test col: ', test_raw_col)
    
    true_raw = df3[true_raw_col].reset_index(drop=True)
    test_raw = rawdf3[test_raw_col].reset_index(drop=True)
    true_raw.columns = test_raw_col

    factor_list = ['spt_rep2', 'spt_rep3', 'spt_rep4']
    factor_in_df = [x for x in test_raw_col if x in factor_list]
    print(factor_in_df)
    for i,item in enumerate(factor_in_df):
        test_raw[test_raw_col[i]] = test_raw[
            test_raw_col[i]].astype(str)
        true_raw[item] = true_raw[item].astype(str)

