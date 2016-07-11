#!usr/bin/env python
import pytest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))


class InputHandler(object):
    '''
    Interface for handling all user input.

    lnedentry: Columns from dataframe
    checks: Indicates presence absence of data values
    rbtns: Indicates presence absence of data values
    verify: Indicates whether input should be verified
    session: Indicates session creation
    filename: Indicates file to load into program
    '''
    def __init__(
            self, name=None, tablename=None, lnedentry={},
            checks={}, rbtns={}, cbox={}, verify=False, session=False,
            filename=None, timedata=None, covdata=None,
            foreignmergeddata=None):
        self.name = name
        self.tablename = tablename
        self.lnedentry = lnedentry
        self.checks = checks
        self.cboxs = cbox
        self.rbtns = rbtns
        self.verifty = verify
        self.session = session
        self.filename = filename
        self.timedata = timedata
        self.covdata = covdata
        self.foreignmergeddata = foreignmergeddata


@pytest.fixture
def rbtn():
    rbtn = {'.csv': True, '.txt': False, '.xlsx': False}
    return rbtn

def test_entries(rbtn):
    userinput = InputHandler(
        name='fileoptions', rbtns=rbtn,
        session=True, filename='DataRawTestFile.csv')
    assert isinstance(userinput, InputHandler)
    print(userinput.name)
