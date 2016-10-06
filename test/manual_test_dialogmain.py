#!/usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
from pandas import read_sql
from collections import OrderedDict, namedtuple
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from Views import ui_mainrefactor as mw
from Views import ui_dialog_main as dmainw
from poplerGUI import ui_logic_session as logicsess
from poplerGUI import ui_logic_site as logicsite
from poplerGUI import class_inputhandler as ini
from poplerGUI import class_modelviewpandas as view
from poplerGUI import ui_logic_preview as tprev
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_helpers as hlp

@pytest.fixture
def MainWindow():
    class MainDialog(QtGui.QDialog, dmainw.Ui_Dialog):

        studytype = namedtuple('studytype', 'checked entry unit')
        derived = namedtuple('derived', 'checked entry unit')
        treatments = namedtuple('treatments', 'checked entry unit')
        contacts = namedtuple('contacts', 'checked entry unit')
        community = namedtuple('community', 'checked entry unit')
        sampfreq = namedtuple('sampfreq', 'checked entry unit')
        dtype = namedtuple('dtype', 'checked entry unit')
        structure = namedtuple('structure', 'checked entry unit')
        ext = namedtuple('spatial_ext', 'checked entry unit')

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

            self.facade = None
            self.mainini = None
            # Place holder: Data Model/ Data model view
            self.mainmodel = None
            self.viewEdit = view.PandasTableModelEdit
            self.form_entries = None
            
            # Placeholders: Data tables
            self.project_table = None

            # Placeholder: Director (table builder), log
            self.maindirector = None
            self._log = None

            # Actions
            self.btnPreview.clicked.connect(self.submit_change)
            self.btnSaveClose.clicked.connect(self.submit_change)
            self.btnCancel.clicked.connect(self.close)

            self.preview = tprev.TablePreview()
            self.message = QtGui.QMessageBox
            self.error = QtGui.QErrorMessage()



        
        def submit_change(self):
            '''
            Method to get data from user form and make project table
            to upload
            '''
            sender = self.sender()
            self.form_entries = OrderedDict((
                ('samplingunits', self.dtype(
                    self.lnedDatatypeunits.text() != '',
                    self.lnedDatatypeunits.text(),
                    None
                )),
                ('datatype', self.dtype(
                    self.cboxDatatype.currentText() != '',
                    self.cboxDatatype.currentText(),
                    None
                )),
                ('structured_type_1', self.structure(
                    self.ckStructure1.isChecked(),
                    self.lnedStructure1.text(),
                    self.lnedStructureunits1.text()
                )),
                ('structured_type_2', self.structure(
                    self.ckStructure2.isChecked(),
                    self.lnedStructure2.text(),
                    self.lnedStructureunits2.text()
                )),
                ('structured_type_3', self.structure(
                    self.ckStructure3.isChecked(),
                    self.lnedStructure3.text(),
                    self.lnedStructureunits3.text()
                )),
                ('samplefreq', self.sampfreq(
                    self.cboxSamplingfrequency.currentText() != 'NULL',
                    self.cboxSamplingfrequency.currentText(),
                    None
                )),
                ('studytype', self.studytype(
                    self.cboxStudytype.currentText() != 'NULL',
                    self.cboxStudytype.currentText(),
                    None
                )),
                ('community', self.community(
                    True,
                    (
                        'yes' if
                        self.rbtnCommunityyes.isChecked() is True
                        else 'no'
                    ),
                    None
                )),
                ('spatial_replication_level_1_extent', self.ext(
                    self.ckSpatialextent1.isChecked(),
                    self.lnedSpatialextent1.text(),
                    self.lnedSpatialextentunits1.text()
                )),
                ('spatial_replication_level_2_extent', self.ext(
                    self.ckSpatialextent2.isChecked(),
                    self.lnedSpatialextent2.text(),
                    self.lnedSpatialextentunits2.text()
                )),
                ('spatial_replication_level_3_extent', self.ext(
                    self.ckSpatialextent3.isChecked(),
                    self.lnedSpatialextent3.text(),
                    self.lnedSpatialextentunits3.text()
                )),
                ('spatial_replication_level_4_extent', self.ext(
                    self.ckSpatialextent4.isChecked(),
                    self.lnedSpatialextent4.text(),
                    self.lnedSpatialextentunits4.text()
                )),
                ('spatial_replication_level_5_extent', self.ext(
                    self.ckSpatialextent5.isChecked(),
                    self.lnedSpatialextent5.text(),
                    self.lnedSpatialextentunits5.text()

                )),
                ('treatment_type_1', self.treatments(
                    self.cboxTreatment1.currentText() != 'NULL',
                    self.cboxTreatment1.currentText(),
                    None
                )),
                ('treatment_type_2', self.treatments(
                    self.cboxTreatment2.currentText() != 'NULL',
                    self.cboxTreatment2.currentText(),
                    None
                )),
                ('treatment_type_3', self.treatments(
                    self.cboxTreatment3.currentText() != 'NULL',
                    self.cboxTreatment3.currentText(),
                    None
                )),
                ('derived', self.derived(
                    self.cboxDerived.currentText() != 'NULL',
                    self.cboxDerived.currentText(),
                    None
                )),
                ('authors', self.contacts(
                    self.lnedAuthor.text() != '',
                    self.lnedAuthor.text(),
                    None
                )),
                ('authors_contact', self.contacts(
                    self.lnedContact.text() != '',
                    self.lnedContact.text(),
                    None
                ))
            ))
            
            self.mainini = ini.InputHandler(
                name='maininfo', tablename='project_table',
                lnedentry=self.form_entries
            )

            self.facade.input_register(self.mainini)
            try:
                self.maindirector = self.facade.make_table('maininfo')
            except Exception as e:
                print(str(e))
                self.error.showMessage(str(e))
            self.facade.create_log_record('project_table')
            self._log = self.facade._tablelog['project_table']
            self.project_table = self.maindirector._availdf.copy()


            if sender is self.btnPreview:
                self.mainmodel = self.viewEdit(self.project_table)
                self.preview.tabviewPreview.setModel(self.mainmodel)
                self.preview.show()
                return
            else:
                pass
            self.facade.push_tables['project_table'] = self.project_table
            self._log.debug(
                'project_table mod: ' +
                ' '.join(self.project_table.columns.values.tolist()))

            orm.convert_types(self.project_table, orm.project_types)
            hlp.write_column_to_log(
                self.form_entries, self._log, 'project_table')
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

            # ------- SITE DIALOG CONSTRUCTOR ARGS ----- #
            self.facade = face.Facade()
            self.dsite = logicsite.SiteDialog()
            # Actions
            self.actionSiteTable.triggered.connect(self.site_display)
            # Custom Signals
            self.dsite.site_unlocks.connect(self.site_complete_enable)

            # ------ SESSION DIALOG CONSTRUCTOR ARGS ----- #
            # Dialog boxes for user feedback
            self.dsession = logicsess.SessionDialog()
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox
            # Custom signals
            self.dsession.raw_data_model.connect(
                self.update_data_model)

            # actions
            self.actionStart_Session.triggered.connect(
                self.session_display)

            # ------- MAIN DIALOG CONSTRUCTOR ARGS ------- #
            self.dmain = MainDialog()
            self.actionMainTable.triggered.connect(self.main_display)
            

        def main_display(self):
            ''' Displays main dialog box'''
            self.dmain.facade = self.facade
            self.dmain.show()
        
        def update_data_model(self):
            newdatamodel = view.PandasTableModel(self.facade._data)
            self.tblViewRaw.setModel(newdatamodel)

        def session_display(self):
            ''' Displays the Site Dialog box'''
            self.dsession.show()
            self.dsession.facade = self.facade
        # ------- END SESSION DIAGLOG CODE --------#

        # -------- START SITE DIALOG CODE ---------#

        @QtCore.pyqtSlot(object)
        def site_complete_enable(self):
            ''' 
            Method to enable actions for display dialog 
            boxes that corresond to different database tables
            '''
            self.actionMainTable.setEnabled(True)
            self.actionTaxaTable.setEnabled(True)
            self.actionTimeFormat.setEnabled(True)
            self.actionRawTable.setEnabled(True)
            self.actionCovariates.setEnabled(True)
            self.update_data_model()

        def site_display(self):
            ''' Displays the Site Dialog box'''
            self.dsite.show()
            self.dsite.facade = self.facade

        # --------- END SITE DIALOG CODE ----------#

    return UiMainWindow()

        # ----------- START SESSION DIALOG CODE ----- #
def test_dialog_site(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)

    qtbot.stopForInteraction()
