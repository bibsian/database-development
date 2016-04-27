import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))



class InputHandler(object):
    '''
    Interface for handling all user input.
    No setters or getters. All accessing will be done throuh
    composition and passing instances of InputHandler.

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
            filename=None):
        self.name = name
        self.tablename = tablename
        self.lnedentry = lnedentry
        self.checks = checks
        self.cboxs = cbox
        self.rbtns = rbtns
        self.verifty = verify
        self.session = session
        self.filename = filename

