#! /usr/bin/env python
import abc
import re
from pandas import concat, DataFrame
from poplerGUI.logiclayer import class_helpers as hlp 

__all__ = [
    'SiteTableBuilder', 'MainTableBuilder',
    'TaxaTableBuilder', 'RawTableBuilder',
    'UpdaterTableBuilder', 'DatabaseTable', 'TableDirector']

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
        'individual_table': individual_table,
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

        print('acols before: ', acols)
        print('nullcols before: ', nullcols)
        print('dbcol before: ', dbcol)

        try:
            acols = [x.rstrip() for x in acols]
        except Exception as e:
            acols = [int(x) for x in acols]
            uniquesubset = dataframe[acols]
            print(str(e))

        remove_from_null = ['lter_table_fkey']
        [nullcols.remove(x) for x in remove_from_null]
        remove_known_fkey = ['lter_table_fkey']
        [dbcol.remove(x) for x in remove_known_fkey]
        lat_lng_null_list = ['lat_study_site', 'lng_study_site']
        [nullcols.remove(x) for x in lat_lng_null_list]

        print('acols after: ', acols)
        print('nullcols after: ', nullcols)
        print('dbcol after: ', dbcol)

        uniquesubset = dataframe[acols]
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

class Project_Table_Builder(AbstractTableBuilder):
    '''
    Concrete table builder implementation: Site
    Note, no get methods because there is no
    alternate informatoin needed
    '''

    def get_dataframe(
            self, dataframe, acols, nullcols, keycols, dbcol,
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
            'spatial_replication_level_2_label',
            'spatial_replication_level_2_number_of_unique_reps',
            'spatial_replication_level_3_label',
            'spatial_replication_level_3_number_of_unique_reps',
            'spatial_replication_level_4_label',
            'spatial_replication_level_4_number_of_unique_reps',
            'num_treatments'
        ]

        # Creating main data table
        maindata = DataFrame(
            {
                'proj_metadata_key': dataframe['global_id'], 
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


class Taxa_Table_Builder(AbstractTableBuilder):
    '''
    Concrete table builder implementation: Site
    Note, no get methods because there is no
    alternate informatoin needed
    '''
    dependentdf = None
    def get_dataframe(
            self, dataframe, acols, nullcols, keycols, dbcol,
            globalid, siteid, sitelevels):

        try:
            acols = [x.rstrip() for x in acols]
        except Exception as e:
            acols = [int(x) for x in acols]
            uniquesubset = dataframe[acols]
            print(str(e))

        remove_unknown_pkey = ['taxa_table_key']
        [dbcol.remove(x) for x in remove_unknown_pkey]
        [nullcols.remove(x) for x in remove_unknown_pkey]
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

        for i, item in enumerate(dbcolrevised):
            final.rename(
                columns={acols[i]: item},
                inplace=True)
        dbcol.append(siteid)
        return final[dbcol]


class Observation_Table_Builder(AbstractTableBuilder):
    '''
    Concrete table builder implementation: Site
    Note, no get methods because there is no
    alternate informatoin needed
    '''
    def get_dataframe(
            self, dataframe, acols, nullcols, keycols, dbcol,
            globalid, siteid, sitelevels):

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

    
class UpdaterTableBuilder(AbstractTableBuilder):
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

        # Columns that will be updated later in the
        # program
        try:
            updatedf = hlp.produce_null_df(
                len(dbcol), dbcol, len(sitelevels), 'NA')
        except Exception as e:
            acols = [int(x) for x in acols]
            updatedf = hlp.produce_null_df(
                len(dbcol), dbcol, len(sitelevels), 'NA')
            print(str(e))

        updatedf['siteid'] = sitelevels
        return updatedf

class ClimateTableBuilder(AbstractTableBuilder):
    '''
    Concrete table builder for climate data.
    '''
    def get_dataframe(
            self, dataframe, acols, nullcols, dbcol,
            globalid, siteid, sitelevels):

        acols = [x.rstrip() for x in acols]
        nullcols = [x.rstrip() for x in nullcols]
        dbcol = [x.rstrip() for x in dbcol]

        col_booleans = list(self._inputs.checks.values())
        col_names = list(self._inputs.checks.keys())
        acols = [
            x.rstrip() for x,y in zip(acols, col_booleans)
            if y is False]
        acols_rename = [
            x.rstrip() for x,y in zip(col_names, col_booleans)
            if y is False]
        nullcols = [
            x.rstrip() for x,y in zip(col_names, col_booleans)
            if y is True]
        dbcol.remove('stationid')

        for i in dbcol:
            if i not in nullcols:
                nullcols.append(i)
            else:
                pass

        print('siteid: ', siteid)
        print('col bools: ', col_booleans)
        print('avaialable cols: ', acols)
        print('null cols: ', nullcols)
        print('db cols: ', dbcol)

        print('dataframe climate build: ', dataframe)

        acols.append(siteid)
        try:
            uniquesubset = dataframe[acols]
        except Exception as e:
            acols = [int(x) for x in acols]
            uniquesubset = dataframe[acols]
            print(str(e))

        nullsubset = hlp.produce_null_df(
            ncols=len(nullcols),
            colnames=nullcols,
            dflength=len(uniquesubset),
            nullvalue='NA')
        print('uq subset build: ', uniquesubset)
        _concat =  concat(
            [uniquesubset, nullsubset], axis=1).reset_index(
                )
        final = _concat.reset_index() 

        try:
            print('build siteid: ', siteid)
            acols_rename.append('stationid')
            for i,item in enumerate(acols_rename):
                final.rename(
                    columns={acols[i]:item}, inplace=True)

            print('final build class: ', final.columns)
            return final

        except Exception as e:
            print(str(e))
            raise AttributeError('Column renaming error')
