#! /usr/bin/env python
from collections import namedtuple
import os
import datetime as tm
import re
from pandas import merge, concat, DataFrame, read_csv, to_numeric
from poplerGUI.logiclayer.class_metaverify import MetaVerifier
from poplerGUI.logiclayer.class_commanders import (
    LoadDataCommander, DataCommandReceiver,
    CommandInvoker, MakeProxyCommander, MakeProxyReceiver,
    CareTakerCommand, CareTakerReceiver)
from poplerGUI.logiclayer.class_helpers import UniqueReplace, check_registration
from poplerGUI.logiclayer.class_tablebuilder import (
    Study_Site_Table_Builder, Table_Builder_Director,
    Project_Table_Builder, Taxa_Table_Builder,
    Observation_Table_Builder, UpdaterTableBuilder)

from poplerGUI.logiclayer import class_logconfig as log
from poplerGUI.logiclayer import class_flusher as flsh
from poplerGUI.logiclayer import class_merger as mrg
from poplerGUI.logiclayer.class_helpers import updated_df_values
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI.logiclayer import class_mergedtoupload as mrg

import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"

all = ['Facade']

class Facade:
    '''
    This is the facade class to handle the interaction
    between the user inputs and the data
    '''

    # Class attributes are related to managing
    # various commands from user
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
        Class instances will be registered with the 
        input dictionary. 
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
            'study_site_table': Study_Site_Table_Builder(),
            'project_table': Project_Table_Builder(),
            'taxa_table': Taxa_Table_Builder(),
            'timetable': None,
            'count_table': Observation_Table_Builder(),
            'biomass_table': Observation_Table_Builder(),
            'density_table': Observation_Table_Builder(),
            'percent_cover_table': Observation_Table_Builder(),
            'individual_table': Observation_Table_Builder(),
            'covartable': None,
            'updatetable': UpdaterTableBuilder()
        }

        self._datamerged = {
            'raw_main': None,
            'raw_main_taxa': None
        }

        self._tablelog = {
            'study_site_table': None,
            'project_table': None,
            'maintable': None,
            'maintable_update': None,
            'timetable': None,
            'taxa_table': None,
            'count_table': None,
            'bimoass_table': None,
            'density_table': None,
            'percent_cover_table': None,
            'individual_table': None,
            'covartable': None,
            'climatesite': None,
            'climateobs': None,
            'addsite': None
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
            'study_site_table': None,
            'project_table': None,
            'taxa_table': None,
            'timetable': None,
            'count_table': None,
            'biomass_table': None,
            'density_table': None,
            'percent_cover_table': None,
            'individual_table': None,
            'covariates': None
        }

        self.pushtables = None
        self.sitepushed = None
        self.mainpushed = None
        self.siteinproject = None
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
                rootpath + end + 'data' + end +
                'Identified_to_upload.csv'),
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
        '''
        Method to store the unique sitelevel in the
        facade class
        '''

        try:
            assert isinstance(sitelevels, list)
        except Exception as e:
            print(str(e))
            raise TypeError('Site levels input is not a list')

        sitelevels.sort()
        self._valueregister['sitelevels'] = sitelevels


    def create_log_record(self, tablename):
        '''
        Method to initialize a logger; appends the file the log
        saves to with relavent information regarding what table
        and type of information is being recorded
        '''
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
                'logs/{}_{}_{}_{}.log'.format(
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
        sitecol = self._inputs['siteinfo'].lnedentry['study_site_key']
        uqsitelevels = self._valueregister['sitelevels']

        director = Table_Builder_Director()           
        builder = self._dbtabledict[tablename]
        director.set_user_input(uniqueinput)
        director.set_builder(builder)

        if tablename != 'project_table':
            director.set_data(self._data)
        else:
            metaverify = MetaVerifier(self._inputs['metacheck'])
            metadata = metaverify._meta
            director.set_data(metadata.iloc[globalid-1,:])

        director.set_globalid(globalid)
        director.set_siteid(sitecol)
        director.set_sitelevels(uqsitelevels)

        return director.get_database_table()

    def push_merged_data(self):
        '''
        Method in facade class to check if all data tables
        have been completed by the user (although
        site table can be empty if records are already in the 
        database).
        '''


        # Tables created from use input
        study_site_table_df = self.push_tables['study_site_table']
        study_site_table_df.fillna('NA', inplace=True)
        project_table_df = self.push_tables['project_table']
        taxa_table_df = self.push_tables['taxa_table']
        time_table_df = self.push_tables['timetable']
        observation_table_df = self.push_tables[
            self._inputs['rawinfo'].tablename]
        observation_table_name = self._inputs['rawinfo'].tablename
        covariate_table_df = self.push_tables['covariates']
        site_levels = self._valueregister['sitelevels']
        site_location = self._valueregister['siteid']
        lter = self._valueregister['lterid']
        # -------------------------------------- #
        # --- Pushing study site table data --- #
        # -------------------------------------- #
        nulltest = study_site_table_df['study_site_key'].drop_duplicates().values.tolist()
        if nulltest == ['NULL']:
            if self.sitepushed is None:
                try:
                    study_site_table_df.to_sql(
                        'study_site_table',
                        orm.conn, if_exists='append', index=False)
                    self.sitepushed = True
                except Exception as e:
                    print(str(e))
                    self._tablelog['study_site_table'].debug(str(e))
                    raise ValueError(
                        'Could not push study site table data: ' + str(e)
                    )
        else:
            pass       

        # -------------------------------------- #
        # --- Pushing project table data --- #
        # -------------------------------------- #
        
        if self.mainpushed is None:
            try:
                project_table_df.to_sql(
                    'project_table', orm.conn,
                    if_exists='append', index=False
                )
                self.mainpushed = True
            except Exception as e:
                print(str(e))
                self._tablelog['project_table'].debug(str(e))
                raise ValueError(
                    'Could not push project table data: ' + str(e)
                )
        else:
            pass
        # -------------------------------------- #
        # --- Pushing site in project table data --- #
        # -------------------------------------- #
        if self.siteinproject is None:
            pass
        else:
            pass

        merge_object = mrg.MergeToUpload()
        site_in_project_key_df = merge_object.site_in_proj_key_df(
            studysitetabledf=study_site_table_df,
            projecttabledf=project_table_df,
            observationtabledf=time_table_df,
            lterlocation=lter,
            studysitelabel=site_location,
            studysitelevels=site_levels
        )


        merge_object.merge_for_taxa_table_upload(
            formated_taxa_table=taxa_table_df,
            siteinprojkeydf=site_in_project_key_df,
            sitelabel=site_location
        )

        taxa_column_in_data = [
            x[0] for x in 
            list(self._inputs['taxainfo'].lnedentry.items())
        ]

        taxa_column_in_push_table = [
            x[1] for x in 
            list(self._inputs['taxainfo'].lnedentry.items())
        ]
        print('past taxa')
        merge_object.merge_for_datatype_table_upload(
            raw_dataframe=time_table_df,
            formated_dataframe=observation_table_df,
            formated_dataframe_name=
            '{}'.format(
                        re.sub('_table', '', self._inputs['rawinfo'].tablename)),
            covariate_dataframe = covariate_table_df,
            siteinprojkeydf=site_in_project_key_df,
            raw_data_taxa_columns=taxa_column_in_data,
            uploaded_taxa_columns=taxa_column_in_push_table
        )