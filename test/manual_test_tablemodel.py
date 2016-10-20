from PyQt4 import QtCore, QtGui
import pytest
import pytestqt
import numpy as np
import pandas as pd
import sys
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"
from Views import ui_dialog_table_preview as uiprev



@pytest.fixture
def df():
    return pd.read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'splitcolumn_data_test.csv'
    )

@pytest.fixture
def PandasTableModelEdit():
    class PandasTableModelEdit(QtCore.QAbstractTableModel):
        log_change = QtCore.pyqtSignal(object)
        '''
        This class is an abstract table class from Qt to visualize
        data in a table format and using the pandas dataframe
        as object that supply the data to be visualized.
        To Do: Nothing
        Last edit: Removed the ability to edit the table
        ''' 
        def __init__(self, data, parent=None):
            QtCore.QAbstractTableModel.__init__(self, parent)
            self.__data = np.array(data.values)
            self.__cols = data.columns
            self.r, self.c = np.shape(self.__data)

        def rowCount(self, parent=None):
            return self.r

        def columnCount(self, parent=None):
            return self.c

        def headerData(self, section, orientation, role):            
            if role == QtCore.Qt.DisplayRole:
                if orientation == QtCore.Qt.Horizontal:
                    return self.__cols[section]
                elif orientation == QtCore.Qt.Vertical:
                    return section

        def data(self, index, role):
            if role == QtCore.Qt.UserRole:
                index = None
                return pd.DataFrame(self.__data, columns=self.__cols)
            else:
                pass

            if index.isValid():
                if role == QtCore.Qt.DisplayRole:
                    return self.__data[index.row(), index.column()]

        def flags(self, index):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |\
                QtCore.Qt.ItemIsEditable

        def setData(self, index, value, role=QtCore.Qt.EditRole):
            if role == QtCore.Qt.EditRole:
                og_value = self.__data(index, QtCore.Qt.DisplayRole)
                self.__data[index.row(), index.column()] = value
                self.dataChanged.emit(index, index)
                self.log_change.emit(
                    {'cell_changes':{og_value: value}})
                return True
            return False

        #def removeRows(self, rowstart, rowend, parent=QtCore.QModelIndex()):
        #    self.beginRemoveRows(
        #        QtCore.QModelIndex(), rowstart, rowend+1)
        #    self.__data = np.delete(
        #            self.__data, np.s_[rowstart:rowend+1], axis=0)
        #    self.endRemoveRows()

        def event(self, event):
            if (event.key() == QtCore.Qt.Key_Return):
                print('Presed Enter')
                raise KeyError
            return QtCore.QAbStractTableModel.event(self, event)

    return PandasTableModelEdit

@pytest.fixture
def Preview(df, PandasTableModelEdit):
    class TablePreview(QtGui.QDialog, uiprev.Ui_Dialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.btnCancel.clicked.connect(self.close)

            self.model = PandasTableModelEdit(df)
            self.model.log_change.connect(self.write_to_log)
            self.tabviewPreview.setModel(self.model)

            # Double click header to change column name
            self.tabviewPreview.horizontalHeader().sectionDoubleClicked.connect(
                self.changeHorizontalHeader)
            # Resize column widths to fit words
            self.tabviewPreview.resizeColumnsToContents()

            # Right click on verticalHeader
            #self.tabviewPreview.setContextMenuPolicy(
            #    QtCore.Qt.CustomContextMenu
            #)
            #self.tabviewPreview.customContextMenuRequested.connect(
            #    self.on_context_menu)
            # Context menu for delete action
            #self.popMenu = QtGui.QMenu(self)
            #self.popMenu.addAction(QtGui.QAction('delete', self))
            #self.popMenu.addSeparator()

        #def on_context_menu(self, point):
        #    ''' Method to initiate the deltion of rows'''
        #    # show context menu
        #    self.popMenu.exec_(
        #        self.tabviewPreview.mapToGlobal(point))
        #    indeces = list(
        #        set([x.row() for x in 
        #        self.tabviewPreview.selectedIndexes()]))
        #    self.model.removeRows(indeces[0], indeces[-1])
        # LEFT OFF HERE. Trying to get the delete rows feature working

        @QtCore.pyqtSlot(object)
        def write_to_log(self, change):
            print(change)

        def changeHorizontalHeader(self, index):
            print(index)
            oldHeader = df.iloc[:,index].name
            newHeader, ok = QtGui.QInputDialog.getText(
                self, 'Input', 'New Column Label:')
            if ok:
                df_updated = df.rename(columns={oldHeader:newHeader})
                self.tabviewPreview.setModel(
                    PandasTableModelEdit(df_updated))

            self.write_to_log(
                {'column_change': {oldHeader:newHeader}})

    return TablePreview()
    
def test_dialog_site(qtbot, Preview):
    Preview.show()
    qtbot.addWidget(Preview)
    qtbot.stopForInteraction()
