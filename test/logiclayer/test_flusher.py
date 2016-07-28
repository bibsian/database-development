import pytest
import pandas as pd
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

from test.logiclayer import class_helpers as hlp
from test.logiclayer import class_userfacade as face
from test.logiclayer import class_timeparse as tparse
from test.logiclayer import class_dictionarydataframe as ddf
from test.logiclayer.datalayer import config as orm
os.chdir(rootpath)
import class_inputhandler as ini

@pytest.fixture
def site_add():
    def site_add(df, tablekey, ormreg, session):
        for i in range(len(df)):

            try:
                ormreg[i] = orm.Sitetable(
                    siteid = df.loc[i, tablekey])
                session.add(ormreg[i])
            except Exception as e:
                session.rollback()
                print(str(e))
                raise ValueError('Could not map Site data')
    return site_add

@pytest.fixture
def main_add():
    def main_add(df, tablekey, ormreg, session):

        try:
            for i in range(len(df)):
                ormreg[i] = orm.Maintable(
                    siteid = df.loc[i, tablekey])
                session.add(ormreg[i])
        except Exception as e:
            session.rollback()
            print(str(e))
            raise ValueError('Could not map Main data')

    return main_add

@pytest.fixture
def taxa_add():
    def taxa_add(df, tablekey, ormreg, session):
        try:
            for i in range(len(df)):
                ormreg[i] = orm.Taxatable(
                    lter_proj_site = df.loc[i, tablekey])
                session.add(ormreg[i])
        except Exception as e:
            session.rollback()
            print(str(e))
            raise ValueError('Could not map Taxa data')
    return taxa_add

@pytest.fixture
def raw_add():
    def raw_add(df, tablekey, ormreg, session):
        try:
            for i in range(len(df)):
                ormreg[i] = orm.Rawtable(
                    taxaid = df.loc[i, tablekey])
                session.add(ormreg[i])
        except Exception as e:
            session.rollback()
            print(str(e))
            raise ValueError('Could not map Raw data')
    return raw_add


@pytest.fixture
def Flusher(site_add, main_add, taxa_add, raw_add):

    class Flusher(object):
        
        def __init__(
                self, dataframe, tablename, tablekey, lterid):
            self.df = dataframe
            self.tablename = tablename
            self.pk = tablekey
            self.lterid = lterid
            self.ormreg = {}
            self.ormtable = {
                'sitetable': site_add,

                'maintable': main_add,

                'taxatable': taxa_add,

                'rawtable': raw_add
            }

        def database_check(self, comparelist):
            print('in check block')
            comparelist = list(comparelist)
            session = orm.Session()
            if self.tablename == 'sitetable':
                maincheck = session.query(
                    orm.Sitetable.siteid).order_by(
                        orm.Sitetable.siteid).filter(
                            orm.Sitetable.lterid == self.lterid)
            elif self.tablename == 'maintable':
                maincheck = session.query(
                    orm.Maintable.metarecordid).order_by(
                        orm.Maintable.metarecordid)
            elif self.tablename == 'taxatable':
                maincheck = session.query(
                    orm.Taxatable.lter_proj_site).order_by(
                        orm.Taxatable.lter_proj_site)
            elif self.tablename == 'rawtable':
                maincheck = session.query(
                    orm.Rawtable.lter_proj_site).order_by(
                        orm.Rawtable.lter_proj_site)
            session.close()
            print('session closes in check')
            maincheckdf = pd.read_sql(
                maincheck.statement, maincheck.session.bind)

            if maincheckdf is not None:
                if len(maincheckdf) == 0:
                    return True
                else:
                    records_entered = maincheckdf[
                        self.pk].values.tolist()
                    check = [
                        x for x in comparelist
                        if x in list(set(records_entered))]
                    return len(check) == 0
            else:
                return True
                
        def go(self, session):
            '''
            method to a
            '''
            self.ormtable[self.tablename](
                self.df, self.pk, self.ormreg, session)

            try:
                for i in range(len(self.df)):
                    dbupload = self.df.loc[
                        i, self.df.columns].to_dict()
                    for key in dbupload.items():
                        setattr(
                            self.ormreg[i], key[0], key[1])
                        session.add(self.ormreg[i])
                session.flush()
                session.commit()
            except Exception as e:
                session.rollback()
                del session
                print(str(e))
                raise ValueError(
                    'Could not update '+self.tablename+' values')
    return Flusher

@pytest.fixture
def flush(Flusher):
    def flush(df,tablename,log,lter, sess):
        save_data = df

        if (tablename == 'sitetable' and
            save_data.loc[0, 'siteid'] in ['NULL', 'null'] and
            len(save_data) == 1 ):
            log.debug('Skipping database transaction')
        else:
            log.debug('Making database transaction')
            try:
                if tablename == 'sitetable':
                    flush = Flusher(
                        save_data,
                        tablename,
                        'siteid',
                        lter)
                    ck = flush.database_check(
                        save_data['siteid'].values.tolist())
                elif tablename == 'maintable':
                    flush = Flusher(
                        save_data,
                        tablename,
                        'metarecordid',
                        lter)
                    ck = flush.database_check(
                        save_data['metarecordid'].values.tolist())
                elif tablename == 'taxatable':
                    flush = Flusher(
                        save_data,
                        tablename,
                        'lter_proj_site',
                        lter)
                    ck = flush.database_check(
                        save_data['lter_proj_site'].values.tolist())
                elif tablename == 'rawtable':
                    flush = Flusher(
                        save_data,
                        tablename,
                        'lter_proj_site',
                        lter)
                    ck = flush.database_check(
                        save_data['lter_proj_site'].values.tolist())

                log.debug(
                    'past database check: ' + tablename + str(ck))
                if ck is True:
                    flush.go(sess)
                else:
                    pass
            except Exception as e:
                print(str(e))
                log.debug(str(e))
                raise ValueError(str(e))
    return flush

@pytest.fixture
def site_table():
    return pd.read_csv('DatabaseConfig/site_table_test.csv')

@pytest.fixture
def main_table():
    return pd.read_csv('DatabaseConfig/main_table_test.csv')


@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 8,
        'metaurl': 'http://sbc.test.rice.com',
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def filehandle():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename='Datasets_manual_test/raw_data_test_2.csv')

    return fileinput

@pytest.fixture
def sitehandle():
    lned = {'siteid': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle

@pytest.fixture
def mainhandle():
    main_input = ini.InputHandler(
        name='maininfo', tablename='maintable')
    return main_input

@pytest.fixture
def taxahandle():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('phylum', 'TAXON_PHYLUM'),
        ('class', 'TAXON_CLASS'),
        ('order', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('phylum', True),
        ('class', True),
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
        name='taxainfo',
        tablename='taxatable',
        lnedentry= hlp.extract(taxalned, available),
        checks=taxacreate)
    return taxaini


@pytest.fixture
def timehandle():
    d = {
        'dayname': 'jd',
        'dayform': 'julian day',
        'monthname': '',
        'monthform': 'NULL',
        'yearname': 'YEAR',
        'yearform': 'YYYY',
        'jd': True,
        'mspell': False
    }
    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)


    return timeini


@pytest.fixture
def obshandle():
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

@pytest.fixture
def covarhandle():
    covarlned = {'columns': None}
    
    covarlned['columns'] = hlp.string_to_list(
        'DEPTH, TEMP, PRECIP'
    )

    covarini = ini.InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)

    return covarini

    
# TESTED ON EMPYTE DATABASE
# If testing on populated database be sure
# siteid's are unique as well as metadatarecord_id's
def test_site_main_flush_commit(
        filehandle, sitehandle, metahandle,
        mainhandle, taxahandle, timehandle,
        obshandle, covarhandle, flush):
    facade = face.Facade()
    facade._valueregister['globalid'] = metahandle.lnedentry[
        'globalid']
    facade._valueregister['lterid'] = metahandle.lnedentry['lter']

    facade.input_register(metahandle)
    facade.meta_verify()

    facade.input_register(filehandle)
    facade.load_data()

    facade.input_register(sitehandle)
    sitedirector = facade.make_table('siteinfo')
    sitetable = sitedirector._availdf
    lter = metahandle.lnedentry['lter']
    ltercol = hlp.produce_null_df(1,['lterid'],len(sitetable),lter)
    sitetable = pd.concat([sitetable, ltercol], axis=1)
    print('sitetable: ', sitetable)

    sitelevels = facade._data[
        'SITE'].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    
    facade.input_register(mainhandle)
    maindirector = facade.make_table('maininfo')
    maintable = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(maintable, orm.maintypes)
    print('maintable: ', maintable)
    orm.convert_types(maintable, orm.maintypes)

    facade.input_register(taxahandle)
    taxadirector = facade.make_table('taxainfo')
    taxatable = taxadirector._availdf

    facade.input_register(timehandle)
    timetable = tparse.TimeParse(
        facade._data, timehandle.lnedentry)
    facade.input_register(obshandle)

    facade.input_register(obshandle)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf

    facade.input_register(covarhandle)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covarhandle.lnedentry['columns']).convert_records()

    rawdata = facade._data

    lter = facade._valueregister['lterid']
    facade.create_log_record('sitetable')
    facade.create_log_record('maintable')

    session = orm.Session()
    # Flushing the first two data tables
    flush(
        sitetable, 'sitetable',
        facade._tablelog['sitetable'], lter, session)
    flush(
        maintable, 'maintable',
        facade._tablelog['maintable'], lter, session)
    session.commit()
