#!usr/bin/env python

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
        'cov': True
    }

    stationtable = {
        'columns': ['lterid', 'lat', 'lng', 'descript'],
        'time': False,
        'cov': False
    }
    sitetable = {
        'columns': ['siteid', 'lat', 'lng', 'descript'],
        'time': False,
        'cov': False
    }

    maintable = {
        'columns': [
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
        'cov': False
    }
    taxatable = {
        'columns': [
            'projid', 'sppcode', 'kingdom', 'phylum', 'class',
            'order','family', 'genus', 'species', 'authority'],
        'time': False,
        'cov': False
    }
    rawtable = {
        'columns': [
            'taxaid', 'projid', 'year', 'month', 'day',
            'spt_rep1', 'spt_rep2', 'spt_rep3', 'spt_rep4',
            'structure', 'individ', 'unitobs', 'covariates'],
        'time': True,
        'cov': True }

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

    def get_null_columns(self):
        availcol = list(self._inputs.lnedentry.keys())
        allcol = self.tabledict[
            self._inputs.tablename]['columns']
        return list(set(allcol).difference(availcol))

    @abc.abstractmethod
    def get_time_data(self):
        pass

    @abc.abstractmethod
    def get_covariates(self):
        pass

    @abc.abstractmethod
    def get_dependencies(self):
        pass

    @abc.abstractmethod
    def get_foreign_key(self):
        pass

class SiteTableBuilder(AbstractTableBuilder):
    '''
    Concrete table builder implementation: Site
    '''

    def get_time_data(self):
        return  self.tabledict[
            self._inputs.tablename]['time']

    def get_covariates(self):
        return self.tabledict[
            self._inputs.tablename]['cov']

    def get_dependencies(self):
        pass

    def get_foreign_key(self):
        pass

class DatabaseTable:
    def __init__(self):
        self._name = None
        self._cols = list()
        self._null = list()
        self._time = None
        self._cov = None
        self._data = None
        self._depend = None
        self._foreign = list()

    def set_table_name(self, tablename):
        self._name = tablename

    def set_columns(self, colnames):
        self._cols = colnames

    def set_null_columns(self, nullcol):
        self._null = nullcol

    def set_time_data(self, timebool):
        self._time = timebool

    def set_covariates(self, covbool):
        self._cov = covbool

    def set_dependencies(self, dependitems):
        self._depend = dependitems

    def set_foreign_key(self):
        pass

class TableDirector:
    '''Constructs database tables'''
    _inputs = None
    _name = None
    _builder = None

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

        nullcol = self._builder.get_null_columns()
        dbtable.set_null_columns(nullcol)

        time = self._builder.get_time_data()
        if time == True:
            pass
        else:
            dbtable.set_time_data(time)

        cov = self._builder.get_covariates()
        if cov == True:
            pass
        else:
            dbtable.set_covariates(cov)

        return dbtable
