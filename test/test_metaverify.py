#! /usr/bin/env python
import pytest
from pandas import read_csv
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
os.chdir(rootpath)
import class_inputhandler as ini


class MetaVerifier(object):
    """
    This is going to be a Singleton pattern i.e. 
    only one instance of this class will be created 
    in the whole program.

    Keyword Arguments
    -----------------
    idnumber: integer
    lterloc: string
    metaurl: string
    """

    if sys.platform == "darwin":
        metapath = (
        "/Users/bibsian/Dropbox/database-development/test/Datasets_manual_test" +
        "/meta_file_test.csv")

    elif sys.platform == "win32":
        metapath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\Datasets_manual_test\\meta_file_test.csv")

    _meta = read_csv(metapath, encoding='iso-8859-11')

    def __init__(self,  inputclsinstance):
        self.idnumber = int(inputclsinstance.lnedentry['globalid'])
        self.lterloc = inputclsinstance.lnedentry['lter']
        self.metaurl = inputclsinstance.lnedentry['metaurl']


    def verify_entries(self):
        '''
        This method is going to be used to verify
        the user input into the program. Ensuring that
        all the parameter supplied match a given record
        in the metadata dataframe.
        '''
        if None in (self.idnumber, self.lterloc, self.metaurl):
            raise AttributeError(
                'Not all attributes have been set. Please enter' +
                'the globalid, lter location, and metadata url.')
        else:
            try:
                assert self.idnumber > 0
            except:
                raise AttributeError(
                    'Plese enter the globalid number.')

            try:

                assert (self._meta.loc[
                    self._meta['global_id']== self.idnumber][
                            'global_id'] == 
                        self.idnumber).bool() is True

                assert (self._meta.loc[
                    self._meta['global_id']== self.idnumber][
                        'lter'] ==
                        self.lterloc).bool() is True

                assert (self._meta.loc[
                    self._meta['global_id']== self.idnumber][
                            'site_metadata']
                        == self.metaurl).bool() is True

                return True
            except:
                raise LookupError(
                    "The verification attributes have not been set" +
                    " correctly. Please check values for the " +
                    "global_id, LTER location, and metadata url.")

@pytest.fixture
def metahandle():
    lentry = {'globalid': 2, 'metaurl': 'https://test', 'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def metahandlecorrect():
    lentry = {
        'globalid': '2',

        'metaurl':
        'http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.17',

        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput


def test_init_nodata(metahandle):
    t = MetaVerifier(metahandle)

    assert (t.idnumber == 2) is True
    assert (t.metaurl == 'https://test') is True
    assert (t.lterloc == 'SBC') is True

    with pytest.raises(LookupError):
        t.verify_entries()


def test_correct_userinput(metahandlecorrect):
    verify = MetaVerifier(metahandlecorrect)
    verify.verify_entries()

