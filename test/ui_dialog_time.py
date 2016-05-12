# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_time.ui'
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
        Dialog.resize(816, 347)
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
"    maring-bottom: 0px;\n"
"    margin-left: 5px;\n"
"    margin-right:5px;    \n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}\n"
""))
        self.verticalLayout_5 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.groupBox = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.lnedYear = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedYear.sizePolicy().hasHeightForWidth())
        self.lnedYear.setSizePolicy(sizePolicy)
        self.lnedYear.setObjectName(_fromUtf8("lnedYear"))
        self.gridLayout.addWidget(self.lnedYear, 3, 1, 1, 1)
        self.cboxYear = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxYear.sizePolicy().hasHeightForWidth())
        self.cboxYear.setSizePolicy(sizePolicy)
        self.cboxYear.setObjectName(_fromUtf8("cboxYear"))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.cboxYear.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cboxYear, 3, 2, 1, 1)
        self.ckYear = QtGui.QCheckBox(self.groupBox)
        self.ckYear.setObjectName(_fromUtf8("ckYear"))
        self.gridLayout.addWidget(self.ckYear, 3, 3, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.cboxDay = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxDay.sizePolicy().hasHeightForWidth())
        self.cboxDay.setSizePolicy(sizePolicy)
        self.cboxDay.setObjectName(_fromUtf8("cboxDay"))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.cboxDay.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cboxDay, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lnedMonth = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedMonth.sizePolicy().hasHeightForWidth())
        self.lnedMonth.setSizePolicy(sizePolicy)
        self.lnedMonth.setObjectName(_fromUtf8("lnedMonth"))
        self.gridLayout.addWidget(self.lnedMonth, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.cboxMonth = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxMonth.sizePolicy().hasHeightForWidth())
        self.cboxMonth.setSizePolicy(sizePolicy)
        self.cboxMonth.setObjectName(_fromUtf8("cboxMonth"))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.cboxMonth.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cboxMonth, 2, 2, 1, 1)
        self.ckMonth = QtGui.QCheckBox(self.groupBox)
        self.ckMonth.setObjectName(_fromUtf8("ckMonth"))
        self.gridLayout.addWidget(self.ckMonth, 2, 3, 1, 1)
        self.lnedDay = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedDay.sizePolicy().hasHeightForWidth())
        self.lnedDay.setSizePolicy(sizePolicy)
        self.lnedDay.setObjectName(_fromUtf8("lnedDay"))
        self.gridLayout.addWidget(self.lnedDay, 1, 1, 1, 1)
        self.ckDay = QtGui.QCheckBox(self.groupBox)
        self.ckDay.setObjectName(_fromUtf8("ckDay"))
        self.gridLayout.addWidget(self.ckDay, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.ckJulian = QtGui.QCheckBox(self.groupBox)
        self.ckJulian.setObjectName(_fromUtf8("ckJulian"))
        self.gridLayout.addWidget(self.ckJulian, 4, 1, 1, 1)
        self.ckMonthSpelling = QtGui.QCheckBox(self.groupBox)
        self.ckMonthSpelling.setObjectName(_fromUtf8("ckMonthSpelling"))
        self.gridLayout.addWidget(self.ckMonthSpelling, 4, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addWidget(self.frame)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem4)
        self.btnSaveClose = QtGui.QPushButton(Dialog)
        self.btnSaveClose.setObjectName(_fromUtf8("btnSaveClose"))
        self.horizontalLayout_7.addWidget(self.btnSaveClose)
        self.btnCancel = QtGui.QPushButton(Dialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_7.addWidget(self.btnCancel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "Identify Temporal Information", None))
        self.label_4.setText(_translate("Dialog", "Column Name", None))
        self.cboxYear.setItemText(0, _translate("Dialog", "dd - mm - YYYY (Any Order)", None))
        self.cboxYear.setItemText(1, _translate("Dialog", "dd - YYYY (Any Order)", None))
        self.cboxYear.setItemText(2, _translate("Dialog", "MM - YYYY (Any Order)", None))
        self.cboxYear.setItemText(3, _translate("Dialog", "YYYY", None))
        self.cboxYear.setItemText(4, _translate("Dialog", "MM", None))
        self.cboxYear.setItemText(5, _translate("Dialog", "DD", None))
        self.cboxYear.setItemText(6, _translate("Dialog", "dd - mm - YY (Any Order)", None))
        self.cboxYear.setItemText(7, _translate("Dialog", "dd - YY (Any Order)", None))
        self.cboxYear.setItemText(8, _translate("Dialog", "MM - YY (Any Order)", None))
        self.cboxYear.setItemText(9, _translate("Dialog", "YY", None))
        self.ckYear.setText(_translate("Dialog", "Year Not Present", None))
        self.label.setText(_translate("Dialog", "Day", None))
        self.cboxDay.setItemText(0, _translate("Dialog", "dd - mm - YYYY (Any Order)", None))
        self.cboxDay.setItemText(1, _translate("Dialog", "dd - YYYY (Any Order)", None))
        self.cboxDay.setItemText(2, _translate("Dialog", "MM - YYYY (Any Order)", None))
        self.cboxDay.setItemText(3, _translate("Dialog", "YYYY", None))
        self.cboxDay.setItemText(4, _translate("Dialog", "MM", None))
        self.cboxDay.setItemText(5, _translate("Dialog", "DD", None))
        self.cboxDay.setItemText(6, _translate("Dialog", "dd - mm - YY (Any Order)", None))
        self.cboxDay.setItemText(7, _translate("Dialog", "dd - YY (Any Order)", None))
        self.cboxDay.setItemText(8, _translate("Dialog", "MM - YY (Any Order)", None))
        self.cboxDay.setItemText(9, _translate("Dialog", "YY", None))
        self.label_3.setText(_translate("Dialog", "Year", None))
        self.label_5.setText(_translate("Dialog", "Time Format", None))
        self.cboxMonth.setItemText(0, _translate("Dialog", "dd - mm - YYYY (Any Order)", None))
        self.cboxMonth.setItemText(1, _translate("Dialog", "dd - YYYY (Any Order)", None))
        self.cboxMonth.setItemText(2, _translate("Dialog", "MM - YYYY (Any Order)", None))
        self.cboxMonth.setItemText(3, _translate("Dialog", "YYYY", None))
        self.cboxMonth.setItemText(4, _translate("Dialog", "MM", None))
        self.cboxMonth.setItemText(5, _translate("Dialog", "DD", None))
        self.cboxMonth.setItemText(6, _translate("Dialog", "dd - mm - YY (Any Order)", None))
        self.cboxMonth.setItemText(7, _translate("Dialog", "dd - YY (Any Order)", None))
        self.cboxMonth.setItemText(8, _translate("Dialog", "MM - YY (Any Order)", None))
        self.cboxMonth.setItemText(9, _translate("Dialog", "YY", None))
        self.ckMonth.setText(_translate("Dialog", "Month Not Present", None))
        self.ckDay.setText(_translate("Dialog", "Day Not Present", None))
        self.label_2.setText(_translate("Dialog", "Month", None))
        self.ckJulian.setText(_translate("Dialog", "Julian Day", None))
        self.ckMonthSpelling.setText(_translate("Dialog", "Month Spelled Out", None))
        self.btnSaveClose.setText(_translate("Dialog", "Save && Close", None))
        self.btnCancel.setText(_translate("Dialog", "Cancel", None))

