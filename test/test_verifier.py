#!/usr/bin/env python
import pytest
import pandas as pd



class Verifier(pd.DataFrame):
    """
    Gloabal Id is a pandas dataframe that
    contains all the metadata along with user
    supplied key word arguments.

    Keyword Arguments
    -----------------
    idnumber: integer
    lterloc: string
    metaurl: string
    """
    def __init__(self, *args, **kwargs):
        idnumber = kwargs.pop('idnumber', None)
        lterloc = kwargs.pop('lterloc', None)
        metaurl = kwargs.pop('metaurl', None)

        super(Verifier, self).__init__(*args, **kwargs)
        # Giving our added attributes None type or assigning
        # them based on user input
        if idnumber is not None:
            self.idnumber = int(idnumber)
        else:
            self.idnumber = None

        if lterloc is not None:
            self.lterloc = str(lterloc)
        else:
            self.lterloc = None

        if metaurl is not None:
            self.metaurl = str(metaurl)
        else:
            self.metaurl = None
        self.records = None

    @property
    def _constructor(self):
        '''
        Defining the constructor to subclass a pandas
        dataframe.
        '''
        return Verifier

    def get_records(self):
        '''
        This method is going to be used to verify
        the user input into the program. Ensuring that
        all the parameter supplied match a given record
        in the metadata dataframe.
        '''
        if None in (self.idnumber, self.lterloc, self.metaurl):
            return self.records
        else:
            try:
                self.records = self[self['global_id'] == self.idnumber]

                assert self.lterloc == list(self[
                    self['global_id'] == self.idnumber]['lter'])[0]

                assert self.metaurl == list(self[
                    self['global_id'] ==
                    self.idnumber]['site_metadata'])[0]

                return self.records

            except:
                raise LookupError(
                    "The global id attributes have not been set" +
                    " correctly. Please check the dataframe, " +
                    "global_id, LTER location, and metadata url.")


@pytest.fixture
def df():
    import pandas as pd
    metadf = pd.read_csv(
        "DataMetaTestFile.csv", encoding="iso-8859-11")
    return metadf


def test_init_nodata():
    assert Verifier
    test = Verifier(idnumber=1)
    assert test.idnumber == 1
    assert len(test.values) == 0
    assert test.records is None
    assert test._data is not None
    print(test._data)


def test_init_data(df):
    test = Verifier(data=df)
    assert test.idnumber is None
    assert test.lterloc is None
    assert test.metaurl is None
    assert test.records is None


def test_lookup_error(df):
    test = Verifier(data=df)
    test.idnumber = 2
    test.lterloc = 'SBC'
    test.metaurl = 'raise error'
    with pytest.raises(LookupError):
        test.get_records()

    test.metaurl = ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?' +
                    'docid=knb-lter-sbc.17')
    print(test.metaurl)
    print(test.get_records())
