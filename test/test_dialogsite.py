#!usr/bin/env python
import pytest
import pytestqt
import pandas as pd
from PyQt4 import QtGui, QtCore, QtWebKit
import itertools
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import class_userfacade as face
import class_inputhandler as ini
import ui_dialog_site as dsite
import ui_mainrefactor as mw
import class_modelviewpandas as view



@pytest.fixture
def MainWindow():
    class SiteDialog(QtGui.QDialog, dsite.Ui_Dialog):

        changed_data = QtCore.pyqtSignal(object)
        site_unlocks = QtCore.pyqtSignal(object)
        
        def __init__(self,  parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.sitelistdata = None
            self.sitelistmodel = None
            self.sitemodlist = None
            self.siteini = None
            self.facade = None
            
            # Status Message
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox

            # Signals and slots
            self.btnSiteID.clicked.connect(self.site_handler)
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnSkip.clicked.connect(self.close)

        def site_handler(self):
            ''' 
            Method to take user input from line edit and
            wrap it with a InputHandler. Then send 
            the wrapped object to the Main Window.
            '''
            lned = {'siteid': self.lnedSiteID.text().strip()}

            self.siteini = ini.InputHandler(
                name='siteinfo', tablename='sitetable', lnedentry=lned)

            try:

                self.facade.input_register(self.siteini)
                self.site_manager()
                
            except Exception as e:
                print(str(e))
                self.error.showMessage(str(e))
                raise LookupError('Input not registered')


            self.message.about(self, 'Status', 'Site Column Recorded')

        def site_manager(self):
            '''
            Receives an InputHandler object from the Site Dialog
            box. Registers the object to the Facade class
            and initiates a method to do work on that user input.
            '''
            try:
                self.sitelistmodel = view.PandasTableModelEdit(
                    self.facade.view_unique('siteinfo'))
                self.listviewSiteLabels.setModel(
                    self.sitelistmodel)
                print('exit site manager')
                
            except Exception as e:
                print(str(e))
                self.error.showMessage(str(e))
                raise AttributeError('Column name not valid')

        def submit_change(self):
            '''
            Method to change factor levels when modified by users
            '''
            npmodlist = self.sitelistmodel.data(
                None, QtCore.Qt.UserRole)
            self.sitemodlist = list(
                itertools.chain.from_iterable(npmodlist))
            try:
                self.facade.replace_levels(
                    'siteinfo', self.sitemodlist)
                print('exit submit_change')
            except Exception as e:
                print(str(e))
                self.error.showMessage('Could not modified levels')
                raise ValueError
            finally:
                self.changed_data.emit(self.facade._data)
                self.site_unlocks.emit()
                self.site_manager()
                self.close()


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
            self.facade = face.Facade()
            self.dsite = SiteDialog()
            self.facade._data = pd.read_csv('SCI_Fish_All_Years_Short.csv')
            datamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(datamodel)

            # Actions
            self.actionSiteTable.triggered.connect(self.site_display)

            # Custom Signals
            self.dsite.changed_data.connect(self.update_data_model)
        @QtCore.pyqtSlot(object)
        def update_data_model(self, dataobject):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)
            self.dsite.facade = self.facade
            print('exit update_data_model')
            
        def site_display(self):
            ''' Displays the Site Dialog box'''
            self.dsite.show()
            self.dsite.facade = self.facade



    return UiMainWindow()

    
def test_class(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()

