#!/usr/bin/env python
import pytest
import re
import decimal as dc
import numbers as nm


class Location(object):
    '''
    This class is going to take the user input regarding where
    in the raw data is the information that we want for
    format with our database schema.

    Key word arguments
    ------------------
    checkbox: This will be a list of checkboxes within the GUI
    indicating whether or not data is available

    lnedit: This will be a list of line edit entries within the GUI
    that record the user input

    newentry: This will be an indiciator to create an entry in
    the raw dataframe if necessary.
    '''
    def __init__(self, **kwargs):
        checkbox = kwargs.setdefault('checkbox', None)
        lnedit = kwargs.setdefault('lnedit', None)
        newentry = kwargs.setdefault('newentry', None)
        typelist = kwargs.setdefault('typelist', None)

        if checkbox is not None:
            assert type(kwargs['checkbox']) is list
            self.checkbox = checkbox

        if lnedit is not None:
            assert type(kwargs['lnedit']) is list
            self.lnedit = kwargs['lnedit']

        if newentry is not None:
            self.newentry = str(newentry)

        if typelist is not None:
            assert type(kwargs['typelist']) is list
            self.numerictypes = [
                x is int or x is float for x in typelist]

    def re_lned_to_list(self):
        '''
        This is a method that will take a list of strings
        (that are user entries), and convert every element in the
        list from a string to a list with regular expressions.

        Example: entries from the user will be of the form
        ['entryone, entrytwo ,entrythree'] and we want to convert
        it to ['entryone', 'entrytwo', 'entrythree']
        '''
        self._lneditlist = [
            re.sub(',\s{1,}', " ", x.rstrip()).split()
            for x in self.lnedit if x is not None]

        assert type(self._lneditlist) == list

        return self._lneditlist

    def re_lned_to_numeric(self):
        pass

    
@pytest.fixture
def lnedlist():
    return [
        ['AQUE', 'AHND', 'BULL', 'SCDI', 'SCDIdupe'],
        ['100', '100', '100', '200', '300'],
        [None]]


@pytest.fixture
def lnedentry():
    return [
        'AQUE, AHND, BULL, SCDI, SCDIdupe',
        '100, 100, 100, 200, 300',
        None]


@pytest.fixture
def typelist():
    return [str, float, None]


def test_init(lnedentry, lnedlist):
    test = Location(lnedit=lnedentry)
    print(lnedlist)
    print(lnedentry)
    print(test.lnedit)
    print(test.re_lned_to_list())
    assert all(
        [x == y for x,y in zip(test.re_lned_to_list(),lnedlist)
        if y is not None])


