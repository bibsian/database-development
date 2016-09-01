#! /usr/bin/env python
import pytest
from pandas import concat, DataFrame, read_csv, read_table
import abc
from collections import OrderedDict
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development" +
        "\\test\\")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_userfacade as face
os.chdir(rootpath)
from poplerGUI import class_inputhandler as ini



@pytest.fixture
def AbstractTableBuilder():
    class AbstractTableBuilder(object):
        '''
        Abstrac class that will be used to implement
        a builder design pattern with all the tables that
        must be concatenated.

        The concrete class created from this abstract class 
        need to be initiated by an input handler instance...
        from the facade class that would be a facade._inputs

        '''
        __meta__ = abc.ABCMeta

        # List of column names within each table of the database
        climaterawtable = {
            'columns': [
                'metarecordid_',
                'title', 'stationid', 'year', 'month', 'day',
                # temp
                'avetempobs', 'avetempmeasure',
                'mintempobs', 'mintempmeasure',
                'maxtempobs', 'maxtempmeasure',
                # precip
                'aveprecipobs', 'aveprecipmeasure',
                'minprecipobs', 'minprecipmeasure',
                'maxprecipobs', 'maxprecipmeasure',
                # wind
                'avewindobs', 'avewindmeasure',
                'minwindobs', 'minwindmeasure',
                'maxwindobs', 'maxwindmeasure',
                # light
                'avelightobs', 'avelightmeasure',
                'minlightobs', 'minlightmeasure',
                'maxlightobs', 'maxlightmeasure',
                # water temp
                'avewatertempobs', 'avewatertempmeasure',
                'minwatertempobs', 'minwatertempmeasure',
                'maxwatertempobs', 'maxwatertempmeasure',
                # ph
                'avephobs', 'avephmeasure',
                'minphobs', 'minphmeasure',
                'maxphobs', 'maxphmeasure',
                # cond
                'avecondobs', 'avecondmeasure',
                'mincondobs', 'mincondmeasure',
                'maxcondobs', 'maxcondmeasure',
                # turbidity
                'aveturbidityobs', 'aveturbiditymeasure',
                'minturbidityobs', 'minturbiditymeasure',
                'maxturbidityobs', 'maxturbiditymeasure',
                # other
                'covariates',
                'knbid_', 'metalink_', 'authors_', 'authors_contact_'],
            'time': True,
            'cov': True,
            'depend': False
        }
        stationtable = {
            'columns': [
                'lterid',
                'lat_climate',
                'lng_climate',
                'descript'

            ],
            'time': False,
            'cov': False,
            'depend': False
        }
        study_site_table = {
            'columns': [
                'study_site_key',
                'lter_table_fkey',
                'lat_study_site',
                'lng_study_site',
                'descript'],
            'time': False,
            'cov': False,
            'depend': False,
            'table_keys': [
                'study_site_key',
                'lter_table_fkey'
            ]
        }

        project_table = {
            'columns': [
                'proj_metadata_key', 'title', 'samplingunits',
                'datatype', 'structured', 'studystartyr',
                'studyendyr',
                'samplefreq',
                'studytype',
                'community',
                # Spatial repliaction attributes
                'spatial_replication_level_1_extent',
                'spatial_replication_level_1_extent_units',
                'spatial_replication_level_1_label',
                'spatial_replication_level_1_number_of_unique_reps',
                'spatial_replication_level_2_extent',
                'spatial_replication_level_2_extent_units',
                'spatial_replication_level_2_label',
                'spatial_replication_level_2_number_of_unique_reps',
                'spatial_replication_level_3_extent',
                'spatial_replication_level_3_extent_units',
                'spatial_replication_level_3_label',
                'spatial_replication_level_3_number_of_unique_reps',
                'spatial_replication_level_4_extent',
                'spatial_replication_level_4_extent_units',
                'spatial_replication_level_4_label',
                'spatial_replication_level_4_number_of_unique_reps',
                'treatment_type', 'derived'
                'authors', 'authors_contact', 'metalink', 'knbid',
            ],
            'time': False,
            'cov': False,
            'depend': False,
            'table_keys': ['proj_metadata_key']
        }

        site_in_project_table = {
            'columns': [
                'site_in_project_key',
                'study_site_table',
                'project_table_fkey',
                'sitestartyr',
                'siteendyr',
                'totalobs',
                'uniquetaxaunits'
            ],
            'time': False,
            'cov': False,
            'depend': True,
            'table_keys': [
                'site_in_project_key',
                'study_site_table_fkey',
                'project_table_fkey'
            ]
        }

        taxa_table = {
            'columns': [
                'taxa_table_key',
                'site_in_project_taxa_key',
                'sppcode',
                'kingdom',
                'subkingdom',
                'infrakingdom',
                'superdivision',
                'division',
                'subdivision',
                'superphylum',
                'phylum',
                'subphylum',
                'clss',
                'subclass',
                'ordr',
                'family',
                'genus',
                'species',
                'common_name',
                'authority'],

            'time': False,
            'cov': False,
            'depend': True,
            'table_keys': [
                'taxa_table_key', 'site_in_project_taxa_key'
            ]
        }

        taxa_accepted_table = {
            'columns': [
                'taxa_accepted_table_key',
                'taxa_original_fkey',
                'site_in_project_taxa_key',
                'sppcode',
                'kingdom_accepted',
                'subkingdom_accepted',
                'infrakingdom_accepted',
                'superdivision_accepted',
                'division_accepted',
                'subdivision_accepted',
                'superphylum_accepted',
                'phylum_accepted',
                'subphylum_accepted',
                'clss_accepted',
                'subclass_accepted',
                'ordr_accepted',
                'family_accepted',
                'genus_accepted',
                'species_accepted',
                'common_name_accepted',
                'authority'],

            'time': False,
            'cov': False,
            'depend': True,
            'table_keys': [
                'taxa_table_key', 'site_in_project_taxa_key'
            ]
        }

        count_table = {
            'columns': [
                'count_table_key',
                'taxa_count_fkey',
                'site_in_project_count_fkey',
                'year', 'month', 'day',
                'spatial_replication_level_1',
                'spatial_replication_level_2',
                'spatial_replication_level_3',
                'spatial_replication_level_4',
                'structure',
                'count_observation',
                'covariates',
                'trt_label'
            ],

            'time': True,
            'cov': True,
            'depend': True,
            'table_keys': [
                'count_table_key',
                'taxa_count_fkey',
                'site_in_project_count_fkey'
            ]
        }

        biomass_table = {
            'columns': [
                'biomass_table_key',
                'taxa_biomass_fkey',
                'site_in_project_biomass_fkey',
                'year', 'month', 'day',
                'spatial_replication_level_1',
                'spatial_replication_level_2',
                'spatial_replication_level_3',
                'spatial_replication_level_4',
                'structure',
                'biomass_observation',
                'covariates',
                'trt_label'
            ],

            'time': True,
            'cov': True,
            'depend': True,
            'table_keys': [
                'biomass_table_key',
                'taxa_biomass_fkey',
                'site_in_project_biomass_fkey'
            ]
        }

        density_table = {
            'columns': [
                'density_table_key',
                'taxa_density_fkey',
                'site_in_project_density_fkey',
                'year', 'month', 'day',
                'spatial_replication_level_1',
                'spatial_replication_level_2',
                'spatial_replication_level_3',
                'spatial_replication_level_4',
                'structure',
                'density_observation',
                'covariates',
                'trt_label'
            ],

            'time': True,
            'cov': True,
            'depend': True,
            'table_keys': [
                'density_table_key',
                'taxa_density_fkey',
                'site_in_project_density_fkey'
            ]
        }

        percent_cover_table = {
            'columns': [
                'percent_cover_table_key',
                'taxa_percent_cover_fkey',
                'site_in_project_percent_cover_fkey',
                'year', 'month', 'day',
                'spatial_replication_level_1',
                'spatial_replication_level_2',
                'spatial_replication_level_3',
                'spatial_replication_level_4',
                'structure',
                'percent_cover_observation',
                'covariates',
                'trt_label'
            ],
            
            'time': True,
            'cov': True,
            'depend': True,
            'table_keys': [
                'percent_cover_table_key',
                'taxa_percent_cover_fkey',
                'site_in_project_percent_cover_fkey'
            ]
        }

        individual_table = {
            'columns': [
                'individual_table_key',
                'taxa_individual_fkey',
                'site_in_project_individual_fkey',
                'year', 'month', 'day',
                'spatial_replication_level_1',
                'spatial_replication_level_2',
                'spatial_replication_level_3',
                'spatial_replication_level_4',
                'structure',
                'individual_observation',
                'covariates',
                'trt_label'
            ],
            'time': True,
            'cov': True,
            'depend': True,
            'table_keys': [
                'individual_table_key',
                'taxa_individual_fkey',
                'site_in_project_individual_fkey'
            ]
        }

        update_project_table = {
            'columns': [
                'proj_metadata_key',
                'studystartyr', 'studyendyr',
                'spatial_replication_level_1_label',
                'spatial_replication_level_1_number_of_unique_reps',
                'spatial_replication_level_2_label',
                'spatial_replication_level_2_number_of_unique_reps',
                'spatial_replication_level_3_label',
                'spatial_replication_level_3_number_of_unique_reps',
                'spatial_replication_level_4_label',
                'spatial_replication_level_4_number_of_unique_reps'
            ],
            'time': False,
            'cov': False,
            'depend': False,
            'table_keys': ['proj_metadata_key']
        }

        site_in_project_table = {
            'columns': [
                'site_in_project_key',
                'study_site_table_fkey',
                'sitestartyr',
                'siteendyr',
                'totalobs',
                'uniquetaxaunits'
            ],
            'time': False,
            'cov': False,
            'depend': False,
            'table_keys': [
                'site_in_project_key',
                'study_site_table_fkey'
            ]
        }

        tabledict = {
            'climaterawtable': climaterawtable,
            'stationtable': stationtable,
            'study_site_table': study_site_table,
            'project_table': project_table,
            'taxa_table': taxa_table,
            'taxa_accepted_table': taxa_accepted_table,
            'count_table': count_table,
            'biomass_table': biomass_table,
            'density_table': density_table,
            'percent_cover_table': percent_cover_table,
            'update_project_table': update_project_table,
            'site_in_project_table': site_in_project_table
        }

        def get_table_name(self):
            return self._inputs.tablename

        def get_columns(self):
            return self.tabledict[
                self._inputs.tablename]['columns']

        def get_available_columns(self):
            return list(self._inputs.lnedentry.values())

        def get_key_columns(self):
            return self.tabledict[
                self._inputs.tablename]['table_keys']
        
        def get_null_columns(self):
            availcol = list(self._inputs.lnedentry.keys())
            allcol = self.tabledict[
                self._inputs.tablename]['columns']
            return [x for x in allcol if x not in availcol]

        @abc.abstractmethod
        def get_dataframe(self):
            pass

    return AbstractTableBuilder

@pytest.fixture
def Study_Site_TableBuilder(AbstractTableBuilder):
    class Study_Site_TableBuilder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''

        def get_dataframe(
                self, dataframe, acols, nullcols, keycols, dbcol,
                globalid, siteid, sitelevels):
            '''
            Method to concatenate a study_site_table
            based on informatoin supplied by the user (acols),
            expected columns in table (dbcol), 
            Columns to be filled with NA (nullcols),
            and the globalid, siteid, and unique site levels
            
            '''

            try:
                acols = [x.rstrip() for x in acols]
            except Exception as e:
                acols = [int(x) for x in acols]
                uniquesubset = dataframe[acols]
                print(str(e))

            uniquesubset = dataframe[acols]
            nullsubset = hlp.produce_null_df(
                ncols=len(nullcols),
                colnames=nullcols,
                dflength=len(uniquesubset),
                nullvalue='NA')

            _concat =  concat(
                [uniquesubset, nullsubset],
                axis=1).reset_index(drop=True)
            final = _concat.drop_duplicates().reset_index(drop=True) 
            final.columns =dbcol

            return final

    return Study_Site_TableBuilder

@pytest.fixture
def Project_TableBuilder(AbstractTableBuilder):
    class Project_TableBuilder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''

        def get_dataframe(
                self, dataframe, acols, nullcols, dbcol,
                globalid, siteid, sitelevels):

            acols = [x.rstrip() for x in acols]
            nullcols = [x.rstrip() for x in nullcols]
            dbcol = [x.rstrip() for x in dbcol]
            
            if 'lter_proj_site' in dbcol:
                dbcol.remove('lter_proj_site')
            else:
                pass
            if 'lter_proj_site' in nullcols:
                nullcols.remove('lter_proj_site')
            else:
                pass
            try:
                assert sitelevels is not None
            except Exception as e:
                print(str(e))
                raise AttributeError(
                    'Site levels not passed to builder')

            # Columns that will be updated later in the
            # program
            autoupdated = [
                'studystartyr', 'studyendyr', 'sitestartyr',
                'siteendyr', 'totalobs', 'uniquetaxaunits',
                 'spatial_replication_level_1_label',
                'spatial_replication_level_1_number_of_unique_reps',
                 'spatial_replication_level_2_label', 'spatial_replication_level_2_number_of_unique_reps',
                 'spatial_replication_level_3_label', 'spatial_replication_level_3_number_of_unique_reps',
                 'spatial_replication_level_4_label', 'spatial_replication_level_4_number_of_unique_reps',
                'num_treatments'
            ]

            # Creating main data table
            maindata = DataFrame(
                {
                    'proj_metadata_key':dataframe['global_id'], 
                    'title': dataframe['title'],
                    'samplingunits': 'NA',
                    'datatype': dataframe['data_type'],
                    'structured': 'NA',
                    'studystartyr': 'NA',
                    'studyendyr': 'NA',
                    'samplefreq': dataframe['temp_int'],
                    'studytype': dataframe['study_type'],
                    'community': dataframe['comm_data'],
                    # Spatial repliaction attributes
                    'spatial_replication_level_1_extent': -99999,
                    'spatial_replication_level_1_extent_units': 'NA',
                    'spatial_replication_level_1_label': 'NA',
                    'spatial_replication_level_1_number_of_unique_reps': 'NA',
                    'spatial_replication_level_2_extent': -99999,
                    'spatial_replication_level_2_extent_units': 'NA',
                    'spatial_replication_level_2_label': 'NA',
                    'spatial_replication_level_2_number_of_unique_reps': 'NA',
                    'spatial_replication_level_3_extent': -99999,
                    'spatial_replication_level_3_extent_units': 'NA',
                    'spatial_replication_level_3_label': 'NA',
                    'spatial_replication_level_3_number_of_unique_reps': 'NA',
                    'spatial_replication_level_4_extent': -99999,
                    'spatial_replication_level_4_extent_units': 'NA',
                    'spatial_replication_level_4_label': 'NA',
                    'spatial_replication_level_4_number_of_unique_reps': 'NA',
                    'treatment_type': dataframe['treatment_type'],
                    'derived': 'NA',
                    'authors': 'NA',
                    'authors_contact': 'NA',
                    'metalink': dataframe['site_metadata'],
                    'knbid': dataframe['portal_id']
                },
                columns = [
                    
                    'proj_metadata_key', 'title', 'samplingunits',
                    'datatype', 'structured', 'studystartyr',
                    'studyendyr',
                    'samplefreq',
                    'studytype', 'community',
                    # Spatial repliaction attributes
                    'spatial_replication_level_1_extent',
                    'spatial_replication_level_1_extent_units',
                    'spatial_replication_level_1_label',
                    'spatial_replication_level_1_number_of_unique_reps',
                    'spatial_replication_level_2_extent',
                    'spatial_replication_level_2_extent_units',
                    'spatial_replication_level_2_label',
                    'spatial_replication_level_2_number_of_unique_reps',
                    'spatial_replication_level_3_extent',
                    'spatial_replication_level_3_extent_units',
                    'spatial_replication_level_3_label',
                    'spatial_replication_level_3_number_of_unique_reps',
                    'spatial_replication_level_4_extent',
                    'spatial_replication_level_4_extent_units',
                    'spatial_replication_level_4_label',
                    'spatial_replication_level_4_number_of_unique_reps',
                    'treatment_type', 'derived',
                    'authors', 'authors_contact', 'metalink', 'knbid',
                ], index=[0])

            _concat =  concat(
                [maindata]*len(sitelevels))
            _concat['siteid'] = sitelevels
            back = [x for x in _concat.columns if x not in autoupdated]
            return _concat[back]
        
    return Project_TableBuilder

@pytest.fixture
def TaxaTableBuilder(AbstractTableBuilder):
    class TaxaTableBuilder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''
        dependentdf = None
        def get_dataframe(
                self, dataframe, acols, nullcols, dbcol,
                globalid, siteid, sitelevels):
            
            try:
                acols = [x.rstrip() for x in acols]
            except Exception as e:
                acols = [int(x) for x in acols]
                uniquesubset = dataframe[acols]
                print(str(e))

            if 'lter_proj_site' in dbcol:
                dbcol.remove('lter_proj_site')
            else:
                pass
            if 'lter_proj_site' in nullcols:
                nullcols.remove('lter_proj_site')
            else:
                pass

            print('SELF INPUTS: ', self._inputs.checks)
            print('ALL COLUMNS: ', acols)
            print('DB COLUMNS: ', dbcol)
            print('DF COLUMNS: ', dataframe.columns.values.tolist())
            print('NULL COLUMNS: ', nullcols)

            if self._inputs.checks['taxacreate'] is True:
                dfcol = dataframe.columns.values.tolist()
                columns_create = [x for x in acols if x not in dfcol]
                print('CREATE :', columns_create)
                for i in columns_create:
                    dataframe.loc[:, i] = i
                print('DF COLUMNS (added): ', dataframe.columns.values.tolist())

            else:
                pass
            
            dbcolrevised = [x for x in dbcol if x not in nullcols]
            uniquesubset_site_list = []
            for i,item in enumerate(sitelevels):                
                unqdf = dataframe[dataframe[siteid]==item]
                try:
                    uniquesubset = unqdf[acols]
                except Exception as e:
                    print(str(e))
                    
                unique = uniquesubset.drop_duplicates()
                unique = unique.reset_index()
                sitelevel = hlp.produce_null_df(
                    ncols=len(unique),
                    colnames=[siteid],
                    dflength=len(unique),
                    nullvalue=item)
                nullsubset = hlp.produce_null_df(
                    ncols=len(nullcols),
                    colnames=nullcols,
                    dflength=len(unique),
                    nullvalue='NA')

                unique = concat(
                    [unique,nullsubset,sitelevel], axis=1)
                uniquesubset_site_list.append(unique)

            final = uniquesubset_site_list[0]
            for i,item in enumerate(uniquesubset_site_list):
                if i > 0:
                    final = concat([final,item], ignore_index=True)
                else:
                    pass

            for i,item in enumerate(dbcolrevised):
                final.rename(
                    columns={acols[i]:item},
                    inplace=True)
            dbcol.append(siteid)
            return final[dbcol]

    return TaxaTableBuilder

@pytest.fixture
def RawTableBuilder(AbstractTableBuilder):
    class RawTableBuilder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''
        def get_dataframe(
                self, dataframe, acols, nullcols, dbcol,
                globalid, siteid, sitelevels):

            try:
                acols = [x.rstrip() for x in acols]
            except Exception as e:
                acols = [int(x) for x in acols]
                uniquesubset = dataframe[acols]
                print(str(e))


            acols.insert(0,siteid)
            nullcols.remove('spt_rep1')
            nullcols.remove('year')
            nullcols.remove('month')
            nullcols.remove('day')
            nullcols.remove('covariates')
            nullcols.remove('taxaid')
            nullcols.remove('lter_proj_site')

            if self._inputs.foreignmergeddata is None:
                pass
            else:
                acols.append('taxaid')
                acols.append('lter_proj_site')

            uniquesubset = dataframe[acols]
            nullsubset = hlp.produce_null_df(
                ncols=len(nullcols),
                colnames=nullcols,
                dflength=len(uniquesubset),
                nullvalue='NA')
            print('build class (null): ', nullsubset)
            print('build class: ',dataframe)
            print('uq subset build: ', uniquesubset)
            _concat =  concat(
                [uniquesubset, nullsubset], axis=1).reset_index(
                    )
            final = _concat.reset_index() 
            print('final build class: ', final)

            try:
                print('build siteid: ', siteid)
                col_to = list(self._inputs.lnedentry.keys())
                col_to.append('spt_rep1')
                col_from = list(self._inputs.lnedentry.values())
                col_from.append(siteid)

                for i,item in enumerate(col_to):
                    final.rename(
                        columns={col_from[i]:item}, inplace=True)
                return final


            except Exception as e:
                print(str(e))
                raise AttributeError('Column renaming error')


    return RawTableBuilder 

@pytest.fixture
def UpdaterTableBuilder(AbstractTableBuilder):
    class UpdaterTableBuilder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''
        def get_dataframe(
                self, dataframe, acols, nullcols, dbcol,
                globalid, siteid, sitelevels):

            # Columns that will be updated later in the
            # program
            try:
                acols = [x.rstrip() for x in acols]
            except Exception as e:
                acols = [int(x) for x in acols]
                print(str(e))

            print('update builder dbcol: ', dbcol)
            updatedf = hlp.produce_null_df(
                len(dbcol), dbcol, len(sitelevels), 'NA')
            updatedf['siteid'] = sitelevels
            print('update builder: ', updatedf)


            return updatedf

    return UpdaterTableBuilder 


@pytest.fixture
def DatabaseTable():
    class DatabaseTable:
        def __init__(self):
            self._name = None
            self._cols = None
            self._null = None
            self._availcols = None
            self._availdf = None
            self._keycols = None

        def set_table_name(self, tablename):
            self._name = tablename

        def set_columns(self, colnames):
            self._cols = colnames

        def set_available_columns(self, acols):
            self._availcols = acols
        
        def set_null_columns(self, nullcol):
            self._null = nullcol

        def set_key_columns(self, keycols):
            self._keycols = keycols

        def set_dataframe(self, availdf):
            self._availdf = availdf
            
    return DatabaseTable


@pytest.fixture
def TableDirector(DatabaseTable):

    class TableDirector:
        '''Constructs database tables'''
        _inputs = None
        _name = None
        _builder = None
        _rawdata = None
        _globalid = None
        _sitelevels = None
        _siteid = None

        def set_user_input(self, userinputcls):
            try:
                self._inputs = userinputcls
            except Exception as e:
                print(str(e))
                raise AttributeError('Incorrect user input class')

        def set_builder(self, builder):
            self._builder = builder
            try:
                assert self._inputs is not None
            except Exception as e:
                print(str(e))
                raise AssertionError('User input not set')

            self._builder._inputs = self._inputs

        def set_data(self, dataframe):
            self._rawdata = dataframe
            try:
                assert self._rawdata is not None
            except Exception as e:
                print(str(e))
                raise AssertionError('Data frame not set')

        def set_globalid(self, globalid):
            try:
                assert globalid is not None
            except Exception as e:
                print(str(e))
                raise AttributeError('Global Id not registered')
            self._globalid = globalid
            
        def set_siteid(self, siteid):
            try:
                assert siteid is not None
            except Exception as e:
                print(str(e))
                raise AttributeError('SiteId is not registered')
            self._siteid = siteid
            
        def set_sitelevels(self, sitelevels):
            self._sitelevels = sitelevels

            
        def get_database_table(self):
            ''' Initiates a concrete table class'''
            dbtable = DatabaseTable()
            try:
                assert self._builder is not None
            except Exception as e:
                print(str(e))
                raise AttributeError('Builder type not set')

            # ---Starts build process--- #
            # Table name
            table = self._builder.get_table_name()
            dbtable.set_table_name(table)

            columns = self._builder.get_columns()
            dbtable.set_columns(columns)

            acolumns = self._builder.get_available_columns()
            dbtable.set_available_columns(acolumns)

            nullcol = self._builder.get_null_columns()
            dbtable.set_null_columns(nullcol)

            keycols = self._builder.get_key_columns()
            dbtable.set_key_columns(keycols)
            
            adata = self._builder.get_dataframe(
                self._rawdata, acolumns, nullcol, columns,
                self._globalid, self._siteid, self._sitelevels)

            dbtable.set_dataframe(adata)

            return dbtable

    return TableDirector

@pytest.fixture
def user_input():
    lned = {'siteid': 'site'}
    user_input = ini.InputHandler(
        name='siteinfo', tablename='study_site_table', lnedentry=lned)
    return user_input

@pytest.fixture
def df():
    return read_csv(
        rootpath + end +
        'Datasets_manual_test/raw_data_test_1.csv')

def test_study_site_table_build(
        Study_Site_TableBuilder, TableDirector, user_input, df):
    '''
    Testing builder class for site table
    '''
    facade = face.Facade()
    facade.input_register(user_input)
    face_input = facade._inputs[user_input.name]
    assert (isinstance(face_input, ini.InputHandler)) is True

    study_site_table_build = Study_Site_TableBuilder()
    assert (isinstance(
        study_site_table_build, Study_Site_TableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(study_site_table_build)
    director.set_data(df)

    sitetab = director.get_database_table()
    showsite = sitetab._availdf
    assert (isinstance(showsite, DataFrame)) is True
    assert 0


