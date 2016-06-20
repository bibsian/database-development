from PyQt4 import QtGui
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import class_inputhandler as ini
import class_timeparse as tmpa
import class_modelviewpandas as view
import ui_dialog_time as uitime
import ui_logic_preview as tprev


class TimeDialog(QtGui.QDialog, uitime.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.facade = None

        # Place holders for user inputs
        self.timelned = {}
        # Place holder: Data Model/ Data model view
        self.timemodel = None
        self.viewEdit = view.PandasTableModelEdit
        # Placeholders: Data tables
        self.timetable = None
        # Placeholder for maindata Orms
        self.timeorms = {}
        # Actions
        self.btnPreview.clicked.connect(self.submit_change)
        self.btnSaveClose.clicked.connect(self.submit_change)
        self.btnCancel.clicked.connect(self.close)

        # Update boxes/preview box
        self.message = QtGui.QMessageBox
        self.error = QtGui.QErrorMessage()
        self.preview = tprev.TablePreview()

    def submit_change(self):
        sender = self.sender()
        self.timelned = {
            'dayname': self.lnedDay.text(),
            'dayform': self.cboxDay.currentText(),
            'monthname': self.lnedMonth.text(),
            'monthform': self.cboxMonth.currentText(),
            'yearname': self.lnedYear.text(),
            'yearform': self.cboxYear.currentText(),
            'jd': self.ckJulian,
            'mspell': self.ckMonthSpelling
        }

        self.timeini = ini.InputHandler(
            name='timeinfo', tablename='timetable',
            lnedentry=self.timelned)
        self.facade.input_register(self.timeini)
        self.timetable = tmpa.TimeParse(
            self.facade._data, self.timelned)

        try:
            timeview =self.timetable.formater().copy()
        except Exception as e:
            print(str(e))
            raise ValueError(
                'Could not format dates - ' +
                'Check entries for errors')

        if sender is self.btnPreview:
            timeview = timeview.applymap(str)
            self.timemodel = self.viewEdit(timeview)
            self.preview.tabviewPreview.setModel(self.timemodel)
            self.preview.show()
            print(timeview)

        elif sender is self.btnSaveClose:
            self.facade._dbtabledict['timetable'] = (
                timeview.applymap(int))
            self.close()
