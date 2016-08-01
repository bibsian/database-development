#! /usr/bin/env python
import abc
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
    must be concatenated
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
        'columns': ['lterid', 'lat', 'lng', 'descript'],
        'time': False,
        'cov': False,
        'depend': False
    }
    sitetable = {
        'columns': ['lterid','siteid', 'lat', 'lng', 'descript'],
        'time': False,
        'cov': False,
        'depend': False
    }

    maintable = {
        'columns': [
            'lter_proj_site',
            'metarecordid', 'title', 'samplingunits',
            'samplingprotocol', 'structured', 'studystartyr',
            'studyendyr', 'siteid',
            'sitestartyr', 'siteendyr', 'samplefreq', 'totalobs',
            'studytype', 'community', 'uniquetaxaunits',
            # Spatial repliaction attributes
            'sp_rep1_ext', 'sp_rep1_ext_units', 'sp_rep1_label',
            'sp_rep1_uniquelevels',
            'sp_rep2_ext', 'sp_rep2_ext_units', 'sp_rep2_label',
            'sp_rep2_uniquelevels',
            'sp_rep3_ext', 'sp_rep3_ext_units', 'sp_rep3_label',
            'sp_rep3_uniquelevels',
            'sp_rep4_ext', 'sp_rep4_ext_units', 'sp_rep4_label',
            'sp_rep4_uniquelevels',
            'authors', 'authors_contact', 'metalink', 'knbid',
            'treatment_type', 'num_treatments',
            'exp_maintainence', 'trt_label', 'derived'],
        'time': False,
        'cov': False,
        'depend': False
    }
    taxatable = {
        'columns': [
            'lter_proj_site', 'sppcode', 'kingdom', 'phylum', 'clss',
            'ordr','family', 'genus', 'species', 'authority'],
        'time': False,
        'cov': False,
        'depend': True
    }
    rawtable = {
        'columns': [
            'taxaid', 'lter_proj_site', 'year', 'month', 'day',
            'spt_rep1', 'spt_rep2', 'spt_rep3', 'spt_rep4',
            'structure', 'individ', 'trt_label',
            'unitobs', 'covariates'],
        'time': True,
        'cov': True ,
        'depend': True
    }

    updatetable = {
        'columns': [
            'studystartyr', 'studyendyr', 'sitestartyr',
            'siteendyr', 'totalobs', 'uniquetaxaunits',
            'sp_rep1_label', 'sp_rep1_uniquelevels',
            'sp_rep2_label', 'sp_rep2_uniquelevels',
            'sp_rep3_label', 'sp_rep3_uniquelevels',
            'sp_rep4_label', 'sp_rep4_uniquelevels',
            'num_treatments'
        ],
        'time': False,
        'cov': False,
        'depend':False
    }

    tabledict = {
        'climaterawtable': climaterawtable,
        'stationtable': stationtable,
        'sitetable': sitetable,
        'maintable': maintable,
        'taxatable': taxatable,
        'rawtable': rawtable,
        'updatetable': updatetable
    }

    def get_table_name(self):
        return self._inputs.tablename

    def get_columns(self):
        return self.tabledict[
            self._inputs.tablename]['columns']

    def get_available_columns(self):
        return list(self._inputs.lnedentry.values())

    def get_null_columns(self):
        availcol = list(self._inputs.lnedentry.keys())
        allcol = self.tabledict[
            self._inputs.tablename]['columns']
        return [x for x in allcol if x not in availcol]

    @abc.abstractmethod
    def get_dataframe(self):
        pass


class SiteTableBuilder(AbstractTableBuilder):
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

        if 'lterid' in dbcol:
            dbcol.remove('lterid')
        else:
            pass
        if 'lterid' in nullcols:
            nullcols.remove('lterid')
        else:
            pass
        nullcols.remove('descript')
        uniquesubset = dataframe[acols]
        nullsubset = hlp.produce_null_df(
            ncols=len(nullcols),
            colnames=nullcols,
            dflength=len(uniquesubset),
            nullvalue='NaN')
        nullsubset2 = hlp.produce_null_df(
            ncols=1,
            colnames=['descript'],
            dflength=len(uniquesubset),
            nullvalue='NA')

        _concat =  concat(
            [uniquesubset, nullsubset, nullsubset2],
            axis=1).reset_index(drop=True)
        final = _concat.drop_duplicates().reset_index(drop=True) 
        final.columns =dbcol
        return final

class MainTableBuilder(AbstractTableBuilder):
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
             'sp_rep1_label', 'sp_rep1_uniquelevels',
             'sp_rep2_label', 'sp_rep2_uniquelevels',
             'sp_rep3_label', 'sp_rep3_uniquelevels',
             'sp_rep4_label', 'sp_rep4_uniquelevels',
            'num_treatments'
        ]

        # Creating main data table
        maindata = DataFrame(
            {
                'metarecordid':dataframe['global_id'], 
                'title': dataframe['title'],
                'samplingunits': 'NA',
                'samplingprotocol': dataframe['data_type'],
                'structured': 'NA',
                'studystartyr': 'NA',
                'studyendyr': 'NA',
                'siteid': 'NA',
                'sitestartyr': 'NA',
                'siteendyr': 'NA',
                'samplefreq': dataframe['temp_int'],
                'totalobs': 'NA',
                'studytype': dataframe['study_type'],
                'community': dataframe['comm_data'],
                'uniquetaxaunits': 'NA',
                # Spatial repliaction attributes
                'sp_rep1_ext': -99999,
                'sp_rep1_ext_units': 'NA',
                'sp_rep1_label': 'NA',
                'sp_rep1_uniquelevels': 'NA',
                'sp_rep2_ext': -99999,
                'sp_rep2_ext_units': 'NA',
                'sp_rep2_label': 'NA',
                'sp_rep2_uniquelevels': 'NA',
                'sp_rep3_ext': -99999,
                'sp_rep3_ext_units': 'NA',
                'sp_rep3_label': 'NA',
                'sp_rep3_uniquelevels': 'NA',
                'sp_rep4_ext': -99999,
                'sp_rep4_ext_units': 'NA',
                'sp_rep4_label': 'NA',
                'sp_rep4_uniquelevels': 'NA',
                'authors': 'NA',
                'authors_contact': 'NA',
                'metalink': dataframe['site_metadata'],
                'knbid': dataframe['portal_id'],
                'treatment_type': dataframe['treatment_type'],
                'num_treatments': 'NA',
                'exp_maintainence': dataframe['exp_maintainence'],
                'trt_label': 'NA',
                'derived': 'NA'

            },
            columns = [
            'metarecordid', 'title', 'samplingunits',
            'samplingprotocol', 'structured', 'studystartyr',
            'studyendyr', 'siteid',
            'sitestartyr', 'siteendyr', 'samplefreq', 'totalobs',
            'studytype', 'community', 'uniquetaxaunits',
            # Spatial repliaction attributes
            'sp_rep1_ext', 'sp_rep1_ext_units', 'sp_rep1_label',
            'sp_rep1_uniquelevels',
            'sp_rep2_ext', 'sp_rep2_ext_units', 'sp_rep2_label',
            'sp_rep2_uniquelevels',
            'sp_rep3_ext', 'sp_rep3_ext_units', 'sp_rep3_label',
            'sp_rep3_uniquelevels',
            'sp_rep4_ext', 'sp_rep4_ext_units', 'sp_rep4_label',
            'sp_rep4_uniquelevels',
            'authors', 'authors_contact', 'metalink', 'knbid',
            'treatment_type', 'num_treatments',
            'exp_maintainence', 'trt_label', 'derived'], index=[0])

        _concat =  concat(
            [maindata]*len(sitelevels))
        _concat['siteid'] = sitelevels
        back = [x for x in _concat.columns if x not in autoupdated]
        return _concat[back]

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
            uniquesubset = unqdf[acols]
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

class RawTableBuilder(AbstractTableBuilder):
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


class DatabaseTable:
    def __init__(self):
        self._name = None
        self._cols = None
        self._null = None
        self._availcols = None
        self._availdf = None

    def set_table_name(self, tablename):
        self._name = tablename

    def set_columns(self, colnames):
        self._cols = colnames

    def set_available_columns(self, acols):
        self._availcols = acols

    def set_null_columns(self, nullcol):
        self._null = nullcol

    def set_dataframe(self, availdf):
        self._availdf = availdf

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

        adata = self._builder.get_dataframe(
            self._rawdata, acolumns, nullcol, columns,
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
        # Columns that will be updated later in the
        # program
        updatedf = hlp.produce_null_df(
            len(dbcol), dbcol, len(sitelevels), 'NA')
        updatedf['siteid'] = sitelevels
        return updatedf

class ClimateTableBuilder(AbstractTableBuilder):
    '''
    Concrete table builder for climate data.
    '''
    def get_dataframe(
            self, dataframe, acols, nullcols, dbcol,
            globalid, siteid, sitelevels):

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

        try:
            dataframe[acols]
        except:
            print('could not find column, trying numeric index')
            acols = [int(x) for x in acols]

        finally:
            acols.append(siteid)

        uniquesubset = dataframe[acols]
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
