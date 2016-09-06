\#! /usr/bin/env python
import pytest
from poplerGUI.logiclayer import class_userfacade as face

@pytest.fixture
def Facade_push():
    class Facade_push(face.Facade):
        def __init__(self):
            face.Facade.__init__(self)


    def merge_push_data(self):
        '''
        Method in facade class to check if all data tables
        have been completed by the user (although
        site table can be empty if records are already in the 
        database).
        '''

        for i, item in enumerate(self.push_tables.values()):
            try:
                if list(
                        self.push_tables.keys())[i] == 'study_site_table':
                    pass
                else:
                    assert (item is not None) is True
            except Exception as e:
                print(str(e))
                raise AttributeError(
                    'Not all data tables have been completed. ' +
                    str(e))

        # User created database tables
    return Facade_push

def test(Facade_push):
    facade_object = Facade_push()
