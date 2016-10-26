# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\MillerLab\Desktop\database-development\Views\ui_dialog_cbind.ui'
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
        Dialog.resize(327, 186)
        Dialog.setStyleSheet(_fromUtf8(".QLabel{\n"
"    background: None;\n"
"    padding: 0px;\n"
"    margin: 0px;\n"
"}\n"
".QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 7px;\n"
"    padding: 2px;\n"
"    padding-left: 15px;\n"
"    background: #EEEEEE;\n"
"}\n"
".QFrame, .QWidget{\n"
"    border-radius: 7;\n"
"    background: white;\n"
"}    \n"
"\n"
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
"}\n"
"\n"
"\n"
""))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.lnedColumn1 = QtGui.QLineEdit(self.groupBox)
        self.lnedColumn1.setObjectName(_fromUtf8("lnedColumn1"))
        self.gridLayout.addWidget(self.lnedColumn1, 1, 0, 1, 1)
        self.lnedColumn2 = QtGui.QLineEdit(self.groupBox)
        self.lnedColumn2.setObjectName(_fromUtf8("lnedColumn2"))
        self.gridLayout.addWidget(self.lnedColumn2, 1, 1, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnPreview = QtGui.QPushButton(Dialog)
        self.btnPreview.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnPreview.setObjectName(_fromUtf8("btnPreview"))
        self.horizontalLayout_2.addWidget(self.btnPreview)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btnSaveClose = QtGui.QPushButton(Dialog)
        self.btnSaveClose.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnSaveClose.setObjectName(_fromUtf8("btnSaveClose"))
        self.horizontalLayout_2.addWidget(self.btnSaveClose)
        self.btnCancel = QtGui.QPushButton(Dialog)
        self.btnCancel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "Bind Columns", None))
        self.label.setText(_translate("Dialog", "Column 1:", None))
        self.label_3.setText(_translate("Dialog", "Column 2:", None))
        self.btnPreview.setText(_translate("Dialog", "Preview", None))
        self.btnSaveClose.setText(_translate("Dialog", "Save && Close", None))
        self.btnCancel.setText(_translate("Dialog", "Cancel", None))

