#!usr/bin/env python
import pytest
import pandas as pd
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import class_inputhandler as ini
import class_helpers as helps

@pytest.fixture
def UniqueReplace():
    class UniqueReplace(object):
        ''' Class to perform the work of returning unique
        combinations of levels given 'n' number of columns
        '''
        def __init__(self, dataframe, clsinstance):
            self._data = pd.DataFrame(dataframe)
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
                        self.lookup).reset_index(drop=True)
                return self.levels
            except Exception as e:
                print(str(e))
                raise LookupError('Invalid column names')

        def replace_levels(self, usermodifiedlist):
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
                    'To replace values to must input only one column' +
                    ' name.')

            if self.levels is not None:
                self.original = self.levels[self.lookup].values.tolist()
                self.modified = usermodifiedlist
                tochange = [
                    [x, y] for x, y in zip(
                        self.original, self.modified) if x != y]
                fromlist = []
                tolist = []
                for i,item in enumerate(tochange):
                    fromlist.append(item[0])
                    tolist.append(item[1])
                return self._data.replace(fromlist, tolist)

            else:
                raise AssertionError(
                    'Must use get_levels method before replacing' +
                    ' values.')

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
    data = pd.read_csv('SCI_Fish_All_Years.csv')
    return data

@pytest.fixture
def user_input_single():
    lned = {'siteid': 'SITE'}
    user_input = ini.InputHandler(name='sitetable', lnedentry=lned)
    return user_input

def test_class(UniqueReplace, user_data, user_input_single):
    testobject = UniqueReplace(user_data, user_input_single)
    listdf = testobject.get_levels()
    print(listdf)
    assert isinstance(testobject, UniqueReplace)
    assert isinstance(listdf, pd.DataFrame)
    modlist = listdf['SITE'].values.tolist()
    assert isinstance(modlist, list)
    modlist[0] = 'BCI'
    modlist[1] = 'BCII'

    newdf = testobject.replace_levels(modlist)
    assert isinstance(newdf, pd.DataFrame)
    
    newtestobject = UniqueReplace(newdf, user_input_single)
    assert isinstance(newtestobject, UniqueReplace)
    newlistdf = newtestobject.get_levels()
    assert isinstance(newlistdf.values.tolist(), list)
    assert 'BCI' in newlistdf['SITE'].values.tolist()
    assert 'BCII' in newlistdf['SITE'].values.tolist()
    assert 'BCI' not in listdf['SITE'].values.tolist()

def test_user_input_multiple(user_data, UniqueReplace):
    lned = {'siteid': 'SITE', 'month':'MONTH'}
    user_input = ini.InputHandler(name='sitetable', lnedentry=lned)
    testobject = UniqueReplace(user_data, user_input)
    assert isinstance(testobject, UniqueReplace)
    uniquelist = testobject.get_levels()
    assert isinstance(uniquelist, pd.DataFrame)
    modlist = uniquelist[list(lned.values())].values.tolist()
    assert isinstance(modlist, list)
    
    assert isinstance(uniquelist, pd.DataFrame)
    with pytest.raises(AssertionError):
        testobject.replace_levels(modlist)

    lned2 = {'siteid': 'site', 'month':'MONTH'}
    user_input2 = ini.InputHandler(name='sitetable', lnedentry=lned2)
    assert isinstance(user_input2, ini.InputHandler)
    testobject2 = UniqueReplace(user_data, user_input2)
    assert isinstance(testobject2, UniqueReplace)
    with pytest.raises(LookupError):
        testobject2.get_levels()

def test_user_values(user_data, UniqueReplace):
    lned = {'from': '-99999', 'to':'NULL'}
    user_input = ini.InputHandler(name='replace', lnedentry=lned)
    testob = UniqueReplace(user_data, user_input)    
    replaced = testob.replace_values()
    print(replaced)
    assert isinstance(replaced, pd.DataFrame)
    assert ('-99999' not in replaced.values) is True
    assert (int(-99999) not in replaced.values) is True
    
