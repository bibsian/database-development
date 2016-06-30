#!usr/bin/env python
from pandas import merge, concat, DataFrame
import datetime as tm
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from collections import namedtuple
from class_commanders import LoadDataCommander, DataCommandReceiver
from class_commanders import CommandInvoker
from class_commanders import MakeProxyCommander, MakeProxyReceiver
from class_commanders import CareTakerCommand, CareTakerReceiver
from class_metaverify import MetaVerifier
from class_helpers import UniqueReplace, check_registration
from class_tablebuilder import (
    SiteTableBuilder, TableDirector, MainTableBuilder,
    TaxaTableBuilder, RawTableBuilder, UpdaterTableBuilder)
import class_logconfig as log
import class_flusher as flsh
import class_merger as mrg
import config as orm
from class_helpers import updated_df_values


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
        'manger', 'caretaker invoker')
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
            'sitelevels': None
        }
        self._data = None

        self._dbtabledict= {
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
            'taxatable': None,
            'timetable': None,
            'rawtable': None,
            'covartable': None
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

        self.push = None
        
    def make_proxy_helper(self, data, label):
        proxycmd = MakeProxyCommander(
            MakeProxyReceiver(), data.reset_index(
                drop=True), label)
        self.input_manager.invoker.perform_commands = proxycmd
        self.input_manager.invoker.make_proxy_data()
        self.input_manager.caretaker.save_to_memento(
            proxycmd._proxy.create_memento())

        self._data = (
            self.input_manager.caretaker.restore_memento(
                label))

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
            dt = (str(tm.datetime.now()).split()[0]).replace("-", "_")
        except Exception as e:
            print(str(e))
            raise AttributeError(
                'Global ID and data file not set')

        self._tablelog[tablename] =(
            log.configure_logger('tableformat',(
                'Logs_UI/{}_{}_{}_{}.log'.format(
                    globalid, tablename,filename,dt))))

    def make_table(self, inputname):
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
        if self.push is None:
            pass
        else:
            raise AttributeError('Data has already been pushed')
        # Commiting sitetable and maintable data
        # that has already been flushed
        orm.session.commit()
        # Stored Variables required for merges
        globalid = self._valueregister['globalid']
        lter = self._valueregister['lterid']
        siteid = self._valueregister['siteid']
        sitelevels = self._valueregister['sitelevels']
        rawdata = self._data
        print('past variable loading')

        # User created database tables
        sitetable = self.push_tables['sitetable']
        print(sitetable)
        print('past sitetable')
        maintable = self.push_tables['maintable']
        orm.convert_types(maintable, orm.maintypes)
        print(maintable)
        print('past maintable')
        taxatable = self.push_tables['taxatable']
        print(taxatable)
        print('past taxatable')
        timetable = self.push_tables['timetable']
        print(timetable)
        print('past timetable')
        rawtable = self.push_tables['rawtable']
        print(rawtable)
        print('past rawtable')
        covartable = self.push_tables['covariates']
        print(covartable)
        print('past covartable')
        print('paste table loading')

        # Merging Maintable data to rawdata (post maindata commit) 
        q1 = mrg.Merger(globalid)
        mainquery = q1.query_database('maintable', sitelevels)
        rawmain_merge = merge(
            rawdata, mainquery,
            left_on=siteid, right_on='siteid', how='left')
        self._datamerged['raw_main'] = rawmain_merge

        # Editing taxa columns for raw-taxa merge
        taxa_formated_cols = list(
            self._inputs['taxainfo'].lnedentry.keys())
        taxa_formated_cols.append(siteid)
        taxa_og_cols = list(
            self._inputs['taxainfo'].lnedentry.values())
        taxa_og_cols.append(siteid)
        # Merged raw data with taxatable data (via a main merge)
        rawtaxa_merge = merge(
            taxatable, rawmain_merge,
            how='inner',
            left_on=taxa_formated_cols, right_on=taxa_og_cols   
        )

        # Appended taxatable with projid's
        taxa_all_columns = taxatable.columns.values.tolist()
        taxa_all_columns.append('projid')
        taxa_all_columns.remove(siteid)
        try:
            taxapush = rawtaxa_merge[
            taxa_all_columns].drop_duplicates().reset_index(drop=True)
            taxaflush = flsh.Flusher(
                taxapush, 'taxatable', 'projid', lter)
            taxaflush.go()
            orm.session.commit()
        except Exception as e:
            print(str(e))
            self._tablelog['taxatable'].debug(str(e))
        
        # Making list of projid's to filter our taxatable query
        projids = list(set(taxapush['projid']))
        taxaquery = q1.query_database('taxatable', projids)
        # Appending taxatable columns for taxamerge with
        # taxaquery (this gets us taxaid's) i.e. full
        # rawdata/database primary keys merge
        taxa_formated_cols.remove(siteid)
        taxa_og_cols.remove(siteid)
        taxa_formated_cols.append('projid')
        taxa_og_cols.append('projid')

        try:
            # Full data/database primary keys merge
            rawmerge = merge(
                rawtaxa_merge, taxaquery,
                left_on=taxa_og_cols, right_on=taxa_formated_cols,
                how='left')
            rawmerge = rawmerge.drop_duplicates()
            self._datamerged['raw_main_taxa'] = rawmerge
            rawpush = concat([
                rawmerge[['projid','taxaid']], rawtable, timetable,
                covartable], axis=1)
            rawflush = flsh.Flusher(
                rawpush, 'rawtable', 'taxaid', lter)
            rawflush.go()
            orm.session.commit()
        except Exception as e:
            print(str(e))
            self._tablelog['rawtable'].debug(str(e))

        self.pushed = True

    def update_main(self):
        timetable = self.push_tables['timetable']
        rawmergedf_all = self._datamerged['raw_main_taxa']
        rawmergedf_all = concat(
            [rawmergedf_all, timetable], axis=1)
        print(rawmergedf_all)
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
            print(yr_list)
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
            'sppcode', 'kingdom', 'phylum', 'clss', 'order',
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
        print('past unique taxa count')
        
        # Spt_rep unique levels
        updatetable.loc[:, 'sp_rep1_label'] = siteloc
        updatetable.loc[:, 'sp_rep1_uniquelevels'] = 1
        bool_list = list(rawloc.values())
        updated_cols = updatetable.columns.values.tolist()
        for i, label in enumerate(rawloc):
            if ((bool_list[i] is False) and
                (label in updated_cols)):
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
                    updated_col_name = list(
                        rawlabel.keys())[i].replace(
                            't', '') + '_uniquelevels'
                    updatetable.loc[
                        updatetable.siteid ==
                        site, updated_col_name] = levelcount[0]
            else:
                pass
        print('past spatial replication')
            
        updatetable_merge = merge(
            updatetable,
            rawmergedf_all[['projid', 'siteid']],
            on='siteid',
            how='outer').drop_duplicates().reset_index(
                drop=True)

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

        updated_df_values(
            updatenull, updatemerged,
            self._tablelog['maintable'], 'maintable'
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
            for i in range(len(updatetable_merge)):
                mainupdates[i] = orm.session.query(
                    orm.Maintable).filter(
                        orm.Maintable.projid == updatetable_merge[
                            'projid'].iloc[i]).one()
                orm.session.add(mainupdates[i])

            print('Past setting orms')
            for i in range(len(updatetable_merge)):
                dbupload = updatetable_merge.loc[
                    i, updatetable_merge.columns].to_dict()
                for key in dbupload.items():
                    setattr(
                        mainupdates[i], key[0], key[1])
                    orm.session.add(mainupdates[i])
        except Exception as e:
            print(str(e))
            self._tablelog['maintable'].debug(str(e))

        print('Past updating records')
        orm.session.commit()

