import pytest
import pandas as pd
import config as orm
from collections import OrderedDict
import class_helpers as hlp
import class_inputhandler as ini
import class_userfacade as face
import class_timeparse as tparse
import class_dictionarydataframe as ddf
import class_flusher as flsh

@pytest.fixture
def site_add():
    
    def site_add(df, tablekey, ormreg):
        for i in range(len(df)):
            ormreg[i] = orm.Sitetable(
                siteid = df.loc[i, tablekey])
            orm.session.add(ormreg[i])
    return site_add

@pytest.fixture
def main_add():
    def main_add(df, tablekey, ormreg):
        for i in range(len(df)):
            ormreg[i] = orm.Maintable(
                siteid = df.loc[i, tablekey])
            orm.session.add(ormreg[i])
    return main_add

@pytest.fixture
def taxa_add():
    def taxa_add(df, tablekey, ormreg):
        for i in range(len(df)):
            ormreg[i] = orm.Taxatable(
                projid = df.loc[i, tablekey])
            orm.session.add(ormreg[i])
    return taxa_add


@pytest.fixture
def raw_add():
    def raw_add(df, tablekey, ormreg):
        for i in range(len(df)):
            ormreg[i] = orm.Rawtable(
                taxaid = df.loc[i, tablekey])
            orm.session.add(ormreg[i])
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

            self.table_check = {
                'sitetable': orm.session.query(
                    orm.Sitetable.siteid).order_by(
                        orm.Sitetable.siteid).filter(
                            orm.Sitetable.lterid == self.lterid),

                'maintable': orm.session.query(
                    orm.Maintable.metarecordid).order_by(
                        orm.Maintable.metarecordid)
            }

        def database_check(self, comparelist):
            comparelist = list(comparelist)
            maincheck = self.table_check[self.tablename]
            maincheckdf = pd.read_sql(
                maincheck.statement, maincheck.session.bind)

            if maincheckdf is not None:
                if len(maincheckdf) == 0:
                    return True
                else:
                    records_entered = maincheckdf[
                        self.pk].values.tolist()
                    check = [
                        x for x in list(
                            set(records_entered)) if x in comparelist]
                    return len(check) == 0
            else:
                return True
                
        def go(self):
            '''
            method to a
            '''
            self.ormtable[self.tablename](
                self.df, self.pk, self.ormreg)
            
            for i in range(len(self.df)):
                dbupload = self.df.loc[
                    i, self.df.columns].to_dict()
                for key in dbupload.items():
                    setattr(
                        self.ormreg[i], key[0], key[1])
                    orm.session.add(self.ormreg[i])
            orm.session.flush()

    return Flusher

@pytest.fixture
def site_table():
    return pd.read_csv('DatabaseConfig/site_table_test.csv')

@pytest.fixture
def main_table():
    return pd.read_csv('DatabaseConfig/main_table_test.csv')


@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 2,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.17'),
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
        filename='DatabaseConfig/raw_data_test.csv')

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
        'dayname': 'DATE',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'DATE',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'DATE',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)


    return timeini


@pytest.fixture
def obshandle():
    obslned = OrderedDict((
        ('spt_rep2', ''),
        ('spt_rep3', ''),
        ('spt_rep4', ''),
        ('structure', ''),
        ('individ', ''),
        ('unitobs', 'COUNT')
    ))
    
    obsckbox = OrderedDict((
        ('spt_rep2', False),
        ('spt_rep3', False),
        ('spt_rep4', False),
        ('structure', False),
        ('individ', False),
        ('unitobs', True)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is True
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
        'DEPTH'
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
        obshandle, covarhandle):
    facade = face.Facade()

    facade.input_register(metahandle)
    facade.meta_verify()

    facade.input_register(filehandle)
    facade.load_data()

    facade.input_register(sitehandle)
    sitedirector = facade.make_table('siteinfo')
    sitetable = sitedirector._availdf

    sitelevels = facade._data[
        'SITE'].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)

    
    facade.input_register(mainhandle)
    maindirector = facade.make_table('maininfo')
    maintable = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(maintable, orm.maintypes)
    print(maintable.columns.values.tolist())
    
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

    globalid = facade._valueregister['globalid']
    lter = facade._valueregister['lterid']
    
    # Flushing the first two data tables
    siteflush = flsh.Flusher(sitetable, 'sitetable', 'siteid', lter)
    ck = siteflush.database_check(
        sitetable['siteid'].values.tolist())
    assert ck is True
    siteflush.go()
    orm.session.flush()

    mainflush = flsh.Flusher(maintable, 'maintable', 'siteid', lter)
    ck = mainflush.database_check(
        maintable['siteid'].values.tolist())
    assert ck is True
    mainflush.go()

    # Commit the first two flushes
    # This is necessary to retrieve primary keys
    orm.session.commit()
