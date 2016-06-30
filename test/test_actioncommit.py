#!/usr/bin/env python
import pytest
import pandas as pd
from collections import OrderedDict
import config as orm
import class_helpers as hlp
import class_inputhandler as ini
import class_userfacade as face
import class_timeparse as tparse
import class_dictionarydataframe as ddf
import class_flusher as flsh
import class_merger as mrg

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
        ('clss', 'TAXON_CLASS'),
        ('order', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
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
        ('spt_rep2', 'REP'),
        ('spt_rep3', 'SP_CODE'),
        ('spt_rep4', ''),
        ('structure', ''),
        ('individ', ''),
        ('unitobs', 'COUNT')
    ))
    
    obsckbox = OrderedDict((
        ('sp_rep2_label', True),
        ('sp_rep3_label', True),
        ('sp_rep4_label', False),
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

# Performed on EMPTY DATABASE ONCE!!
# If database is not empty, records will keep
# being added
@pytest.fixture
def updatehandle():
    update_input = ini.InputHandler(
        name='updateinfo', tablename='updatetable')
    return update_input

def test_merger_data(
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
    facade._valueregister['siteid'] = 'SITE'

    
    facade.input_register(mainhandle)
    maindirector = facade.make_table('maininfo')
    maintable = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(maintable, orm.maintypes)
    
    facade.input_register(taxahandle)
    taxadirector = facade.make_table('taxainfo')
    taxatable = taxadirector._availdf

    facade.input_register(timehandle)
    timetable = tparse.TimeParse(
        facade._data, timehandle.lnedentry).formater()
    facade.input_register(obshandle)

    facade.input_register(obshandle)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf

    facade.input_register(covarhandle)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covarhandle.lnedentry['columns']).convert_records()

    
    # Stored Variables
    globalid = facade._valueregister['globalid']
    lter = facade._valueregister['lterid']
    siteid = facade._valueregister['siteid']
    sitelevels = facade._valueregister['sitelevels']
    rawdata = facade._data

    sitetable.loc[:,'lterid'] = lter
    
    # Commit the first two flushes
    # This is necessary to retrieve primary keys
    siteflush = flsh.Flusher(sitetable, 'sitetable', 'siteid', lter)
    ck = siteflush.database_check(
        sitetable['siteid'].values.tolist())
    assert ck is True
    siteflush.go()
    orm.session.commit()
    
    mainflush = flsh.Flusher(maintable, 'maintable', 'siteid', lter)
    ck = mainflush.database_check(
        maintable['siteid'].values.tolist())
    assert ck is True
    mainflush.go()
    orm.session.commit()

    # Merging Maintable data to rawdata (post maindata commit) 
    q1 = mrg.Merger(globalid)
    mainquery = q1.query_database('maintable', sitelevels)
    rawmain_merge = pd.merge(
        rawdata, mainquery,
        left_on=siteid, right_on='siteid', how='left')
    facade._datamerged['raw_main'] = rawmain_merge

    # Editing taxa columns for raw-taxa merge
    taxa_formated_cols = list(
        facade._inputs['taxainfo'].lnedentry.keys())
    taxa_formated_cols.append(siteid)
    taxa_og_cols = list(
        facade._inputs['taxainfo'].lnedentry.values())
    taxa_og_cols.append(siteid)
    # Merged raw data with taxatable data (via a main merge)
    rawtaxa_merge = pd.merge(
        taxatable, rawmain_merge,
        how='inner',
        left_on=taxa_formated_cols, right_on=taxa_og_cols   
    )
    
    # Appended taxatable with projid's
    taxa_all_columns = taxatable.columns.values.tolist()
    taxa_all_columns.append('projid')
    taxa_all_columns.remove(siteid)
    taxapush = rawtaxa_merge[
        taxa_all_columns].drop_duplicates().reset_index(drop=True)
    taxaflush = flsh.Flusher(taxapush, 'taxatable', 'projid', lter)
    taxaflush.go()
    orm.session.commit()

    # Making list of projid's to filter our taxatable query
    projids = list(set(taxapush['projid']))
    taxaquery = q1.query_database('taxatable', projids)
    # Appending taxatable columns for taxamerge with
    # taxaquery (this gets us taxaid's) i.e. full
    # rawdata/database primary keys merge
    taxa_formated_cols.remove(siteid)
    taxa_og_cols.remove(siteid)
    taxa_formated_cols.append('projid')
    taxa_og_cols.append('projid')

    # Full data/database primary keys merge
    rawmerge = pd.merge(
        rawtaxa_merge, taxaquery,
        left_on=taxa_og_cols, right_on=taxa_formated_cols,
        how='left')
    rawmerge = rawmerge.drop_duplicates()
    facade._datamerged['raw_main_taxa'] = rawmerge
    rawmerge.to_csv('raw_merged_data_test.csv')
    rawpush = pd.concat([
        rawmerge[['projid','taxaid']], rawtable, timetable,
        covartable], axis=1)
    rawflush = flsh.Flusher(rawpush, 'rawtable', 'taxaid', lter)
    rawflush.go()
    orm.session.commit()

@pytest.fixture
def rawmergedf_all():
    rawdf =pd.read_csv('raw_merged_data_test.csv')
    return rawdf


def test_update_data(
        filehandle, sitehandle, metahandle, updatehandle,
        mainhandle, taxahandle, timehandle,
        obshandle, covarhandle,
        rawmergedf_all):
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
    facade._valueregister['siteid'] = 'SITE'

    facade.input_register(mainhandle)
    maindirector = facade.make_table('maininfo')
    maintable = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(maintable, orm.maintypes)
    
    facade.input_register(taxahandle)
    taxadirector = facade.make_table('taxainfo')
    taxatable = taxadirector._availdf

    facade.input_register(timehandle)
    timetable = tparse.TimeParse(
        facade._data, timehandle.lnedentry).formater()
    facade.input_register(obshandle)
    rawmergedf_all = pd.concat([rawmergedf_all, timetable], axis=1)
    
    facade.input_register(obshandle)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf

    facade.input_register(covarhandle)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covarhandle.lnedentry['columns']).convert_records()

    facade.input_register(updatehandle)
    updaterdirector = facade.make_table('updateinfo')
    updatetable = updaterdirector._availdf

    siteloc = facade._valueregister['siteid']
    projids = list(set(rawmergedf_all['projid'].values.tolist()))
    rawlabel = facade._inputs['rawinfo'].lnedentry
    rawloc = facade._inputs['rawinfo'].checks


    ##### Generating derived data #####

    # Study Start and End year
    # Site Start and End year
    yr_all= []
    for i,item in enumerate(sitelevels):
        yr_list = rawmergedf_all[rawmergedf_all['siteid'] == item][
            'year'].values.tolist()
        yr_list.sort()
        [yr_all.append(x) for x in yr_list]
        updatetable.loc[
            updatetable.siteid == item, 'sitestartyr'] = yr_list[0]
        updatetable.loc[
            updatetable.siteid == item, 'siteendyr'] = yr_list[-1]
        updatetable.loc[
            updatetable.siteid == item, 'totalobs'] = len(yr_list)
        updatetable.loc[
            updatetable.siteid == item, 'siteendyr'] = yr_list[-1]
    yr_all.sort()
    updatetable.loc[:, 'studystartyr'] = yr_all[0]
    updatetable.loc[:, 'studyendyr'] = yr_all[-1]


    # Unique Taxa units    
    taxa_col_list = [
        'sppcode', 'kingdom', 'phylum', 'clss', 'order',
        'family', 'genus', 'species']
    taxa_col_list_y = [x + '_y' for x in taxa_col_list]
    taxa_col_list_y.append('siteid')
    taxauniquedf = rawmergedf_all[taxa_col_list_y].drop_duplicates()
    taxa_site_count = pd.DataFrame(
        {'count': taxauniquedf.groupby(
            'siteid').size()}).reset_index()
    updatetable['uniquetaxaunits'] = taxa_site_count['count']

    # Spt_rep unique levels
    updatetable.loc[:, 'sp_rep1_label'] = siteloc
    updatetable.loc[:, 'sp_rep1_uniquelevels'] = 1
    bool_list = list(rawloc.values())
    
    for i, label in enumerate(rawloc):
        if (bool_list[i] is True) and (
                label in updatetable.columns.values.tolist()):
            updatetable.loc[:, label] = list(rawlabel.values())[i]
            for j, site in enumerate(sitelevels):
                levelcount = []
                uqleveldf = rawmergedf_all[
                    rawmergedf_all[siteloc] == site][
                    list(rawlabel.values())[i]].copy()
                levelcount.append(len(uqleveldf.unique()))

                col = list(
                    rawlabel.keys())[i].replace(
                        't', '') + '_uniquelevels'
                
                updatetable.loc[
                    updatetable.siteid == site, col] = levelcount[0]
        else:
            pass

    updatetable_merge = pd.merge(
        updatetable, rawmergedf_all[['projid', 'siteid']],
        on='siteid', how='outer').drop_duplicates().reset_index(
            drop=True)
    updatetable_merge.drop('siteid', axis=1, inplace=True)

    
    # Creating orms for updating tables: Must be done
    # AFTER COMMITTING SITE AND MAIN TABLE INFORMATION
    mainupdates = {}

    orm.convert_types(updatetable_merge, orm.maintypes)

    print(updatetable_merge)
    for i in range(len(updatetable_merge)):
        mainupdates[i] = orm.session.query(
            orm.Maintable).filter(
                orm.Maintable.projid == updatetable_merge[
                    'projid'].iloc[i]).one()
        orm.session.add(mainupdates[i])


    for i in range(len(updatetable_merge)):
        dbupload = updatetable_merge.loc[
            i, updatetable_merge.columns].to_dict()
        for key in dbupload.items():
            setattr(
                mainupdates[i], key[0], key[1])
            orm.session.add(mainupdates[i])

    orm.session.commit()
