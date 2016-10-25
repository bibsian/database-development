#! /usr/bin/env python
import pytest
import pytestqt
from PyQt4 import QtGui, QtCore
from pandas import read_csv
import subprocess
import sys,os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development")
    end ="/"
    
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development" )
    end = "\\"
from Views import ui_mainrefactor as mw
from poplerGUI import ui_logic_session as sesslogic
from poplerGUI import ui_logic_site as sitelogic
from poplerGUI import ui_logic_main as mainlogic
from poplerGUI import ui_logic_taxa as taxalogic
from poplerGUI import ui_logic_time as timelogic
from poplerGUI import ui_logic_obs as rawlogic
from poplerGUI import ui_logic_covar as covarlogic
from poplerGUI import ui_logic_climatesite as climsitelogic
from poplerGUI import ui_logic_widetolong as widetolonglogic
from poplerGUI import ui_logic_splitcolumn as splitcolumnlogic
from poplerGUI import ui_logic_replace as replacelogic
from poplerGUI import ui_logic_cbind as cbindlogic
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI import class_modelviewpandas as view
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer.datalayer.class_filehandles import Memento


@pytest.fixture
def MainWindow():
    class UiMainWindow(QtGui.QMainWindow, mw.Ui_MainWindow):
        '''
        The main window class will serve to manage the display
        of various dialog boxes, the facade class, model-viewer
        tables, and menu actions.
        '''
        def __init__(self, parent=None):
            super().__init__(parent)
            # attributes
            self.setupUi(self)
            self.facade = face.Facade()
            self._log = None
            self.dsite = sitelogic.SiteDialog()
            self.dsession = sesslogic.SessionDialog()
            self.dmain = mainlogic.MainDialog()
            self.dtaxa = taxalogic.TaxaDialog()
            self.dtime = timelogic.TimeDialog()
            self.draw = rawlogic.ObsDialog()
            self.dcovar = covarlogic.CovarDialog()
            self.dclimatesite = climsitelogic.ClimateSite()
            self.dclimatesession = sesslogic.SessionDialog()
            self.dwidetolong = widetolonglogic.WidetoLongDialog()
            self.dsplitcolumn = splitcolumnlogic.SplitColumnDialog()
            self.dreplacevalue = replacelogic.ReplaceValueDialog()
            self.dcbind = cbindlogic.CbindDialog()
            self.data_model = view.PandasTableModelEdit(None)
            self.data_model.log_change.connect(self.write_to_log)
            self.change_count = 0
            
            # Actions
            self.actionUndo.triggered.connect(self.undo_data_mod)
            self.actionCombine_Columns.triggered.connect(
                self.cbind_display)
            self.actionReplace.triggered.connect(
                self.replace_value_display)
            self.actionConvert_Wide_to_Long.triggered.connect(
                self.wide_to_long_display)
            self.actionSplit_Column_By.triggered.connect(
                self.split_column_display)
            self.actionSiteTable.triggered.connect(self.site_display)
            self.actionStart_Session.triggered.connect(
                self.session_display)
            self.actionEnd_Session.triggered.connect(
                self.end_session)
            self.actionMainTable.triggered.connect(self.main_display)
            self.actionTaxaTable.triggered.connect(self.taxa_display)
            self.actionTimeFormat.triggered.connect(self.time_display)
            self.actionRawTable.triggered.connect(self.obs_display)
            self.actionCovariates.triggered.connect(self.covar_display)
            self.actionCommit.triggered.connect(self.commit_data)
            self.actionClimateSiteTable.triggered.connect(
                self.climate_site_display)
            self.actionNew_Climate.triggered.connect(
                self.climate_session_display)

            self.mdiArea.addSubWindow(self.subwindow_2)
            self.mdiArea.addSubWindow(self.subwindow_1)
            
            # Custom Signals
            self.dsite.site_unlocks.connect(self.site_complete_enable)
            self.dwidetolong.update_data.connect(self.update_data_model)
            self.dsplitcolumn.update_data.connect(self.update_data_model)
            self.dreplacevalue.update_data.connect(self.update_data_model)
            self.dcbind.update_data.connect(self.update_data_model)
            self.dclimatesite.climatesite_unlocks.connect(
                self.climate_site_complete_enabled)
            self.dsession.raw_data_model.connect(
                self.update_data_model)
            self.dclimatesession.raw_data_model.connect(
                self.update_data_model)

            # Dialog boxes for user feedback
            self.error = QtGui.QErrorMessage()
            self.message = QtGui.QMessageBox

            metadf = read_csv(
                rootpath + end + 'data' + end +
                'Identified_to_upload.csv', encoding='iso-8859-11')
            metamodel = view.PandasTableModel(
                metadf[
                    [
                        'global_id', 'lter', 'title', 'site_metadata',
                        'temp_int'
                    ]
                ]
            )
            
            self.tblViewMeta.setModel(metamodel)
            self.tblViewMeta.resizeColumnsToContents()
            self.tblViewRaw.horizontalHeader().sectionDoubleClicked.connect(
                self.changeHorizontalHeader)
            self.tblViewRaw.resizeColumnsToContents()

        @staticmethod
        def update_data_view(self):
            self.data_model = view.PandasTableModelEdit(None)
            self.data_model.set_data(self.facade._data)
            self.tblViewRaw.setModel(self.data_model)

        def undo_data_mod(self):
            if self.facade.data_caretaker._statelist:
                self.facade.data_originator.restore_from_memento(
                    self.facade.data_caretaker.restore()
                )
                self.facade._data = self.facade.data_originator._data.copy()
                self.update_data_view(self)
            else:
                self.error.showMessage(
                    'No further undo'
                )

        @QtCore.pyqtSlot(object)
        def update_data_model(self, dataframe_state):
            ''' Updating data model and facade instance with
            other dialog boxes '''
            self.change_count += 1

            new_dataframe_state = Memento(
                self.facade._data.copy(),
                '{}_{}'.format(dataframe_state, self.change_count)
            )
            self.facade.data_caretaker.save(new_dataframe_state)
            self.facade.data_originator.restore_from_memento(
                new_dataframe_state
            )
            self.update_data_view(self)
            # Updating facade instances with dialog boxes
            self.dsite.facade = self.facade
            self.dclimatesite.facade = self.facade

        @QtCore.pyqtSlot(object)
        def write_to_log(self, dict_obj):
            self.facade.create_log_record('changecell')
            self._log = self.facade._tablelog['changecell']
            hlp.write_column_to_log(
                dict_obj, self._log, 'changecell')

        @QtCore.pyqtSlot(object)
        def update_webview(self, url):
            print(url)
            
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
            self.update_data_model('Updating data')

        def changeHorizontalHeader(self, index):
            ''' method to update data model when column headers
            are changed '''
            oldHeader = self.facade._data.iloc[:,index].name
            newHeader, ok = QtGui.QInputDialog.getText(
                self, 'Input', 'New Column Label:')
            if ok:
                self.facade._data.rename(
                    columns={oldHeader:newHeader}, inplace=True)
            self.facade.create_log_record('changecolumn')
            self._log = self.facade._tablelog['changecolumn']
            hlp.write_column_to_log(
                {
                    'column_changes':
                    {
                        oldHeader: newHeader}
                },
                self._log, 'changecolumn'
            )
            self.update_data_model('header_changes')

        def cbind_display(self):
            ''' Displays dialog box to combine columns '''
            self.dcbind.show()
            self.dcbind.facade = self.facade

        def replace_value_display(self):
            ''' Displays dialog box to split a column '''
            self.dreplacevalue.show()
            self.dreplacevalue.facade = self.facade

        def split_column_display(self):
            ''' Displays dialog box to split a column '''
            self.dsplitcolumn.show()
            self.dsplitcolumn.facade = self.facade

        def wide_to_long_display(self):
            ''' Displays dialog box to melt data '''
            self.dwidetolong.show()
            self.dwidetolong.facade = self.facade
            
        def site_display(self):
            ''' Displays the Site Dialog box'''
            self.dsite.show()
            self.dsite.facade = self.facade

        def addsite_display(self):
            ''' Display dialog box for adding site column'''
            self.daddsite.show()
            self.daddsite.facade = self.facade
            
        def session_display(self):
            ''' Displays the Site Dialog box'''
            self.dsession.show()
            self.dsession.facade = self.facade

        def main_display(self):
            ''' Displays main dialog box'''
            self.dmain.facade = self.facade
            self.dmain.show()

        def taxa_display(self):
            ''' Display the Taxa Dialog box'''
            self.dtaxa.facade = self.facade
            self.dtaxa.show()

        def time_display(self):
            ''' Display the Time Dialog box'''
            self.dtime.facade = self.facade
            self.dtime.show()

        def obs_display(self):
            ''' Display the Raw Obs Dialog box'''
            self.draw.facade = self.facade
            self.draw.show()

        def covar_display(self):
            '''Display the Raw Obs Dialog box'''
            self.dcovar.facade = self.facade
            self.dcovar.show()

        def commit_data(self):
            ''' Method to call the upload to database command '''
            commithandle = ini.InputHandler(
                name='updateinfo', tablename='updatetable')
            self.facade.input_register(commithandle)
            try:
                self.facade.push_merged_data()
                self.actionCommit.setEnabled(False)
                self.message.about(
                    self, 'Status', 'Database transaction complete')
            except Exception as e:
                print(str(e))
                self.facade._tablelog['project_table'].debug(str(e))
                self.error.showMessage(
                    'Datbase transaction error: ' + str(e) +
                    '. May need to alter site abbreviations.')
                raise ValueError(str(e))

        # Below are dialog boxes and logic that relate to Climate data
        def climate_site_display(self):
            ''' Displays the Site Dialog box'''
            self.dclimatesite.show()
            self.dclimatesite.facade = self.facade

        @QtCore.pyqtSlot(object)
        def climate_site_complete_enabled(self, datamod2):
            self.actionClimateRawTable.setEnabled(True)
            self.update_data_model()

        def climate_session_display(self):
            ''' Displays the Climate session dialog box'''
            self.dclimatesession.show()
            self.dclimatesession.facade = self.facade
            self.actionSiteTable.setEnabled(False)
            self.actionClimateSiteTable.setEnabled(True)
            metapath = (
    	        str(os.getcwd()) + 
    	        '/Datasets_manual_test/meta_climate_test.csv')
            metadf = read_csv(metapath, encoding='iso-8859-11')
            metamodel = view.PandasTableModel(metadf)
            self.tblViewMeta.setModel(metamodel)

        def end_session(self):
            self.close()
            subprocess.call(
                "python" + " poplerGUI_run_main.py", shell=True)


    return UiMainWindow()


def test_dialog_site(qtbot, MainWindow):
    MainWindow.show()
    qtbot.addWidget(MainWindow)
    qtbot.stopForInteraction()
