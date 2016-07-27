#!usr/bin/env python
import pytest
from pandas import read_csv, read_sql, DataFrame
from collections import OrderedDict
from itertools import chain
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))

import class_helpers as helps
import datalayer.config as orm
import class_userfacade as face
os.chdir(rootpath)
import class_inputhandler as ini


@pytest.fixture
def UniqueReplace():
    class UniqueReplace(object):
        ''' Class to perform the work of returning unique
        combinations of levels given 'n' number of columns
        '''
        def __init__(self, dataframe, clsinstance):
            self._data = dataframe.copy()
            self.userinput = clsinstance
            self.lookup = list(clsinstance.lnedentry.values())
            self.levels = None
            self.original = None
            self.modified = None

        def get_levels(self):
            '''
            Returns pandas dataframe with unique combination of
            levels
            '''
            try:
                self.levels = self._data[
                    self.lookup].drop_duplicates().sort_values(
                        self.lookup).reset_index()
                return self.levels
            except Exception as e:
                print(str(e))
                raise LookupError('Invalid column names')

        def replace_levels(
                self, modifiedlevelname, allotherlevels=None):
            '''
            Takes a modified list of factor level labels and converts
            the original labels in the dataframe into
            the modified labels.
            '''
            try:
                assert len(self.lookup) == 1
            except Exception as e:
                print(str(e))
                raise AssertionError(
                    'To replace values input only one column' +
                    ' name.')

            self.modified = modifiedlevelname
            self.original = self._data[self.lookup].drop_duplicates()
            og_list = self.original[self.lookup].values.tolist()
            if any(isinstance(i, list) for i in og_list):
                og_list = list(chain.from_iterable(og_list))
            else:
                pass

            level_name_changed_from = [
                x for x in og_list if x not in allotherlevels]
            print(level_name_changed_from, self.modified)

            try:
                assert (
                    len(self.modified) == len(level_name_changed_from))


                self._data = self._data.replace(
                    {self.lookup[0]: {
                        level_name_changed_from[0]: self.modified[0]}},
                )
                return self._data

            except Exception as e:
                print(str(e))
                raise AttributeError('Too many levels to replace')
            return self._data

        def replace_values(self):
            '''
            takes a list of values to change
            '''
            
            try:
                if helps.check_int(
                        self.userinput.lnedentry['from']) is True:
                
                    modified = self._data.replace(
                        int(self.userinput.lnedentry['from']),
                        self.userinput.lnedentry['to'])

                    return modified

                else:
                    pass

            except Exception as e:
                print(str(e))
                raise LookupError('InputHandler key error')

            finally:
                modified = self._data.replace(
                    self.userinput.lnedentry['from'],
                    self.userinput.lnedentry['to'])

                return modified
                    
    return UniqueReplace


@pytest.fixture
def user_data():
    data = read_csv('Datasets_manual_test/SCI_Fish_All_Years.csv')
    return data


@pytest.fixture
def site_dialog_data():
    data = read_csv('Datasets_manual_test/raw_data_test_dialogsite.csv')
    return data


@pytest.fixture
def df():
    data = read_csv('Datasets_manual_test/raw_data_test.csv')
    return data


@pytest.fixture
def user_input_single():
    lned = {'siteid': 'SITE'}
    user_input = ini.InputHandler(name='sitetable', lnedentry=lned)
    return user_input

@pytest.fixture
def filehandle():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename='Datasets_manual_test/raw_data_test_dialogsite.csv')

    return fileinput

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
def sitehandle():
    lned = {'siteid': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle



def test_user_input_multiple_no_otherlist(user_data, UniqueReplace):
    lned = {'siteid': 'SITE', 'month':'MONTH'}
    user_input = ini.InputHandler(name='sitetable', lnedentry=lned)
    testobject = UniqueReplace(user_data, user_input)
    assert isinstance(testobject, UniqueReplace)
    uniquelist = testobject.get_levels()
    assert isinstance(uniquelist, DataFrame)
    modlist = uniquelist[list(lned.values())].values.tolist()
    assert isinstance(modlist, list)
    assert isinstance(uniquelist, DataFrame)
    with pytest.raises(AssertionError):
        testobject.replace_levels(modlist)

    lned2 = {'siteid': 'site', 'month': 'MONTH'}
    user_input2 = ini.InputHandler(name='sitetable', lnedentry=lned2)
    assert isinstance(user_input2, ini.InputHandler)
    testobject2 = UniqueReplace(user_data, user_input2)
    assert isinstance(testobject2, UniqueReplace)
    with pytest.raises(LookupError):
        testobject2.get_levels()


def test_user_values(user_data, UniqueReplace):
    lned = {'from': '-99999', 'to': 'NULL'}
    user_input = ini.InputHandler(name='replace', lnedentry=lned)
    testob = UniqueReplace(user_data, user_input)
    replaced = testob.replace_values()
    print(replaced)
    assert isinstance(replaced, DataFrame)
    assert ('-99999' not in replaced.values) is True
    assert (int(-99999) not in replaced.values) is True


def test_removed_argument(df, UniqueReplace, user_input_single):
    columns_to_compare = ['SITE', 'DEPTH', 'SP_CODE']
    og_subset = df[columns_to_compare]

    og_levels = og_subset['SITE'].drop_duplicates().values.tolist()
    og_levels.sort()
    og_list = []
    for i in og_levels:
        og_list.append((i, i))

    og_dict = OrderedDict(og_list)
    level_to_change = ['SITEMOD1']

    all_others = [
        x for x in list(og_dict.keys()) if x != 'Site1'
    ]
    all_others.sort()
    all_others = list(set(all_others))

    test = UniqueReplace(df, user_input_single)
    test.get_levels()
    test_replace_subset = test.replace_levels(level_to_change, all_others)
    notequal = (og_subset != test_replace_subset[columns_to_compare])

    print(og_subset)
    print(test_replace_subset)
    print(notequal)
    assert (
        'Site1' not in test_replace_subset['SITE'].values.tolist()) is True

def test_modified_sites(
        metahandle, filehandle, sitehandle,
        UniqueReplace, user_input_single):

    fac = face.Facade()
    fac.input_register(metahandle)
    fac.meta_verify()
    fac.input_register(filehandle)
    fac.load_data()
    fac.input_register(sitehandle)

    verification = fac._data
    
    site_data_director = fac.make_table('siteinfo')
    original_data = site_data_director._availdf.copy()
    original_site_list = original_data[
            'siteid'].values.tolist()
    original_site_list.sort()
    print('original site list: ', original_site_list)

    original_site_ordered = []
    for i in original_site_list:
        original_site_ordered.append((i, i))
    site_dict = OrderedDict(original_site_ordered)

    session = orm.Session()
    # Setting query data, sitelist
    dbquery = session.query(
        orm.Sitetable).order_by(
            orm.Sitetable.siteid).filter(
                    orm.Sitetable.lterid == 'SBC')
    session.close()
    
    database_data = read_sql(
        dbquery.statement, dbquery.session.bind)
    database_site_list = database_data[
        'siteid'].values.tolist()
    print('database_site_list: ', database_site_list)


    # Setting database data, sitelist
    updated_data = original_data[
        ~original_data['siteid'].isin(database_site_list)]
    updated_site_list = updated_data[
        'siteid'].values.tolist()
    print('og updated: :', updated_site_list)
    def updating_data_loop(updated=None):
        site_data_director = fac.make_table('siteinfo')
        
        # Setting original data, site list, and dictionary
        original_data = site_data_director._availdf.copy()
        
        # Setting original data, site list, and dictionary
        original_data = site_data_director._availdf.copy()
        original_site_list = original_data[
                'siteid'].values.tolist()
        original_site_list.sort()
        print('original site list: ', original_site_list)
        
        original_site_ordered = []
        for i in original_site_list:
            original_site_ordered.append((i, i))
        site_dict = OrderedDict(original_site_ordered)

        session = orm.Session()
        # Setting query data, sitelist
        dbquery = session.query(
            orm.Sitetable).order_by(
                orm.Sitetable.siteid).filter(
                        orm.Sitetable.lterid == 'SBC')
        session.close()
        database_data = read_sql(
            dbquery.statement, dbquery.session.bind)
        database_site_list = database_data[
            'siteid'].values.tolist()
        print('database_site_list: ', database_site_list)

        if updated is None:
            # Setting database data, sitelist
            updated_data = original_data[
                ~original_data['siteid'].isin(database_site_list)]
            updated_site_list = updated_data[
                'siteid'].values.tolist()
        else:
            print('Not none')
            updated_data = updated
            updated_site_list = updated_data[
                'siteid'].values.tolist()
        print('updated_site_list: ', updated_site_list)

        user_modified_sites = [
            x for x in list(site_dict.keys())
            if x not in database_site_list and
            x not in updated_site_list
        ]
        print('user_modified_sites: ', user_modified_sites)

        if len(user_modified_sites) == 0:
            pass
        else:
            not_in_db_change_site_to = [
                x for x in updated_site_list
                if x not in list(site_dict.keys()) and
                x not in original_site_list
            ]
            [
                not_in_db_change_site_to.append(x)
                for x in database_site_list
                if x not in list(site_dict.keys()) and
                x not in updated_site_list
            ]    
            print(
                'not_in_db_change_site_to: ', set(not_in_db_change_site_to))

            print(
                'about to enter modified sites list loop: ',
                user_modified_sites)
            for j, site_i in enumerate(
                    list(set(not_in_db_change_site_to))):
                sites_not_updated = [
                    x for x in list(site_dict.keys())
                    if x not in user_modified_sites
                ]
                print('site_i, not update: ', site_i, sites_not_updated)
                fac._data = fac.replace_levels(
                    'siteinfo', [site_i], sites_not_updated)
        
        print('inside loop (facade): ', fac._data)
        return updated_data.copy()

    # Should be no change because the modification was
    # in the database
    
    # Using function defined above to
    # simulate the 'replace_levels' functiong
    # in the facade class
    updated_data = updated_data.replace(
        {'siteid': {'Site4': 'SITEMOD4'}})
    print('update_data post update: ', updated_data)
    nextupdate = updating_data_loop(updated_data)
    print('update_data_loop (original): ', nextupdate)
    print('updated_data_loop (facade): ', fac._data)

    # Verifying site level is modified
    checklist1 = fac._data['SITE']
    assert ('Site3' not in checklist1) is True
    # Verifying adjacent column entries
    verifylist_count = verification['COUNT'].values.tolist()
    checklist_count = verification['COUNT'].values.tolist()
    assert (verifylist_count == checklist_count) is True

    # Using function defined above to
    # simulate the 'replace_levels' function
    # as would be used when the update method is called
    # (see test_dialogsite.py)
    updated_data = updated_data.replace(
        {'siteid': {'Site5': 'SITEMOD5'}})
    print('update_data post update2: ', updated_data)

    nextupdate2 = updating_data_loop(updated_data)
    print('update_data_loop2 (original): ', nextupdate2)
    print('updated_data_loop2 (facade): ', fac._data)

    # Verifying site levels modified (previous call to
    # function and current call)
    checklist2 = fac._data['SITE']
    assert ('Site4' and 'Site5' not in checklist2) is True
    # Verifying adjacent column entries
    verifylist_depth = verification['DEPTH'].values.tolist()
    checklist_depth = verification['DEPTH'].values.tolist()
    assert (verifylist_depth == checklist_depth) is True

    # Using function defined above to
    # simulate the 'replace_levels' function
    # as would be used when the update method is called
    # (see test_dialogsite.py)
    updated_data = updated_data.replace(
        {'siteid': {'Site7': 'SITEMOD7'}})
    print('update_data post update3: ', updated_data)

    nextupdate3 = updating_data_loop(updated_data)
    print('update_data_loop3 (original): ', nextupdate3)
    print('updated_data_loop3 (facade): ', fac._data)

    # Verifying site levels modified (previous call to
    # function and current call)
    checklist3 = fac._data['SITE']
    assert ('Site4' and'Site5' and 'Site7' not in checklist3) is True
    # Verifying adjacent column entries
    verifylist_spcode = verification['SP_CODE'].values.tolist()
    checklist_spcode = verification['SP_CODE'].values.tolist()
    assert (verifylist_spcode == checklist_spcode) is True
