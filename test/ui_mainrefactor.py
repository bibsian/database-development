# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/bibsian/Dropbox/database-development/test/Views/ui_mainrefactor.ui'
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
        MainWindow.resize(1185, 777)
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
"}"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("https://www.lternet.edu/")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayout_3.addWidget(self.webView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1185, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuReplace = QtGui.QMenu(self.menuEdit)
        self.menuReplace.setObjectName(_fromUtf8("menuReplace"))
        self.menuSplit = QtGui.QMenu(self.menubar)
        self.menuSplit.setObjectName(_fromUtf8("menuSplit"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidgetRaw = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetRaw.sizePolicy().hasHeightForWidth())
        self.dockWidgetRaw.setSizePolicy(sizePolicy)
        self.dockWidgetRaw.setBaseSize(QtCore.QSize(500, 500))
        self.dockWidgetRaw.setStyleSheet(_fromUtf8(""))
        self.dockWidgetRaw.setFeatures(QtGui.QDockWidget.DockWidgetFloatable)
        self.dockWidgetRaw.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidgetRaw.setObjectName(_fromUtf8("dockWidgetRaw"))
        self.dockWidgetContentsAll = QtGui.QWidget()
        self.dockWidgetContentsAll.setObjectName(_fromUtf8("dockWidgetContentsAll"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.dockWidgetContentsAll)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.tblViewRaw = QtGui.QTableView(self.dockWidgetContentsAll)
        self.tblViewRaw.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblViewRaw.sizePolicy().hasHeightForWidth())
        self.tblViewRaw.setSizePolicy(sizePolicy)
        self.tblViewRaw.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tblViewRaw.setShowGrid(False)
        self.tblViewRaw.setSortingEnabled(False)
        self.tblViewRaw.setObjectName(_fromUtf8("tblViewRaw"))
        self.verticalLayout_5.addWidget(self.tblViewRaw)
        self.dockWidgetRaw.setWidget(self.dockWidgetContentsAll)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetRaw)
        self.dockWidgetMeta = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetMeta.sizePolicy().hasHeightForWidth())
        self.dockWidgetMeta.setSizePolicy(sizePolicy)
        self.dockWidgetMeta.setFeatures(QtGui.QDockWidget.DockWidgetFloatable)
        self.dockWidgetMeta.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidgetMeta.setObjectName(_fromUtf8("dockWidgetMeta"))
        self.dockWidgetContentsMeta = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContentsMeta.sizePolicy().hasHeightForWidth())
        self.dockWidgetContentsMeta.setSizePolicy(sizePolicy)
        self.dockWidgetContentsMeta.setObjectName(_fromUtf8("dockWidgetContentsMeta"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContentsMeta)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tblViewMeta = QtGui.QTableView(self.dockWidgetContentsMeta)
        self.tblViewMeta.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblViewMeta.sizePolicy().hasHeightForWidth())
        self.tblViewMeta.setSizePolicy(sizePolicy)
        self.tblViewMeta.setFrameShape(QtGui.QFrame.Box)
        self.tblViewMeta.setSortingEnabled(False)
        self.tblViewMeta.setObjectName(_fromUtf8("tblViewMeta"))
        self.horizontalLayout.addWidget(self.tblViewMeta)
        self.dockWidgetMeta.setWidget(self.dockWidgetContentsMeta)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetMeta)
        self.toolBar = QtGui.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionStart_Session = QtGui.QAction(MainWindow)
        self.actionStart_Session.setObjectName(_fromUtf8("actionStart_Session"))
        self.actionEnd_Session = QtGui.QAction(MainWindow)
        self.actionEnd_Session.setObjectName(_fromUtf8("actionEnd_Session"))
        self.actionLoad_File = QtGui.QAction(MainWindow)
        self.actionLoad_File.setObjectName(_fromUtf8("actionLoad_File"))
        self.actionOne_to_many = QtGui.QAction(MainWindow)
        self.actionOne_to_many.setObjectName(_fromUtf8("actionOne_to_many"))
        self.actionMany_to_one = QtGui.QAction(MainWindow)
        self.actionMany_to_one.setObjectName(_fromUtf8("actionMany_to_one"))
        self.actionDisplay_unique = QtGui.QAction(MainWindow)
        self.actionDisplay_unique.setObjectName(_fromUtf8("actionDisplay_unique"))
        self.actionString_split = QtGui.QAction(MainWindow)
        self.actionString_split.setObjectName(_fromUtf8("actionString_split"))
        self.actionUploaded_tables = QtGui.QAction(MainWindow)
        self.actionUploaded_tables.setObjectName(_fromUtf8("actionUploaded_tables"))
        self.actionTables_to_upload = QtGui.QAction(MainWindow)
        self.actionTables_to_upload.setObjectName(_fromUtf8("actionTables_to_upload"))
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
        self.actionModify_ontomany_entries = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionModify_ontomany_entries.setFont(font)
        self.actionModify_ontomany_entries.setObjectName(_fromUtf8("actionModify_ontomany_entries"))
        self.actionActionTemporalParser = QtGui.QAction(MainWindow)
        self.actionActionTemporalParser.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionActionTemporalParser.setFont(font)
        self.actionActionTemporalParser.setVisible(True)
        self.actionActionTemporalParser.setIconVisibleInMenu(True)
        self.actionActionTemporalParser.setObjectName(_fromUtf8("actionActionTemporalParser"))
        self.actionCovariates = QtGui.QAction(MainWindow)
        self.actionCovariates.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.actionCovariates.setFont(font)
        self.actionCovariates.setObjectName(_fromUtf8("actionCovariates"))
        self.actionFactor_levels = QtGui.QAction(MainWindow)
        self.actionFactor_levels.setObjectName(_fromUtf8("actionFactor_levels"))
        self.actionValue = QtGui.QAction(MainWindow)
        self.actionValue.setObjectName(_fromUtf8("actionValue"))
        self.menuFile.addAction(self.actionStart_Session)
        self.menuFile.addAction(self.actionEnd_Session)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad_File)
        self.menuReplace.addAction(self.actionFactor_levels)
        self.menuReplace.addSeparator()
        self.menuReplace.addAction(self.actionValue)
        self.menuEdit.addAction(self.menuReplace.menuAction())
        self.menuEdit.addAction(self.actionDisplay_unique)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionModify_ontomany_entries)
        self.menuSplit.addAction(self.actionOne_to_many)
        self.menuSplit.addAction(self.actionMany_to_one)
        self.menuSplit.addSeparator()
        self.menuSplit.addAction(self.actionString_split)
        self.menuSplit.addSeparator()
        self.menuView.addAction(self.actionUploaded_tables)
        self.menuView.addAction(self.actionTables_to_upload)
        self.menuView.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSplit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionSiteTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMainTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTaxaTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionActionTemporalParser)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRawTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCovariates)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClimateSiteTable)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClimateRawTable)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Formatter", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuReplace.setTitle(_translate("MainWindow", "Replace..", None))
        self.menuSplit.setTitle(_translate("MainWindow", "Split", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.dockWidgetRaw.setWindowTitle(_translate("MainWindow", "Raw Data Viewer", None))
        self.dockWidgetMeta.setWindowTitle(_translate("MainWindow", "Metadata Viewer", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Data Cleaner", None))
        self.actionStart_Session.setText(_translate("MainWindow", "New Session...", None))
        self.actionStart_Session.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionEnd_Session.setText(_translate("MainWindow", "End Session...", None))
        self.actionEnd_Session.setShortcut(_translate("MainWindow", "Ctrl+E", None))
        self.actionLoad_File.setText(_translate("MainWindow", "Load File", None))
        self.actionOne_to_many.setText(_translate("MainWindow", "One to many", None))
        self.actionMany_to_one.setText(_translate("MainWindow", "Many to one", None))
        self.actionDisplay_unique.setText(_translate("MainWindow", "Display unique", None))
        self.actionString_split.setText(_translate("MainWindow", "String split", None))
        self.actionUploaded_tables.setText(_translate("MainWindow", "Uploaded tables", None))
        self.actionTables_to_upload.setText(_translate("MainWindow", "Tables to upload..", None))
        self.actionSiteTable.setText(_translate("MainWindow", "Sites", None))
        self.actionMainTable.setText(_translate("MainWindow", "Metadata", None))
        self.actionTaxaTable.setText(_translate("MainWindow", "Taxa", None))
        self.actionRawTable.setText(_translate("MainWindow", "Observations", None))
        self.actionClimateSiteTable.setText(_translate("MainWindow", "Climate Sites", None))
        self.actionClimateRawTable.setText(_translate("MainWindow", "Climate Observations", None))
        self.actionModify_ontomany_entries.setText(_translate("MainWindow", "Modify one to many records..", None))
        self.actionActionTemporalParser.setText(_translate("MainWindow", "Format Time", None))
        self.actionCovariates.setText(_translate("MainWindow", "Covariates", None))
        self.actionFactor_levels.setText(_translate("MainWindow", "Factor levels", None))
        self.actionValue.setText(_translate("MainWindow", "Value", None))

from PyQt4 import QtWebKit