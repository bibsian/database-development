#! /usr/bin/env python
import pytest
from pandas import concat, DataFrame, read_csv
import abc
from collections import OrderedDict
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Dropbox/database-development/" +
        "test/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
import class_helpers as hlp
import class_userfacade as face
os.chdir(rootpath)
import class_inputhandler as ini




@pytest.fixture
def AbstractTableBuilder():
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
                'authors', 'authors_contact', 'metalink', 'knbid'],
            'time': False,
            'cov': False,
            'depend': False
        }
        taxatable = {
            'columns': [
                'lter_proj_site', 'sppcode', 'kingdom', 'phylum', 'clss',
                'order','family', 'genus', 'species', 'authority'],
            'time': False,
            'cov': False,
            'depend': True
        }
        rawtable = {
            'columns': [
                'taxaid', 'lter_proj_site', 'year', 'month', 'day',
                'spt_rep1', 'spt_rep2', 'spt_rep3', 'spt_rep4',
                'structure', 'individ', 'unitobs', 'covariates'],
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
                'sp_rep4_label', 'sp_rep4_uniquelevels'
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

    return AbstractTableBuilder

@pytest.fixture
def SiteTableBuilder(AbstractTableBuilder):
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
            uniquesubset = dataframe[acols]
            nullsubset = hlp.produce_null_df(
                ncols=len(nullcols),
                colnames=nullcols,
                dflength=len(uniquesubset),
                nullvalue='NaN')
            _concat =  concat(
                [uniquesubset, nullsubset], axis=1).reset_index(
                    drop=True)
            final = _concat.drop_duplicates().reset_index(drop=True) 

            final.columns =dbcol
            return final
                
        
    return SiteTableBuilder

@pytest.fixture
def MainTableBuilder(AbstractTableBuilder):
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
                 'sp_rep4_label', 'sp_rep4_uniquelevels'
            ]

            # Creating main data table
            maindata = DataFrame(
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
                    'sp_rep2_ext': 'NULL',
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

            _concat =  concat(
                [maindata]*len(sitelevels))
            _concat['siteid'] = sitelevels
            back = [x for x in _concat.columns if x not in autoupdated]
            return _concat[back]
        
    return MainTableBuilder

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
                    nullvalue='NaN')

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
                nullvalue='NaN')
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

            updatedf = hlp.produce_null_df(
                len(dbcol), dbcol, len(sitelevels), 'NULL')
            updatedf['siteid'] = sitelevels
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

            adata = self._builder.get_dataframe(
                self._rawdata, acolumns, nullcol, columns,
                self._globalid, self._siteid, self._sitelevels)

            dbtable.set_dataframe(adata)

            return dbtable

    return TableDirector

@pytest.fixture
def user_input():
    lned = {'siteid': 'SITE'}
    user_input = ini.InputHandler(
        name='siteinfo', tablename='sitetable', lnedentry=lned)
    return user_input

@pytest.fixture
def df():
    return read_csv('Datasets_manual_test/raw_data_test_2.csv')

def test_sitetable_build(
        SiteTableBuilder, TableDirector, user_input, df):
    '''
    Testing builder classes
    '''
    facade = face.Facade()
    facade.input_register(user_input)
    face_input = facade._inputs[user_input.name]
    assert (isinstance(face_input, ini.InputHandler)) is True

    sitetable = SiteTableBuilder()
    assert (isinstance(sitetable, SiteTableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(sitetable)
    director.set_data(df)

    sitetab = director.get_database_table()
    showsite = sitetab._availdf
    assert (isinstance(showsite, DataFrame)) is True
    
def test_error_builds(SiteTableBuilder, TableDirector, user_input):
    pass


@pytest.fixture
def main_user_input():
    ui = ini.InputHandler(name='maininfo', tablename='maintable')
    return ui

@pytest.fixture
def metadf():
    if sys.platform == "darwin":
        metapath = (
            "/Users/bibsian/Dropbox/database-development/test/Datasets_manual_test/" +
            "meta_file_test.csv")
            
    elif sys.platform == "win32":
        #=======================#
        # Paths to data and conversion of files to dataframe
        #=======================#
        metapath = (
            "C:\\Users\MillerLab\\Dropbox\\database-development" +
            "\\test\\Datasets_manual_test\\meta_file_test.csv")

    metadf = read_csv(metapath, encoding="iso-8859-11")
    return metadf
    
def test_maintable_build(
        MainTableBuilder, TableDirector, main_user_input, metadf, df):

    sitelevels = df['SITE'].values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(main_user_input)
    face_input = facade._inputs[main_user_input.name]

    assert (isinstance(face_input, ini.InputHandler)) is True
    maintable = MainTableBuilder()
    assert (isinstance(maintable, MainTableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(maintable)
    director.set_data(metadf)    
    director.set_sitelevels(sitelevels)

    maintab = director.get_database_table()
    showmain = maintab._availdf
    print(showmain)
    assert (isinstance(showmain, DataFrame)) is True
    

@pytest.fixture
def taxa_user_input():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', 'TAXON_KINGDOM'),
        ('phylum', 'TAXON_PHYLUM'),
        ('clss', 'TAXON_CLASS'),
        ('order', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', True),
        ('phylum', True),
        ('clss', True),
        ('order', True),
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
    
    taxaini = ini.InputHandler(
        name='taxainput',
        tablename='taxatable',
        lnedentry= hlp.extract(taxalned, available),
        checks=taxacreate)
    return taxaini

@pytest.fixture
def taxadfexpected():
    return read_csv('DatabaseConfig/taxa_table_test.csv')

def test_taxatable_build(
        TaxaTableBuilder, TableDirector, taxa_user_input, df,
        taxadfexpected):
    sitelevels = df['SITE'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(taxa_user_input)
    face_input = facade._inputs[taxa_user_input.name]
    taxabuilder = TaxaTableBuilder()
    assert (isinstance(taxabuilder, TaxaTableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(taxabuilder)
    director.set_data(df)
    director.set_globalid(2)
    director.set_siteid('SITE')
    director.set_sitelevels(sitelevels)
    
    taxatable = director.get_database_table()
    showtaxa = taxatable._availdf
    assert isinstance(showtaxa,DataFrame)    

    testphylum = showtaxa['phylum'].values.tolist()
    testorder = showtaxa['order'].values.tolist()
    testspecies = showtaxa['species'].values.tolist()

    truephylum = taxadfexpected['phylum'].values.tolist()
    trueorder = taxadfexpected['order'].values.tolist()
    truespecies = taxadfexpected['species'].values.tolist()

#    assert (testphylum == truephylum) is True
#    assert (testorder == trueorder) is True
#    assert (testspecies == truespecies) is True

@pytest.fixture
def taxa_user_input_create():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', 'TAXON_KINGDOM'),
        ('phylum', 'TAXON_PHYLUM'),
        ('clss', 'TAXON_CLASS'),
        ('order', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', 'Animalia'),
        ('kingdom', True),
        ('phylum', True),
        ('clss', True),
        ('order', True),
        ('family', True),
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
    
    taxaini = ini.InputHandler(
        name='taxainput',
        tablename='taxatable',
        lnedentry= hlp.extract(taxalned, available),
        checks=taxacreate)
    return taxaini

def test_taxatable_build_create(
        TaxaTableBuilder, TableDirector, taxa_user_input_create, df,
        taxadfexpected):
    sitelevels = df['SITE'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(taxa_user_input_create)
    face_input = facade._inputs[taxa_user_input_create.name]
    taxabuilder = TaxaTableBuilder()
    assert (isinstance(taxabuilder, TaxaTableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(taxabuilder)
    director.set_data(df)
    director.set_globalid(2)
    director.set_siteid('SITE')
    director.set_sitelevels(sitelevels)
    
    taxatable = director.get_database_table()
    showtaxa = taxatable._availdf
    assert isinstance(showtaxa,DataFrame)    
    print(showtaxa)

    testphylum = showtaxa['phylum'].values.tolist()
    testorder = showtaxa['order'].values.tolist()
    testspecies = showtaxa['species'].values.tolist()

    truephylum = taxadfexpected['phylum'].values.tolist()
    trueorder = taxadfexpected['order'].values.tolist()
    truespecies = taxadfexpected['species'].values.tolist()

#    assert (testphylum == truephylum) is True
#    assert (testorder == trueorder) is True
#    assert (testspecies == truespecies) is True
    
@pytest.fixture
def raw_userinput():
    obslned = OrderedDict((
        ('spt_rep2', 'PLOT'),
        ('spt_rep3', ''),
        ('spt_rep4', ''),
        ('structure', ''),
        ('individ', ''),
        ('unitobs', 'COUNT')
    ))
    
    obsckbox = OrderedDict((
        ('spt_rep2', False),
        ('spt_rep3', True),
        ('spt_rep4', True),
        ('structure', True),
        ('individ', True),
        ('unitobs', False)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is False
    ]

    rawini = ini.InputHandler(
        name='rawinfo',
        tablename='rawtable',
        lnedentry= hlp.extract(obslned, available),
        checks=obsckbox)

    return rawini
    
def test_rawtable_build(
        TableDirector, raw_userinput, df, RawTableBuilder):
    sitelevels = df['SITE'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(raw_userinput)
    face_input = facade._inputs[raw_userinput.name]
    rawbuilder = RawTableBuilder()
    assert (isinstance(rawbuilder, RawTableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(rawbuilder)
    director.set_data(df)
    director.set_globalid(2)
    director.set_siteid('SITE')
    director.set_sitelevels(sitelevels)
    rawtable = director.get_database_table()
    showraw = rawtable._availdf

    counttest = showraw['unitobs'].values.tolist()
    counttrue = df['COUNT'].values.tolist()

    sitetest = showraw['spt_rep1'].values.tolist()
    sitetrue = df['SITE'].values.tolist()

    assert (counttest == counttrue) is True
    assert (sitetest == sitetrue) is True

def test_update_table(
        TableDirector, raw_userinput, df, UpdaterTableBuilder):
    sitelevels = df['SITE'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(raw_userinput)
    face_input = facade._inputs[raw_userinput.name]
    updatebuilder = UpdaterTableBuilder()
    assert (isinstance(updatebuilder, UpdaterTableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(updatebuilder)
    director.set_data(df)
    director.set_globalid(2)
    director.set_siteid('SITE')
    director.set_sitelevels(sitelevels)
    updatedf = director.get_database_table()
    showupdate = updatedf._availdf
    print(showupdate)
    assert isinstance(showupdate, DataFrame) is True
    assert (len(showupdate) == len(sitelevels)) is True
