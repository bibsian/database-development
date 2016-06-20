#!usr/bin/env python
import abc
from class_helpers import *
import class_merger as mrg
import config as orm

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
            'covariates'],
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
            'projid',
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
            'authors', 'authors_contact', 'metalink', 'knbid'],
        'time': False,
        'cov': False,
        'depend': False
    }
    taxatable = {
        'columns': [
            'projid', 'sppcode', 'kingdom', 'phylum', 'clss',
            'order','family', 'genus', 'species', 'authority'],
        'time': False,
        'cov': False,
        'depend': True
    }
    rawtable = {
        'columns': [
            'taxaid', 'projid', 'year', 'month', 'day',
            'spt_rep1', 'spt_rep2', 'spt_rep3', 'spt_rep4',
            'structure', 'individ', 'unitobs', 'covariates'],
        'time': True,
        'cov': True ,
        'depend': True
    }

    tabledict = {
        'climaterawtable': climaterawtable,
        'stationtable': stationtable,
        'sitetable': sitetable,
        'maintable': maintable,
        'taxatable': taxatable,
        'rawtable': rawtable
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

    def get_time_status(self):
        return  self.tabledict[
            self._inputs.tablename]['time']

    @abc.abstractmethod
    def get_time_data(self):
        pass

    def get_cov_status(self):
        return self.tabledict[
            self._inputs.tablename]['cov']

    @abc.abstractmethod
    def get_cov_data(self):
        pass


    def get_dependent_status(self):
        return self.tabledict[
            self._inputs.tablename]['depend']

    @abc.abstractmethod
    def get_dependent_data(self):
        pass

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
        try:
            assert acols is not None
        except Exception as e:
            print(str(e))
            raise AssertionError('Columns names not set')
        try:
            assert dataframe is not None
        except Exception as e:
            print(str(e))
            raise AssertionError('Raw dataframe not set')
        if 'lterid' in dbcol:
            dbcol.remove('lterid')
        else:
            pass
        if 'lterid' in nullcols:
            nullcols.remove('lterid')
        else:
            pass
        uniquesubset = dataframe[acols]
        nullsubset = produce_null_df(
            ncols=len(nullcols),
            colnames=nullcols,
            dflength=len(uniquesubset),
            nullvalue='NaN')

        concat =  pd.concat(
            [uniquesubset, nullsubset], axis=1).reset_index(
                drop=True)
        final = concat.drop_duplicates().reset_index(drop=True) 
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
        try:
            assert acols is not None
        except Exception as e:
            print(str(e))
            raise AssertionError('Columns names not set')
        try:
            assert dataframe is not None
        except Exception as e:
            print(str(e))
            raise AssertionError('Raw dataframe not set')
        if 'projid' in dbcol:
            dbcol.remove('projid')
        else:
            pass
        if 'projid' in nullcols:
            nullcols.remove('projid')
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
             'sp_rep4_label', 'sp_rep4_uniquelevels'
        ]

        # Creating main data table
        maindata = pd.DataFrame(
            {
                'metarecordid':dataframe['global_id'], 
                'title': dataframe['title'],
                'samplingunits': 'NULL',
                'samplingprotocol': dataframe['data_type'],
                'structured': 'NULL',
                'studystartyr': 'NULL',
                'studyendyr': 'NULL',
                'siteid': 'NULL',
                'sitestartyr': 'NULL',
                'siteendyr': 'NULL',
                'samplefreq': dataframe['temp_int'],
                'totalobs': 'NULL',
                'studytype': dataframe['study_type'],
                'community': dataframe['comm_data'],
                'uniquetaxaunits': 'NULL',
                # Spatial repliaction attributes
                'sp_rep1_ext': 'NULL',
                'sp_rep1_ext_units': 'NULL',
                'sp_rep1_label': 'NULL',
                'sp_rep1_uniquelevels': 'NULL',
                'sp_rep2_ext': 'NULL,',
                'sp_rep2_ext_units': 'NULL',
                'sp_rep2_label': 'NULL',
                'sp_rep2_uniquelevels': 'NULL',
                'sp_rep3_ext': 'NULL',
                'sp_rep3_ext_units': 'NULL',
                'sp_rep3_label': 'NULL',
                'sp_rep3_uniquelevels': 'NULL',
                'sp_rep4_ext': 'NULL',
                'sp_rep4_ext_units': 'NULL',
                'sp_rep4_label': 'NULL',
                'sp_rep4_uniquelevels': 'NULL',
                'authors': 'NULL',
                'authors_contact': 'NULL',
                'metalink': dataframe['site_metadata'],
                'knbid': dataframe['portal_id']
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
            'authors', 'authors_contact', 'metalink', 'knbid'
            ], index=[0])

        concat =  pd.concat(
            [maindata]*len(sitelevels))
        concat['siteid'] = sitelevels
        back = [x for x in concat.columns if x not in autoupdated]
        return concat[back]

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
            assert acols is not None
        except Exception as e:
            print(str(e))
            raise AssertionError('Columns names not set')
        try:
            assert dataframe is not None
        except Exception as e:
            print(str(e))
            raise AssertionError('Raw dataframe not set')
        if 'projid' in dbcol:
            dbcol.remove('projid')
        else:
            pass
        if 'projid' in nullcols:
            nullcols.remove('projid')
        else:
            pass

        dbcolrevised = [x for x in dbcol if x not in nullcols]
        uniquesubset_site_list = []
        self.dependentdf = produce_null_df(
            ncols=2, colnames=['uniquetaxaunits', 'siteid'],
            dflength=len(sitelevels), nullvalue='NULL'
        )
        for i,item in enumerate(sitelevels):                
            unqdf = dataframe[dataframe[siteid]==item]
            uniquesubset = unqdf[acols]
            unique = uniquesubset.drop_duplicates()
            unique = unique.reset_index(drop=True)
            self.dependentdf[
                'uniquetaxaunits'].iloc[i] = len(uniquesubset)
            self.dependentdf['siteid'].iloc[i] = item

            sitelevel = produce_null_df(
                ncols=len(unique),
                colnames=[siteid],
                dflength=len(unique),
                nullvalue=item)
            nullsubset = produce_null_df(
                ncols=len(nullcols),
                colnames=nullcols,
                dflength=len(unique),
                nullvalue='NaN')

            unique = pd.concat(
                [unique,nullsubset,sitelevel], axis=1)
            uniquesubset_site_list.append(unique)

        final = uniquesubset_site_list[0]
        for i,item in enumerate(uniquesubset_site_list):
            if i > 0:
                final = pd.concat([final,item], ignore_index=True)
            else:
                pass

        for i,item in enumerate(dbcolrevised):
            final.rename(
                columns={acols[i]:item},
                inplace=True)

        query_class = mrg.Merger(globalid)
        sitefilter = sitelevels
        q_data = query_class.query_database(
            'maintable', sitefilter)
        taxa_merge = pd.merge(
            final, q_data,
            left_on=siteid, right_on='siteid',
            how='left'
        )

        self.dependentdf = pd.merge(
            taxa_merge, self.dependentdf,
            left_on='siteid', right_on='siteid',
            how='left'
        )


        dbcol.insert(0,'projid')
        return taxa_merge[dbcol]

    def get_dependent_data(self):
        maindata = self.dependentdf[
            ['projid','uniquetaxaunits_y']].drop_duplicates()
        maindata.columns = ['projid', 'uniquetaxaunits']
        maindata = maindata.reset_index()
        mainqueries = {}

        try:
            for i in range(len(maindata)):
                mainqueries[i] = orm.session.query(
                    orm.Maintable).filter(
                        orm.Maintable.projid ==
                        maindata['projid'][i])
                mainqueries[i].one().uniquetaxaunits = (
                    maindata['uniquetaxaunits'][i])
            orm.session.flush()
        except Exception as e:
            print(str(e))
            raise ValueError(
                'Could not modified maintable uniquetaxaunits')

class DatabaseTable:
    def __init__(self):
        self._name = None
        self._cols = None
        self._null = None
        self._availcols = None
        self._availdf = None
        self._time = None
        self._timedf = None
        self._cov = None
        self._covdf = None
        self._depend = None
        self._dependdf = None
        self._foreigndf = None

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

    def set_time_status(self, timebool):
        self._time = timebool

    def set_cov_status(self, covbool):
        self._cov = covbool

    def set_dependent_status(self, dependitems):
        self._depend = dependitems

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
            raise AssertionError('Data not set')

    def set_globalid(self, globalid):
        try:
            assert globalid is not None
        except Exception as e:
            print(str(e))
            raise AttributeError('Global Id is not registered')
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

        time = self._builder.get_time_status()
        dbtable.set_time_status(time)

        cov = self._builder.get_cov_status()
        dbtable.set_cov_status(cov)

        dep = self._builder.get_dependent_status()
        dbtable.set_dependent_status(dep)
        print(dep)
        if dep is True:
            print('in the build block')
            self._builder.get_dependent_data()
            print('executed the dependent command')
        else:
            pass

        return dbtable
