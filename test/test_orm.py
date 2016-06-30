import pytest
import pandas as pd
from sys import platform as _platform
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import class_helpers as hlp
import config as orm

@pytest.fixture
def metadf():
    if _platform == "darwin":
        metapath = (
            "/Users/bibsian/Dropbox/database-development/data" +
            "/meta_file_test.csv")            
    elif _platform == "win32":
        #=======================#
        # Paths to data and conversion of files to dataframe
        #=======================#
        metapath = (
            "C:\\Users\MillerLab\\Dropbox\\database-development" +
            "\\data\\meta_file_test.csv")
    metadf = pd.read_csv(metapath, encoding="iso-8859-11")
    return metadf

@pytest.fixture
def dbcolumns():
    dblist = [
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
        'authors', 'authors_contact', 'metalink', 'knbid']
    return dblist

@pytest.fixture
def tablebuild():
    def get_dataframe(
            dataframe, acols, nullcols, dbcol,
            sitelevels):
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
        return concat.reset_index(drop=True)
    return get_dataframe

# TEST ASSUMES sitelevels ARE IN DATABASE ALREADY!!!!!
def test_write(metadf, tablebuild, dbcolumns):
    sitelevels = ['Site1', 'Site2', 'Site3']
    avail = ['all']
    nulldf = ['none']
    tablefull = tablebuild(metadf, avail, nulldf, dbcolumns, sitelevels)
    orm.convert_types(tablefull, orm.maintypes)
    table = tablefull
    print(table.columns)
    print(table)
    print(table['metarecordid'])
    print(table['uniquetaxaunits'])

    mainorms = {}

    for i in range(len(table)):
        mainorms[i] = orm.Maintable(
            siteid=table.loc[i,'siteid'])
        orm.session.add(mainorms[i])

    for i in range(len(table)):
        dbupload = table.loc[
            i,table.columns].to_dict()
        for key in dbupload.items():
            setattr(mainorms[i], key[0], key[1])
    orm.session.commit()

    
    


