\#!usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore, QtTest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_mainrefactor as mw
import ui_dialog_session as ds


@pytest.fixture
def interface():

    class SessionDialog(QtGui.QDialog, ds.Ui_DialogSession):
        identifyer = 'Session'

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            # Attributes
            self.records = [
                ('GlobalID', self.lineEditGlobalid),
                ('MetaURL', self.lineEditMetaURL),
                ('LTERloc', self.cboxLTERloc)]
            
            self.__metaentry = {}
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox()
            
            # Signals/Slots
            self.btnSubmitMeta.clicked.connect(self.extract_entry)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

        def extract_entry(self):
            sender = self.sender()
            for i,item in enumerate(self.records):
                if i < (len(self.records)-1):
                    self.__metaentry[item[0]] = item[1].text()
                else:
                    self.__metaentry[item[0]]= item[1].currentText()
            print(self.__metaentry)
            try:
                assert ('' not in self.__metaentry.values()) is True
            except:
                self.error.showMessage(
                    'All required informatoin is not present.')
                raise AssertionError('All info not present')

            # Send signal to Facade and run entires through
            # verifier class. Then display entries confirmed.
            self.message.about(self, 'Update','Entries Confirmed')

        def pass_entry(self):
            pass


    class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            # attributes
            self.setupUi(self)
            self.sessionD = SessionDialog()

            # actions
            self.actionStart_Session.triggered.connect(
                self.session_manager)

        def session_manager(self):
            '''
            Methods to display the Session dialog box and initiate
            functionality
            '''
            self.sessionD.show()
            


    test = UiMainWindow()
    return test


def test_show_raise_error(qtbot, interface):
    '''
    test to check widgets show
    '''
    interface.show()
    qtbot.addWidget(interface)
    qtbot.keyClick(interface, "n", QtCore.Qt.ControlModifier, 200)
    
    sessionbox = interface.sessionD
    submitbtn = sessionbox.btnSubmitMeta

    qtbot.addWidget(sessionbox)
    qtbot.addWidget(submitbtn)
    
    qtbot.mouseClick(submitbtn, QtCore.Qt.LeftButton)
