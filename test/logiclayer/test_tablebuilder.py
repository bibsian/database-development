#! /usr/bin/env python
import pytest
from pandas import concat, DataFrame, read_csv, read_table
import abc
from collections import OrderedDict
import re
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_userfacade as face
os.chdir(rootpath)
from poplerGUI import class_inputhandler as ini


# ------------------------------------------------------ #
# ---------------- Abstract table builder --------------- #
# ------------------------------------------------------ #
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
                'datatype',
                'structured_type_1', 'structured_type_1_units',
                'structured_type_2', 'structured_type_2_units',
                'structured_type_3', 'structured_type_3_units',
                'studystartyr',
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
                'spatial_replication_level_5_extent',
                'spatial_replication_level_5_extent_units',
                'spatial_replication_level_5_label',
                'spatial_replication_level_5_number_of_unique_reps',
                'treatment_type_1', 'treatment_type_2',
                'treatment_type_3', 'control_group',
                'derived'
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
                'spatial_replication_level_5',
                'treatment_type_1',
                'treatment_type_2',
                'treatment_type_3',
                'structure_type_1',
                'structure_type_2',
                'structure_type_3',
                'count_observation',
                'covariates'
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
                'spatial_replication_level_5',
                'treatment_type_1',
                'treatment_type_2',
                'treatment_type_3',
                'structure_type_1',
                'structure_type_2',
                'structure_type_3',
                'biomass_observation',
                'covariates'
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
                'spatial_replication_level_5',
                'treatment_type_1',
                'treatment_type_2',
                'treatment_type_3',
                'structure_type_1',
                'structure_type_2',
                'structure_type_3',
                'density_observation',
                'covariates'
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
                'spatial_replication_level_5',
                'treatment_type_1',
                'treatment_type_2',
                'treatment_type_3',
                'structure_type_1',
                'structure_type_2',
                'structure_type_3',
                'percent_cover_observation',
                'covariates'
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
                'spatial_replication_level_5',
                'treatment_type_1',
                'treatment_type_2',
                'treatment_type_3',
                'structure_type_1',
                'structure_type_2',
                'structure_type_3',
                'individual_observation',
                'covariates'
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
                'spatial_replication_level_4_number_of_unique_reps',
                'spatial_replication_level_5_label',
                'spatial_replication_level_5_number_of_unique_reps',
                'treatment_type_1', 'treatment_type_2',
                'treatment_type_3'
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
            'individual_table': individual_table,
            'update_project_table': update_project_table,
            'site_in_project_table': site_in_project_table
        }

        def get_table_name(self):
            return self._inputs.tablename

        def get_columns(self):
            return self.tabledict[
                self._inputs.tablename]['columns']

        @abc.abstractmethod
        def get_available_columns(self):
            return list(self._inputs.lnedentry.values())

        def get_key_columns(self):
            return self.tabledict[
                self._inputs.tablename]['table_keys']

        @abc.abstractmethod
        def get_null_columns(self):
            availcol = list(self._inputs.lnedentry.keys())
            allcol = self.tabledict[
                self._inputs.tablename]['columns']
            return [x for x in allcol if x not in availcol]

        @abc.abstractmethod
        def get_dataframe(self):
            pass

    return AbstractTableBuilder


# ------------------------------------------------------ #
# ---------------- Study Site Table Builder --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def Study_Site_Table_Builder(AbstractTableBuilder):
    class Study_Site_Table_Builder(AbstractTableBuilder):
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

            acols: columns returned from the GUI (i.e. line edit entries)

            dbcol: all columns within the table

            nullcols: all columns within the table that HAVE to have
            NA's generated by the table builder

            keycols: primary and foreign keys in the table 
            (Typically what are removed from the nullcol list)
            '''


            
            acols = list(acols) if acols is not None else acols
            nullcols = list(nullcols) if acols is not None else nullcols
            keycols = list(keycols) if keycols is not None else keycols
            dbcol = list(dbcol) if dbcol is not None else dbcol
            sitelevels = list(sitelevels) if sitelevels is not None else sitelevels

            print('acols before: ', acols)
            print('nullcols before: ', nullcols)
            print('dbcol before: ', dbcol)
            
            try:
                acols = [x.rstrip() for x in acols]
            except Exception as e:
                acols = [int(x) for x in acols]
                uniquesubset = dataframe[acols]
                print(str(e))
                
            try:
                remove_from_null = ['lter_table_fkey']
                [nullcols.remove(x) for x in remove_from_null]
            except Exception as e:
                print(str(e))
            try:
                remove_known_fkey = ['lter_table_fkey']
                [dbcol.remove(x) for x in remove_known_fkey]
            except Exception as e:
                print(str(e))
            try:
                lat_lng_null_list = ['lat_study_site', 'lng_study_site']
                [nullcols.remove(x) for x in lat_lng_null_list]
            except Exception as e:
                print(str(e))


            print('acols after: ', acols)
            print('nullcols after: ', nullcols)
            print('dbcol after: ', dbcol)

            uniquesubset = dataframe[acols]
            uniquesubset.columns = ['study_site_key']
            nullcols_non_numeric = hlp.produce_null_df(
                ncols=len(nullcols),
                colnames=nullcols,
                dflength=len(uniquesubset),
                nullvalue='NA')

            nullcols_numeric = hlp.produce_null_df(
                ncols=len(lat_lng_null_list),
                colnames=lat_lng_null_list,
                dflength=len(uniquesubset),
                nullvalue='-99999')

            _concat = concat(
                [uniquesubset, nullcols_non_numeric, nullcols_numeric],
                axis=1).reset_index(drop=True)
            
            final = _concat.drop_duplicates().reset_index(drop=True)
            
            return final

    return Study_Site_Table_Builder

@pytest.fixture
def Project_Table_Builder(AbstractTableBuilder):
    class Project_Table_Builder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''
        @staticmethod
        def entry_verifier(dictionary):
            for i, (key, value) in enumerate(dictionary.items()):
                try:
                    if value.checked is True:
                        assert (value.entry != '' and value.entry != 'NULL') is True
                        if 'spatial' in key:
                            assert(value.unit != '')
                        else:
                            pass
                    else:
                        assert (value.entry == '' or value.entry == 'NULL') is True
                        if 'spatial' in key:
                            assert(value.unit == '')
                        else:
                            pass
                except Exception as e:
                    print(str(e))
                    raise AssertionError(key + ': entries not valid.')
            print('Entries are valid')

        def get_available_columns(self):
            return None

        def get_null_columns(self):
            return None

        def get_dataframe(
                self, dataframe, acols, nullcols, keycols, dbcol,
                globalid, siteid, sitelevels):

            dataframe.reset_index(inplace=True)
            # Columns that will be updated later in the
            # program
            autoupdated = [
                'studystartyr', 'studyendyr', 'sitestartyr',
                'siteendyr', 'totalobs', 'uniquetaxaunits',
                'spatial_replication_level_1_label',
                'spatial_replication_level_1_number_of_unique_reps',
                'spatial_replication_level_2_label',
                'spatial_replication_level_2_number_of_unique_reps',
                'spatial_replication_level_3_label',
                'spatial_replication_level_3_number_of_unique_reps',
                'spatial_replication_level_4_label',
                'spatial_replication_level_4_number_of_unique_reps',
                'spatial_replication_level_5_label',
                'spatial_replication_level_5_number_of_unique_reps',

            ]

            # Creating main data table
            maindata = DataFrame(
                {
                    'proj_metadata_key': dataframe['global_id'], 
                    'title': dataframe['title'],
                    'samplingunits': 'NA',
                    'datatype': dataframe['data_type'],
                    'structured_type_1': 'NA',
                    'structured_type_1_units': 'NA',
                    'structured_type_2': 'NA',
                    'structured_type_2_units': 'NA',
                    'structured_type_3': 'NA',
                    'structured_type_3_units': 'NA',
                    'studystartyr': -99999,
                    'studyendyr': -99999,
                    'samplefreq': dataframe['temp_int'],
                    'studytype': dataframe['study_type'],
                    'community': dataframe['comm_data'],
                    # Spatial repliaction attributes
                    'spatial_replication_level_1_extent': -99999,
                    'spatial_replication_level_1_extent_units': 'NA',
                    'spatial_replication_level_1_label': 'NA',
                    'spatial_replication_level_1_number_of_unique_reps': -99999,
                    'spatial_replication_level_2_extent': -99999,
                    'spatial_replication_level_2_extent_units': 'NA',
                    'spatial_replication_level_2_label': 'NA',
                    'spatial_replication_level_2_number_of_unique_reps': -99999,
                    'spatial_replication_level_3_extent': -99999,
                    'spatial_replication_level_3_extent_units': 'NA',
                    'spatial_replication_level_3_label': 'NA',
                    'spatial_replication_level_3_number_of_unique_reps': -99999,
                    'spatial_replication_level_4_extent': -99999,
                    'spatial_replication_level_4_extent_units': 'NA',
                    'spatial_replication_level_4_label': 'NA',
                    'spatial_replication_level_4_number_of_unique_reps': -99999,
                    'spatial_replication_level_5_extent': -99999,
                    'spatial_replication_level_5_extent_units': 'NA',
                    'spatial_replication_level_5_label': 'NA',
                    'spatial_replication_level_5_number_of_unique_reps': -99999,
                    'treatment_type_1': 'NA',
                    'treatment_type_2': 'NA',
                    'treatment_type_3': 'NA',
                    'control_group': 'NA',
                    'derived': 'NA',
                    'authors': 'NA',
                    'authors_contact': 'NA',
                    'metalink': dataframe['site_metadata'],
                    'knbid': dataframe['portal_id']
                },
                columns=[
                    'proj_metadata_key', 'title', 'samplingunits',
                    'datatype',
                    'structured_type_1',
                    'structured_type_1_units',
                    'structured_type_2',
                    'structured_type_2_units',
                    'structured_type_3',
                    'structured_type_3_units',
                    'studystartyr',
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
                    'spatial_replication_level_5_extent',
                    'spatial_replication_level_5_extent_units',
                    'spatial_replication_level_5_label',
                    'spatial_replication_level_5_number_of_unique_reps',
                    'treatment_type_1',
                    'treatment_type_2',
                    'treatment_type_3',
                    'control_group',
                    'derived',
                    'authors', 'authors_contact', 'metalink', 'knbid',
                ], index=[0])

            form_dict = self._inputs.lnedentry
            
            self.entry_verifier(form_dict)

            for i, (key, value) in enumerate(form_dict.items()):
                if value.checked is True:
                    maindata.loc[0, key] = value.entry
                    if 'spatial' in key or 'structure' in key:
                        if value.unit == '':
                            maindata.loc[0, '{}_units'.format(key)] = 'NA'
                        else:
                            maindata.loc[0, '{}_units'.format(key)] = value.unit
                    else:
                        pass
                else:
                    pass
            return maindata
        
    return Project_Table_Builder

# ------------------------------------------------------ #
# ---------------- Taxa table builder --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def Taxa_Table_Builder(AbstractTableBuilder):
    class Taxa_Table_Builder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''
        dependentdf = None
        def get_dataframe(
                self, dataframe,
                acols, nullcols, keycols, dbcol,
                globalid, siteid, sitelevels):

            acols = list(acols) if acols is not None else acols
            nullcols = list(nullcols) if acols is not None else nullcols
            keycols = list(keycols) if keycols is not None else keycols
            dbcol = list(dbcol) if dbcol is not None else dbcol
            sitelevels = list(sitelevels) if sitelevels is not None else sitelevels

            try:
                acols = [x.rstrip() for x in acols]
            except Exception as e:
                acols = [int(x) for x in acols]
                uniquesubset = dataframe[acols]
                print(str(e))

            try:
                [dbcol.remove(x) for x in keycols]
            except Exception as e:
                print(str(e))
            
            try:
                [nullcols.remove(x) for x in keycols]
            except Exception as e:
                print(str(e))


            print('SELF INPUTS: ', self._inputs.checks)
            print('AVAILABLE COLUMNS: ', acols)
            print('DB COLUMNS: ', dbcol)
            print('NULL COLUMNS: ', nullcols)
            print('DF COLUMNS: ', dataframe.columns.values.tolist())

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
            print('DB COLUMN REVISED: ', dbcolrevised)

            uniquesubset_site_list = []
            for i,item in enumerate(sitelevels):                
                uniquesubset = dataframe[dataframe[siteid]==item]
                try:
                    uniquesubset = uniquesubset[acols]
                except Exception as e:
                    print(str(e))
                for j, rename_item in enumerate(dbcolrevised):
                    uniquesubset.rename(
                        columns={acols[j]: rename_item},
                        inplace=True)
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
                    [unique, nullsubset, sitelevel], axis=1)
                uniquesubset_site_list.append(unique)
            print(uniquesubset_site_list)

            final = uniquesubset_site_list[0]
            for i, item in enumerate(uniquesubset_site_list):
                if i > 0:
                    final = concat([final, item], ignore_index=True)
                else:
                    pass
            print('past subsetting sites')
            dbcol.append(siteid)
            print(final)

            return final[dbcol].copy()

    return Taxa_Table_Builder

# ------------------------------------------------------ #
# ---------------- Observation table builder --------------- #
# -- Count, Biomass, Density, Percent Cover & Individual -- #
# ------------------------------------------------------ #
@pytest.fixture
def Observation_Table_Builder(AbstractTableBuilder):
    class Observation_Table_Builder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''
        def get_dataframe(
                self, dataframe, acols, nullcols, keycols, dbcol,
                globalid, siteid, sitelevels):

            acols = list(acols) if acols is not None else acols
            nullcols = list(nullcols) if acols is not None else nullcols
            keycols = list(keycols) if keycols is not None else keycols
            dbcol = list(dbcol) if dbcol is not None else dbcol
            sitelevels = list(sitelevels) if sitelevels is not None else sitelevels

            [
                '{}_observation'.format(
                    re.sub('_table', '', self._inputs.tablename))
                for x in acols if x == 'unitobs']

            [
                '{}_observation'.format(
                    re.sub('_table', '', self._inputs.tablename))
                for x in nullcols if x == 'unitobs']

            print('obs acols: ', acols)
            print('obs nullcols: ', nullcols)

            if self._inputs.tablename == 'individual_table':
                try:
                    acols.remove('')
                except Exception as e:
                    print('no individual column to remove: ', str(e))
            else:
                pass
            
            try:
                acols = [x.rstrip() for x in acols]
            except Exception as e:
                acols = [int(x) for x in acols]
                uniquesubset = dataframe[acols]
                print(str(e))

            # Insert siteid column and remove
            # spatial rep 1 from null columns (already have data
            # in siteid column of raw data)


            acols.insert(0, siteid)
            nullcols.remove('spatial_replication_level_1')
            nullcols.remove(
                '{}_observation'.format(
                    re.sub('_table', '', self._inputs.tablename)
                ))

            columns_to_be_added_later = [
                'year', 'month', 'day', 'covariates']
            [nullcols.remove(x) for x in columns_to_be_added_later]
            [nullcols.remove(x) for x in keycols]
            
            if self._inputs.foreignmergeddata is None:
                pass
            else:
                columns_where_data_is_from_query = [
                    'taxa_{}_fkey'.format(
                        re.sub('_table', '', self._inputs.tablename)),
                    'site_in_project_{}_fkey'.format(
                        re.sub('_table', '', self._inputs.tablename)
                    )
                ]
                [acols.append(x) for x in columns_where_data_is_from_query]

            uniquesubset = dataframe[acols]
            print('uniquesub: ', uniquesubset)
            nullsubset = hlp.produce_null_df(
                ncols=len(nullcols),
                colnames=nullcols,
                dflength=len(uniquesubset),
                nullvalue='NA')
            print('null subset: ', nullsubset)
            _concat = concat(
                [uniquesubset, nullsubset], axis=1).reset_index(
                    )
            final = _concat.reset_index()

            if self._inputs.tablename == 'individual_table':
                final['individual_observation'] = 1
                print('should have added individual observation')
            else:
                pass
            print('final build class columns: ', final.columns)
            try: 
                fomated_column_to_change = list(self._inputs.lnedentry.keys())
                fomated_column_to_change.append('spatial_replication_level_1')
                for index, item in enumerate(fomated_column_to_change):
                    if item == 'unitobs':
                        fomated_column_to_change[index] = '{}_observation'.format(
                            re.sub(
                                '_table', '', self._inputs.tablename))

                original_column_names_to_change = list(
                    self._inputs.lnedentry.values())
                original_column_names_to_change.append(siteid)

                for i, item in enumerate(fomated_column_to_change):
                    final.rename(
                        columns={
                            original_column_names_to_change[i]: item},
                        inplace=True)

                return final


            except Exception as e:
                print(str(e))
                raise AttributeError('Column renaming error')

    return Observation_Table_Builder 


# ------------------------------------------------------ #
# ---------------- Site in Project table builder --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def Site_In_Project_Table_Builder(AbstractTableBuilder):
    class Site_In_Project_Table_Builder(AbstractTableBuilder):
        '''
        Concrete table builder implementation: Site
        Note, no get methods because there is no
        alternate informatoin needed
        '''
        def get_dataframe(
                self, dataframe, acols, nullcols, keycols, dbcol,
                globalid, siteid, sitelevels):

            acols = list(acols) if acols is not None else acols
            nullcols = list(nullcols) if acols is not None else nullcols
            keycols = list(keycols) if keycols is not None else keycols
            dbcol = list(dbcol) if dbcol is not None else dbcol
            sitelevels = list(sitelevels) if sitelevels is not None else sitelevels

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

    return Site_In_Project_Table_Builder 

# ------------------------------------------------------ #
# ---------------- Data base table setter --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def Database_Table_Setter():
    class Database_Table_Setter:
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
            
    return Database_Table_Setter

# ------------------------------------------------------ #
# ---------------- Table Builder Director --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def Table_Builder_Director(Database_Table_Setter):

    class Table_Builder_Director:
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
            dbtable = Database_Table_Setter()
            try:
                assert self._builder is not None
            except Exception as e:
                print(str(e))
                raise AttributeError('Builder type not set')

            # ---Starts build process--- #
            # Table name
            table = self._builder.get_table_name()
            dbtable.set_table_name(table)

            dbcols = self._builder.get_columns()
            dbtable.set_columns(dbcols)

            acolumns = self._builder.get_available_columns()
            dbtable.set_available_columns(acolumns)

            nullcol = self._builder.get_null_columns()
            dbtable.set_null_columns(nullcol)

            keycols = self._builder.get_key_columns()
            dbtable.set_key_columns(keycols)

            adata = self._builder.get_dataframe(
                self._rawdata, acolumns, nullcol, keycols, dbcols,
                self._globalid, self._siteid, self._sitelevels)

            dbtable.set_dataframe(adata)

            return dbtable

    return Table_Builder_Director

# ------------------------------------------------------ #
# ---------------- Site table build test --------------- #
# ------------------------------------------------------ #
# 
# @pytest.fixture
# def dataset_test_1():
#     return read_csv(
#         rootpath + end + 'test' + end +
#         'Datasets_manual_test/raw_data_test_1.csv')
# 
# def test_study_site_table_build(
#         Study_Site_Table_Builder, Table_Builder_Director,
#         site_handle_1_count, dataset_test_1):
#     '''
#     Testing builder class for site table
#     '''
#     facade = face.Facade()
#     facade.input_register(site_handle_1_count)
#     face_input = facade._inputs[site_handle_1_count.name]
#     assert (isinstance(face_input, ini.InputHandler)) is True
# 
#     study_site_table_build = Study_Site_Table_Builder()
#     assert (isinstance(
#         study_site_table_build, Study_Site_Table_Builder)) is True
# 
#     director = Table_Builder_Director()
#     assert (isinstance(director, Table_Builder_Director)) is True
#     director.set_user_input(face_input)
#     director.set_builder(study_site_table_build)
#     director.set_data(dataset_test_1)
# 
#     sitetab = director.get_database_table()
#     showsite = sitetab._availdf
#     assert (isinstance(showsite, DataFrame)) is True
# 
# 
# 
# # ------------------------------------------------------ #
# # ---------------- Project table build test --------------- #
# # ------------------------------------------------------ #
# 
# @pytest.fixture
# def metadata_data():
#     return read_csv(
#         rootpath + end + 'data' + end +
#         'Identified_to_upload.csv', encoding='iso-8859-11')
# 
# 
# def test_project_table_build(
#         Project_Table_Builder, Table_Builder_Director,
#         project_handle_1_count, metadata_data, dataset_test_1):
# 
#     sitelevels = dataset_test_1[
#         'site'].drop_duplicates().values.tolist()
# 
#     facade = face.Facade()
#     facade.input_register(project_handle_1_count)
#     face_input = facade._inputs[project_handle_1_count.name]
# 
#     assert (isinstance(face_input, ini.InputHandler)) is True
#     project_table = Project_Table_Builder()
#     assert (isinstance(project_table, Project_Table_Builder)) is True
# 
#     director = Table_Builder_Director()
#     assert (isinstance(director, Table_Builder_Director)) is True
#     director.set_user_input(face_input)
#     director.set_globalid(1)
#     director.set_builder(project_table)
#     director.set_data(metadata_data)
#     director.set_sitelevels(sitelevels)
#     director.set_siteid('site')
# 
#     project_table_df = director.get_database_table()
#     show_project_table = project_table_df._availdf
#     print(show_project_table)
#     
# 
#     assert (
#         'control_group' in show_project_table.columns.values.tolist()) is True
#     
#     assert (isinstance(show_project_table, DataFrame)) is True
#     assert (
#         show_project_table['datatype'].drop_duplicates().values.tolist()
#         == ['count']) is True
#     assert (
#         show_project_table['proj_metadata_key'].values.tolist()
#         == [1]) is True
# 
# 
# 
# # ------------------------------------------------------ #
# # ---------------- Taxa table build test --------------- #
# # --------------- Create taxa feature is OFF ----------- #
# # ------------------------------------------------------ #
# 
# @pytest.fixture
# def taxadfexpected():
#     taxadfexpected = read_csv(
#         rootpath + end + 'test' +  end +
#         'Datasets_manual_test' + end + 'taxa_table_test.csv')
#     taxadfexpected.fillna('NA', inplace=True)
#     return taxadfexpected
#     
# def test_taxatable_build(
#         Taxa_Table_Builder, Table_Builder_Director, taxa_handle_1_count,
#         dataset_test_1, taxadfexpected):
#     sitelevels = dataset_test_1['site'].drop_duplicates().values.tolist()
#     sitelevels.sort()
#     facade = face.Facade()
#     facade.input_register(taxa_handle_1_count)
#     face_input = facade._inputs[taxa_handle_1_count.name]
#     taxabuilder = Taxa_Table_Builder()
#     assert (isinstance(taxabuilder, Taxa_Table_Builder)) is True
# 
#     director = Table_Builder_Director()
#     assert (isinstance(director, Table_Builder_Director)) is True
#     director.set_user_input(face_input)
#     director.set_builder(taxabuilder)
#     director.set_data(dataset_test_1)
#     director.set_globalid(1)
#     director.set_siteid('site')
#     director.set_sitelevels(sitelevels)
#     
#     taxatable = director.get_database_table()
#     showtaxa = taxatable._availdf
#     assert isinstance(showtaxa,DataFrame)    
# 
# 
#     taxatable 
#     taxatable = director.get_database_table()
#     showtaxa = taxatable._availdf
#     print(showtaxa)
# 
#     testphylum = list(set(showtaxa['phylum'].values.tolist()))
#     testphylum.sort()
#     testorder = list(set(showtaxa['genus'].values.tolist()))
#     testorder.sort()
#     testspecies = list(set(showtaxa['species'].values.tolist()))
#     testspecies.sort()
# 
#     
#     taxadfexpected = taxadfexpected[
#         taxadfexpected['metadata_key'] == 1]
#     
#     truephylum = list(set(taxadfexpected['phylum'].values.tolist()))
#     truephylum.sort()
#     trueorder = list(set(taxadfexpected['genus'].values.tolist()))
#     trueorder.sort()
#     truespecies = list(set(taxadfexpected['species'].values.tolist()))
#     truespecies.sort()
# 
#     assert (testphylum == truephylum) is True
#     assert (testorder == trueorder) is True    
#     assert (testspecies == truespecies) is True
# 
# # ------------------------------------------------------ #
# # ---------------- Taxa table build test --------------- #
# # --------------- Create taxa feature is ON ----------- #
# # ------------------------------------------------------ #
# @pytest.fixture
# def taxa_user_input_create():
#     taxalned = OrderedDict((
#         ('commonname', ''),
#         ('sppcode', ''),
#         ('kingdom', 'Animalia'),
#         ('subkingdom', ''),
#         ('infrakingdom', ''),
#         ('superdivision', ''),
#         ('divsion', ''),
#         ('subdivision', ''),
#         ('superphylum', ''),
#         ('phylum', ''),
#         ('subphylum', ''),
#         ('clss', ''),
#         ('subclass', ''),
#         ('ordr', ''),
#         ('family', ''),
#         ('genus', 'genus'),
#         ('species', 'species')
#     ))
# 
#     taxackbox = OrderedDict((
#         ('commonname', False),
#         ('sppcode', False),
#         ('kingdom', True),
#         ('subkingdom', False),
#         ('infrakingdom', False),
#         ('superdivision', False),
#         ('divsion', False),
#         ('subdivision', False),
#         ('superphylum', False),
#         ('phylum', False),
#         ('subphylum', False),
#         ('clss', False),
#         ('subclass', False),
#         ('ordr', False),
#         ('family', False),
#         ('genus', True),
#         ('species', True)
#     ))
# 
#     taxacreate = {
#         'taxacreate': True
#     }
#     
#     available = [
#         x for x,y in zip(
#             list(taxalned.keys()), list(
#                 taxackbox.values()))
#         if y is True
#     ]
#     
#     taxaini = ini.InputHandler(
#         name='taxainput',
#         tablename='taxa_table',
#         lnedentry= hlp.extract(taxalned, available),
#         checks=taxacreate)
#     return taxaini
# 
# def test_taxatable_build_create(
#         Taxa_Table_Builder, Table_Builder_Director,
#         taxa_user_input_create, dataset_test_1,
#         taxadfexpected):
#     sitelevels = dataset_test_1['site'].drop_duplicates().values.tolist()
#     sitelevels.sort()
#     facade = face.Facade()
#     facade.input_register(taxa_user_input_create)
#     face_input = facade._inputs[taxa_user_input_create.name]
#     taxabuilder = Taxa_Table_Builder()
#     assert (isinstance(taxabuilder, Taxa_Table_Builder)) is True
# 
#     director = Table_Builder_Director()
#     assert (isinstance(director, Table_Builder_Director)) is True
#     director.set_user_input(face_input)
#     director.set_builder(taxabuilder)
#     director.set_data(dataset_test_1)
#     director.set_globalid(2)
#     director.set_siteid('site')
#     director.set_sitelevels(sitelevels)
# 
#     taxatable = director.get_database_table()
#     showtaxa = taxatable._availdf
#     assert isinstance(showtaxa, DataFrame)
#     print(showtaxa)
#     showtaxa['phylum'] = 'Animalia'
#     print(showtaxa)
#     
#     testphylum = list(set(showtaxa['phylum'].values.tolist()))
#     testphylum.sort()
#     testorder = list(set(showtaxa['genus'].values.tolist()))
#     testorder.sort()
#     testspecies = list(set(showtaxa['species'].values.tolist()))
#     testspecies.sort()
# 
#     taxadfexpected.loc[:, 'phylum'] = 'Animalia'
#     print('phylum column: ', taxadfexpected['phylum'])
#     taxadfexpected = taxadfexpected[
#         taxadfexpected['metadata_key'] == 1]
# 
#     truephylum = list(set(taxadfexpected['phylum'].values.tolist()))
#     truephylum.sort()
#     trueorder = list(set(taxadfexpected['genus'].values.tolist()))
#     trueorder.sort()
#     truespecies = list(set(taxadfexpected['species'].values.tolist()))
#     truespecies.sort()
# 
#     assert (testphylum == truephylum) is True
#     assert (testorder == trueorder) is True
#     assert (testspecies == truespecies) is True
# 
# 
# # ------------------------------------------------------ #
# # ------------ Observation (count) table build test --------------- #
# # ------------------------------------------------------ #
# 
# def test_count_table_build(
#         Table_Builder_Director, count_handle_1_count,
#         dataset_test_1, Observation_Table_Builder):
#     sitelevels = dataset_test_1[
#         'site'].drop_duplicates().values.tolist()
#     sitelevels.sort()
#     facade = face.Facade()
#     facade.input_register(count_handle_1_count)
#     face_input = facade._inputs[count_handle_1_count.name]
#     countbuilder = Observation_Table_Builder()
#     assert (isinstance(countbuilder, Observation_Table_Builder)) is True
# 
#     director = Table_Builder_Director()
#     assert (isinstance(director, Table_Builder_Director)) is True
#     director.set_user_input(face_input)
#     director.set_builder(countbuilder)
#     director.set_data(dataset_test_1)
#     director.set_globalid(2)
#     director.set_siteid('site')
#     director.set_sitelevels(sitelevels)
#     counttable = director.get_database_table()
#     showcount = counttable._availdf
#     print('finished: ', showcount)
#     counttest = showcount['count_observation'].values.tolist()
#     counttrue = dataset_test_1['count'].values.tolist()
# 
#     sitetest = showcount[
#         'spatial_replication_level_1'].values.tolist()
#     sitetrue = dataset_test_1['site'].values.tolist()
# 
#     assert (counttest == counttrue) is True
#     assert (sitetest == sitetrue) is True
# 
# # ------------------------------------------------------ #
# # ------------ Observation (percentcover) table build test -------- #
# # ------------------------------------------------------ #
# 
@pytest.fixture
def dataset_test_4():
    return read_csv(
        rootpath + end + 'test' + end +
        'Datasets_manual_test/raw_data_test_4.csv')

def test_percent_cover_table_build(
        Table_Builder_Director,  biomass_handle_4_percent_cover,
        dataset_test_4, Observation_Table_Builder):
    sitelevels = dataset_test_4[
        'site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(biomass_handle_4_percent_cover)
    face_input = facade._inputs[biomass_handle_4_percent_cover.name]
    percent_coverbuilder = Observation_Table_Builder()
    assert (isinstance(percent_coverbuilder, Observation_Table_Builder)) is True

    director = Table_Builder_Director()
    assert (isinstance(director, Table_Builder_Director)) is True
    director.set_user_input(face_input)
    director.set_builder(percent_coverbuilder)
    director.set_data(dataset_test_4)
    director.set_globalid(2)
    director.set_siteid('site')
    director.set_sitelevels(sitelevels)
    percent_covertable = director.get_database_table()
    showpercent_cover = percent_covertable._availdf
    print('finished: ', showpercent_cover)

    percent_covertest = showpercent_cover['percent_cover_observation'].values.tolist()
    percent_covertrue = dataset_test_4['cover'].values.tolist()

    percent_covertest = [float(x) for x in percent_covertest]
    percent_covertrue = [float(x) for x in percent_covertrue]
    
    sitetest = showpercent_cover[
        'spatial_replication_level_1'].values.tolist()
    sitetrue = dataset_test_4['site'].values.tolist()
    print(showpercent_cover.columns)
    assert 0
    assert (percent_covertest == percent_covertrue) is True
    assert (sitetest == sitetrue) is True

# ------------------------------------------------------ #
# ------------ Observation (individual) table build test -------- #
# ------------------------------------------------------ #

# @pytest.fixture
# def dataset_test_5():
#     return read_csv(
#         rootpath + end + 'test' + end +
#         'Datasets_manual_test/raw_data_test_5.csv')
# 
# def test_individual_table_build(
#         Table_Builder_Director, count_handle5,
#         dataset_test_5, Observation_Table_Builder):
#     sitelevels = dataset_test_5[
#         'SITE'].drop_duplicates().values.tolist()
#     sitelevels.sort()
#     facade = face.Facade()
#     facade.input_register(count_handle5)
#     face_input = facade._inputs[count_handle5.name]
#     individualbuilder = Observation_Table_Builder()
#     assert (isinstance(individualbuilder, Observation_Table_Builder)) is True
# 
#     director = Table_Builder_Director()
#     assert (isinstance(director, Table_Builder_Director)) is True
#     director.set_user_input(face_input)
#     director.set_builder(individualbuilder)
#     director.set_data(dataset_test_5)
#     director.set_globalid(2)
#     director.set_siteid('SITE')
#     director.set_sitelevels(sitelevels)
#     individualtable = director.get_database_table()
#     showindividual = individualtable._availdf
#     print('finished: ', showindividual)
# 
#     check_individual_obs = showindividual[
#         'individual_observation'].drop_duplicates().values.tolist()
#     
#     sitetest = showindividual[
#         'spatial_replication_level_1'].values.tolist()
#     sitetrue = dataset_test_5['SITE'].values.tolist()
# 
#     assert (check_individual_obs == [1]) is True
#     assert (sitetest == sitetrue) is True
