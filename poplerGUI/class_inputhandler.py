
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
        self.verify = verify
        self.session = session
        self.filename = filename
        self.timedata = timedata
        self.covdata = covdata
        self.foreignmergeddata = foreignmergeddata
