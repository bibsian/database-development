# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/bibsian/Desktop/git/database-development/Views/ui_mainrefactor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(984, 616)
        MainWindow.setBaseSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet(_fromUtf8("QLabel{\n"
"    padding: 3;\n"
"}\n"
"\n"
"QFrame{\n"
"    border-radius: 7;\n"
"}\n"
"\n"
"QTableView{\n"
"    background: white;\n"
"}\n"
"\n"
"\n"
".QLineEdit{\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid black;\n"
"    border-radius: 8px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
".QPushButton {\n"
"    color: black;\n"
"    background: #EEEEEE;\n"
"    border-width: 1px;\n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 7;\n"
"    margin-top: 0px;\n"
"    margin-left: 5px;\n"
"    margin-right:5px;    \n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        self.mdiArea.setEnabled(True)
        self.mdiArea.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.mdiArea.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mdiArea.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.mdiArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.mdiArea.setActivationOrder(QtGui.QMdiArea.CreationOrder)
        self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(False)
        self.mdiArea.setTabsMovable(True)
        self.mdiArea.setObjectName(_fromUtf8("mdiArea"))
        self.subwindow_1 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subwindow_1.sizePolicy().hasHeightForWidth())
        self.subwindow_1.setSizePolicy(sizePolicy)
        self.subwindow_1.setMinimumSize(QtCore.QSize(100, 400))
        self.subwindow_1.setBaseSize(QtCore.QSize(0, 0))
        self.subwindow_1.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.subwindow_1.setObjectName(_fromUtf8("subwindow_1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.subwindow_1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblViewMeta = QtGui.QTableView(self.subwindow_1)
        self.tblViewMeta.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblViewMeta.sizePolicy().hasHeightForWidth())
        self.tblViewMeta.setSizePolicy(sizePolicy)
        self.tblViewMeta.setFrameShape(QtGui.QFrame.Box)
        self.tblViewMeta.setSortingEnabled(False)
        self.tblViewMeta.setObjectName(_fromUtf8("tblViewMeta"))
        self.verticalLayout.addWidget(self.tblViewMeta)
        self.subwindow_2 = QtGui.QWidget()
        self.subwindow_2.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subwindow_2.sizePolicy().hasHeightForWidth())
        self.subwindow_2.setSizePolicy(sizePolicy)
        self.subwindow_2.setMinimumSize(QtCore.QSize(100, 400))
        self.subwindow_2.setBaseSize(QtCore.QSize(0, 0))
        self.subwindow_2.setObjectName(_fromUtf8("subwindow_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.subwindow_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblViewRaw = QtGui.QTableView(self.subwindow_2)
        self.tblViewRaw.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblViewRaw.sizePolicy().hasHeightForWidth())
        self.tblViewRaw.setSizePolicy(sizePolicy)
        self.tblViewRaw.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tblViewRaw.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tblViewRaw.setShowGrid(False)
        self.tblViewRaw.setSortingEnabled(False)
        self.tblViewRaw.setObjectName(_fromUtf8("tblViewRaw"))
        self.verticalLayout_2.addWidget(self.tblViewRaw)
        self.horizontalLayout_2.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 984, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuSplit = QtGui.QMenu(self.menubar)
        self.menuSplit.setObjectName(_fromUtf8("menuSplit"))
        self.menuDatabase = QtGui.QMenu(self.menubar)
        self.menuDatabase.setObjectName(_fromUtf8("menuDatabase"))
        MainWindow.setMenuBar(self.menubar)
        self.actionStart_Session = QtGui.QAction(MainWindow)
        self.actionStart_Session.setObjectName(_fromUtf8("actionStart_Session"))
        self.actionEnd_Session = QtGui.QAction(MainWindow)
        self.actionEnd_Session.setObjectName(_fromUtf8("actionEnd_Session"))
        self.actionLoad_File = QtGui.QAction(MainWindow)
        self.actionLoad_File.setObjectName(_fromUtf8("actionLoad_File"))
        self.actionSiteTable = QtGui.QAction(MainWindow)
        self.actionSiteTable.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.actionSiteTable.setFont(font)
        self.actionSiteTable.setVisible(True)
        self.actionSiteTable.setObjectName(_fromUtf8("actionSiteTable"))
        self.actionMainTable = QtGui.QAction(MainWindow)
        self.actionMainTable.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionMainTable.setFont(font)
        self.actionMainTable.setObjectName(_fromUtf8("actionMainTable"))
        self.actionTaxaTable = QtGui.QAction(MainWindow)
        self.actionTaxaTable.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionTaxaTable.setFont(font)
        self.actionTaxaTable.setObjectName(_fromUtf8("actionTaxaTable"))
        self.actionRawTable = QtGui.QAction(MainWindow)
        self.actionRawTable.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionRawTable.setFont(font)
        self.actionRawTable.setObjectName(_fromUtf8("actionRawTable"))
        self.actionClimateSiteTable = QtGui.QAction(MainWindow)
        self.actionClimateSiteTable.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionClimateSiteTable.setFont(font)
        self.actionClimateSiteTable.setObjectName(_fromUtf8("actionClimateSiteTable"))
        self.actionClimateRawTable = QtGui.QAction(MainWindow)
        self.actionClimateRawTable.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.actionClimateRawTable.setFont(font)
        self.actionClimateRawTable.setObjectName(_fromUtf8("actionClimateRawTable"))
        self.actionTimeFormat = QtGui.QAction(MainWindow)
        self.actionTimeFormat.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionTimeFormat.setFont(font)
        self.actionTimeFormat.setVisible(True)
        self.actionTimeFormat.setIconVisibleInMenu(True)
        self.actionTimeFormat.setObjectName(_fromUtf8("actionTimeFormat"))
        self.actionCovariates = QtGui.QAction(MainWindow)
        self.actionCovariates.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionCovariates.setFont(font)
        self.actionCovariates.setObjectName(_fromUtf8("actionCovariates"))
        self.actionCommit = QtGui.QAction(MainWindow)
        self.actionCommit.setObjectName(_fromUtf8("actionCommit"))
        self.actionNot_implemented = QtGui.QAction(MainWindow)
        self.actionNot_implemented.setObjectName(_fromUtf8("actionNot_implemented"))
        self.actionNot_implemented_2 = QtGui.QAction(MainWindow)
        self.actionNot_implemented_2.setObjectName(_fromUtf8("actionNot_implemented_2"))
        self.actionNew_Climate = QtGui.QAction(MainWindow)
        self.actionNew_Climate.setObjectName(_fromUtf8("actionNew_Climate"))
        self.actionEnd_Climate = QtGui.QAction(MainWindow)
        self.actionEnd_Climate.setObjectName(_fromUtf8("actionEnd_Climate"))
        self.actionConvert_Wide_to_Long = QtGui.QAction(MainWindow)
        self.actionConvert_Wide_to_Long.setObjectName(_fromUtf8("actionConvert_Wide_to_Long"))
        self.actionUndo = QtGui.QAction(MainWindow)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionSplit_Column_By = QtGui.QAction(MainWindow)
        self.actionSplit_Column_By.setObjectName(_fromUtf8("actionSplit_Column_By"))
        self.actionReplace = QtGui.QAction(MainWindow)
        self.actionReplace.setObjectName(_fromUtf8("actionReplace"))
        self.actionCombine_Columns = QtGui.QAction(MainWindow)
        self.actionCombine_Columns.setObjectName(_fromUtf8("actionCombine_Columns"))
        self.toolBar.addAction(self.actionSiteTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMainTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTaxaTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTimeFormat)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRawTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCovariates)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClimateSiteTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClimateRawTable)
        self.menuFile.addAction(self.actionStart_Session)
        self.menuFile.addAction(self.actionEnd_Session)
        self.menuFile.addAction(self.actionNew_Climate)
        self.menuFile.addAction(self.actionEnd_Climate)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_File)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionConvert_Wide_to_Long)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionReplace)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCombine_Columns)
        self.menuSplit.addAction(self.actionSplit_Column_By)
        self.menuSplit.addSeparator()
        self.menuDatabase.addAction(self.actionCommit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSplit.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Formatter", None))
        self.subwindow_1.setWindowTitle(_translate("MainWindow", "Metadata Viewer", None))
        self.subwindow_2.setWindowTitle(_translate("MainWindow", "Raw Data Viewer", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Data Cleaner", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuSplit.setTitle(_translate("MainWindow", "Split", None))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database", None))
        self.actionStart_Session.setText(_translate("MainWindow", "New Session...", None))
        self.actionStart_Session.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionEnd_Session.setText(_translate("MainWindow", "End Session...", None))
        self.actionEnd_Session.setShortcut(_translate("MainWindow", "Ctrl+E", None))
        self.actionLoad_File.setText(_translate("MainWindow", "Load File", None))
        self.actionSiteTable.setText(_translate("MainWindow", "Sites", None))
        self.actionMainTable.setText(_translate("MainWindow", "Metadata", None))
        self.actionTaxaTable.setText(_translate("MainWindow", "Taxa", None))
        self.actionRawTable.setText(_translate("MainWindow", "Observations", None))
        self.actionClimateSiteTable.setText(_translate("MainWindow", "Climate Sites", None))
        self.actionClimateRawTable.setText(_translate("MainWindow", "Climate Observations", None))
        self.actionTimeFormat.setText(_translate("MainWindow", "Format Time", None))
        self.actionCovariates.setText(_translate("MainWindow", "Covariates", None))
        self.actionCommit.setText(_translate("MainWindow", "Commit", None))
        self.actionNot_implemented.setText(_translate("MainWindow", "not implemented", None))
        self.actionNot_implemented_2.setText(_translate("MainWindow", "not implemented", None))
        self.actionNew_Climate.setText(_translate("MainWindow", "New Climate...", None))
        self.actionEnd_Climate.setText(_translate("MainWindow", "End Climate...", None))
        self.actionConvert_Wide_to_Long.setText(_translate("MainWindow", "Format Wide to Long", None))
        self.actionConvert_Wide_to_Long.setShortcut(_translate("MainWindow", "Meta+W, Meta+L", None))
        self.actionUndo.setText(_translate("MainWindow", "Undo", None))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z", None))
        self.actionSplit_Column_By.setText(_translate("MainWindow", "Split Column By", None))
        self.actionReplace.setText(_translate("MainWindow", "Replace", None))
        self.actionReplace.setShortcut(_translate("MainWindow", "Meta+R", None))
        self.actionCombine_Columns.setText(_translate("MainWindow", "Combine Columns", None))

