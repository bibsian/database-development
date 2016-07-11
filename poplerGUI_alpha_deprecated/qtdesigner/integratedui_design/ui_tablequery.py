# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\MillerLab\Dropbox\database-development\GUI\qtdesigner\integratedui_design\ui_tablequery.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(593, 486)
        Dialog.setStyleSheet(_fromUtf8("\n"
".QPushButton{\n"
"    color: black;\n"
"    border-width: 1px;\n"
"    border-color: #339;\n"
"    border-style: solid;\n"
"    border-radius: 7;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    padding-top: 5px;\n"
"    padding-bottom: 5px;\n"
"}\n"
"\n"
".QLabel{\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"    padding: 5px;\n"
"    border-radius: 2px;\n"
"    border: 1px solid black;\n"
"\n"
"}\n"
"\n"
"\n"
""))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setFrameShape(QtGui.QFrame.Box)
        self.label_2.setFrameShadow(QtGui.QFrame.Plain)
        self.label_2.setLineWidth(1)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.tblList = QtGui.QTableView(Dialog)
        self.tblList.setObjectName(_fromUtf8("tblList"))
        self.verticalLayout_2.addWidget(self.tblList)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setStyleSheet(_fromUtf8("QLineEdit{\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 2px solid gray;\n"
"    border-radius: 8px;\n"
"}"))
        self.label_3.setFrameShape(QtGui.QFrame.Box)
        self.label_3.setFrameShadow(QtGui.QFrame.Plain)
        self.label_3.setLineWidth(1)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.queryTable = QtGui.QTableView(Dialog)
        self.queryTable.setStyleSheet(_fromUtf8(""))
        self.queryTable.setObjectName(_fromUtf8("queryTable"))
        self.verticalLayout.addWidget(self.queryTable)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setStyleSheet(_fromUtf8(".QLabel{\n"
"    font-size: 12px;\n"
"    padding: 5px;\n"
"    border-radius: 2px;\n"
"    border: 1px;\n"
"\n"
"}\n"
""))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnboxOk = QtGui.QDialogButtonBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnboxOk.sizePolicy().hasHeightForWidth())
        self.btnboxOk.setSizePolicy(sizePolicy)
        self.btnboxOk.setOrientation(QtCore.Qt.Horizontal)
        self.btnboxOk.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.btnboxOk.setObjectName(_fromUtf8("btnboxOk"))
        self.horizontalLayout_2.addWidget(self.btnboxOk)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "Table of Generated Information", None))
        self.label_3.setText(_translate("Dialog", "Database Query for Current Related Records", None))
        self.label.setText(_translate("Dialog", "If the generated list contains records already in the database skip this form.", None))
        self.btnboxOk.setToolTip(_translate("Dialog", "If the site labels and coordinates match \n"
" values in the database you may skip \n"
" this form.", None))

