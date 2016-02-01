# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui1_Test.ui'
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
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabDBRawView = QtGui.QTabWidget(self.centralwidget)
        self.tabDBRawView.setGeometry(QtCore.QRect(230, 50, 302, 255))
        self.tabDBRawView.setObjectName(_fromUtf8("tabDBRawView"))
        self.tabDB = QtGui.QWidget()
        self.tabDB.setObjectName(_fromUtf8("tabDB"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabDB)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeDB = QtGui.QTreeView(self.tabDB)
        self.treeDB.setObjectName(_fromUtf8("treeDB"))
        self.verticalLayout.addWidget(self.treeDB)
        self.tabDBRawView.addTab(self.tabDB, _fromUtf8(""))
        self.tabRaw = QtGui.QWidget()
        self.tabRaw.setObjectName(_fromUtf8("tabRaw"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabRaw)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblRaw = QtGui.QTableView(self.tabRaw)
        self.tblRaw.setObjectName(_fromUtf8("tblRaw"))
        self.verticalLayout_2.addWidget(self.tblRaw)
        self.tabDBRawView.addTab(self.tabRaw, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.actionOpen_Raw_File = QtGui.QAction(MainWindow)
        self.actionOpen_Raw_File.setObjectName(_fromUtf8("actionOpen_Raw_File"))
        self.menuFile.addAction(self.actionConnect)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_Raw_File)
        self.menuFile.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabDBRawView.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.tabDBRawView.setTabText(self.tabDBRawView.indexOf(self.tabDB), _translate("MainWindow", "Tab 1", None))
        self.tabDBRawView.setTabText(self.tabDBRawView.indexOf(self.tabRaw), _translate("MainWindow", "Tab 2", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionConnect.setText(_translate("MainWindow", "Connect", None))
        self.actionOpen_Raw_File.setText(_translate("MainWindow", "Open Raw File", None))

