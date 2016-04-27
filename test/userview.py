#!usr/bin/env python
from PyQt4 import QtGui, QtCore, QtWebKit
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import ui_mainrefactor as mw
import ui_dialog_session as ds
import commanders as cmd
import userfacade as face
import inputhandler as ini


class SessionDialog(QtGui.QDialog, ds.Ui_DialogSession):
    '''
    Dialog pop that prompts the user to inpute
    unique metadata relating to the file that
    will be loaded.
    
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Attributes
        self.records = [
            ('globalid', self.lineEditGlobalid),
            ('metaurl', self.lineEditMetaURL),
            ('lter', self.cboxLTERloc)]

        self._metalned = {}
        
        # Dialog boxes for user feedback
        self.error = QtGui.QErrorMessage()
        self.message = QtGui.QMessageBox()

        # Signals/Slots
        self.btnSubmitMeta.clicked.connect(self.extract_entry)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def extract_entry(self):
        '''
        Method to extract the user input from the
        line edit boxes.
        '''

        for i, item in enumerate(self.records):
            if i < (len(self.records)-1):
                self._metalned[item[0]] = item[1].text()
            else:
                self._metalned[item[0]] = item[1].currentText()

        try:
            assert ('' not in self._metalned.values()) is True
        except:
            self.error.showMessage(
                'All informatoin is not present.')
            raise AssertionError('All info not present')
        
        # Send signal to Facade and run entires through
        # verifier class. Then display entries confirmed.
        self.message.about(self, 'Update', 'Entries Confirmed')

    def pass_entry(self):
        '''
        Method to return the dictionary that contains the
        metadata information
        '''

        try:
            assert ('' not in self._metalned.values()) is True
        except:
            raise AssertionError('Cant pass metalned; not complete')

        return self.metalned


class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
    '''
    The main window class will serve to gather all informatoin
    from Dialog boxes, actions, and instantiate classes
    that are required to perform the necessary lower level logic
    (i.e. implement a Facade, Commander, MetaVerifier, etc.
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        # attributes
        self.setupUi(self)
        self.sessionD = SessionDialog()
        self.face = face.Facade()


        # actions
        self.actionStart_Session.triggered.connect(
            self.session_manager)

    def session_manager(self):
        '''
        Methods to display the Session dialog box and initiate
        functionality
        '''
        self.sessionD.show()
        

