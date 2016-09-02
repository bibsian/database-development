#! /usr/bin/env python
import pytest
from poplerGUI.logiclayer import class_userfacade as face

@pytest.fixture
def Facade_push():
    class Facade_push(face.Facade):
        def __init__(self):
            face.Facade.__init__(self)

    return Facade_push

def test(Facade_push):
    facade_object = Facade_push()
