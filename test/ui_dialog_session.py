# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\MillerLab\Desktop\database-development\test\Views\ui_dialog_session.ui'
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
        Dialog.resize(743, 420)
        Dialog.setStyleSheet(_fromUtf8(".QLabel{\n"
"    background: None;\n"
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
".QLineEdit{\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid black;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
".QPushButton {\n"
"    color: black;\n"
"    background: #EEEEEE;\n"
"    border-width: 1px;\n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 7;\n"
"    margin-left: 5px;\n"
"    margin-right:5px;    \n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px; /* move to the right by 5px */\n"
"}\n"
"/* Style the tab using the tab sub-control. Note that it reads QTabBar _not_ QTabWidget */\n"
"\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0         #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    padding: 2px;\n"
"}\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"}\n"
"QTabBar::tab:selected {\n"
"    border-color: #9B9B9B;\n"
"    border-bottom-color: #C2C7CB; /* same as pane color */\n"
"}\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"\n"
""))
        self.verticalLayout_6 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.frame = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(_fromUtf8(""))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        spacerItem = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.groupBoxMeta = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxMeta.sizePolicy().hasHeightForWidth())
        self.groupBoxMeta.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxMeta.setFont(font)
        self.groupBoxMeta.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxMeta.setObjectName(_fromUtf8("groupBoxMeta"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBoxMeta)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lnedGlobalId = QtGui.QLineEdit(self.groupBoxMeta)
        self.lnedGlobalId.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedGlobalId.sizePolicy().hasHeightForWidth())
        self.lnedGlobalId.setSizePolicy(sizePolicy)
        self.lnedGlobalId.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedGlobalId.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedGlobalId.setObjectName(_fromUtf8("lnedGlobalId"))
        self.horizontalLayout.addWidget(self.lnedGlobalId)
        self.cboxLTERloc = QtGui.QComboBox(self.groupBoxMeta)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboxLTERloc.sizePolicy().hasHeightForWidth())
        self.cboxLTERloc.setSizePolicy(sizePolicy)
        self.cboxLTERloc.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.cboxLTERloc.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cboxLTERloc.setAutoFillBackground(False)
        self.cboxLTERloc.setFrame(False)
        self.cboxLTERloc.setObjectName(_fromUtf8("cboxLTERloc"))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.cboxLTERloc.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.cboxLTERloc)
        self.lnedMetadataUrl = QtGui.QLineEdit(self.groupBoxMeta)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedMetadataUrl.sizePolicy().hasHeightForWidth())
        self.lnedMetadataUrl.setSizePolicy(sizePolicy)
        self.lnedMetadataUrl.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedMetadataUrl.setText(_fromUtf8(""))
        self.lnedMetadataUrl.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedMetadataUrl.setObjectName(_fromUtf8("lnedMetadataUrl"))
        self.horizontalLayout.addWidget(self.lnedMetadataUrl)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnVerifyMeta = QtGui.QPushButton(self.groupBoxMeta)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnVerifyMeta.sizePolicy().hasHeightForWidth())
        self.btnVerifyMeta.setSizePolicy(sizePolicy)
        self.btnVerifyMeta.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnVerifyMeta.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.btnVerifyMeta.setAutoDefault(False)
        self.btnVerifyMeta.setFlat(False)
        self.btnVerifyMeta.setObjectName(_fromUtf8("btnVerifyMeta"))
        self.horizontalLayout_2.addWidget(self.btnVerifyMeta)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_7.addWidget(self.groupBoxMeta)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem4 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.groupBoxFile = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxFile.sizePolicy().hasHeightForWidth())
        self.groupBoxFile.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxFile.setFont(font)
        self.groupBoxFile.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxFile.setObjectName(_fromUtf8("groupBoxFile"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBoxFile)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lnedDelimiter = QtGui.QLineEdit(self.groupBoxFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedDelimiter.sizePolicy().hasHeightForWidth())
        self.lnedDelimiter.setSizePolicy(sizePolicy)
        self.lnedDelimiter.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedDelimiter.setText(_fromUtf8(""))
        self.lnedDelimiter.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedDelimiter.setObjectName(_fromUtf8("lnedDelimiter"))
        self.gridLayout.addWidget(self.lnedDelimiter, 2, 1, 1, 1)
        self.lnedSkipBottom = QtGui.QLineEdit(self.groupBoxFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedSkipBottom.sizePolicy().hasHeightForWidth())
        self.lnedSkipBottom.setSizePolicy(sizePolicy)
        self.lnedSkipBottom.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedSkipBottom.setText(_fromUtf8(""))
        self.lnedSkipBottom.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedSkipBottom.setObjectName(_fromUtf8("lnedSkipBottom"))
        self.gridLayout.addWidget(self.lnedSkipBottom, 2, 3, 1, 1)
        self.rbtnTxt = QtGui.QRadioButton(self.groupBoxFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbtnTxt.sizePolicy().hasHeightForWidth())
        self.rbtnTxt.setSizePolicy(sizePolicy)
        self.rbtnTxt.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rbtnTxt.setObjectName(_fromUtf8("rbtnTxt"))
        self.gridLayout.addWidget(self.rbtnTxt, 2, 0, 1, 1)
        self.ckHeader = QtGui.QCheckBox(self.groupBoxFile)
        self.ckHeader.setObjectName(_fromUtf8("ckHeader"))
        self.gridLayout.addWidget(self.ckHeader, 2, 4, 1, 1)
        self.lnedSkipTop = QtGui.QLineEdit(self.groupBoxFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedSkipTop.sizePolicy().hasHeightForWidth())
        self.lnedSkipTop.setSizePolicy(sizePolicy)
        self.lnedSkipTop.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedSkipTop.setText(_fromUtf8(""))
        self.lnedSkipTop.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedSkipTop.setObjectName(_fromUtf8("lnedSkipTop"))
        self.gridLayout.addWidget(self.lnedSkipTop, 2, 2, 1, 1)
        self.lnedExcelSheet = QtGui.QLineEdit(self.groupBoxFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedExcelSheet.sizePolicy().hasHeightForWidth())
        self.lnedExcelSheet.setSizePolicy(sizePolicy)
        self.lnedExcelSheet.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedExcelSheet.setText(_fromUtf8(""))
        self.lnedExcelSheet.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedExcelSheet.setObjectName(_fromUtf8("lnedExcelSheet"))
        self.gridLayout.addWidget(self.lnedExcelSheet, 1, 1, 1, 1)
        self.rbtnCsv = QtGui.QRadioButton(self.groupBoxFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbtnCsv.sizePolicy().hasHeightForWidth())
        self.rbtnCsv.setSizePolicy(sizePolicy)
        self.rbtnCsv.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rbtnCsv.setObjectName(_fromUtf8("rbtnCsv"))
        self.gridLayout.addWidget(self.rbtnCsv, 0, 0, 1, 1)
        self.rbtnExcel = QtGui.QRadioButton(self.groupBoxFile)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbtnExcel.sizePolicy().hasHeightForWidth())
        self.rbtnExcel.setSizePolicy(sizePolicy)
        self.rbtnExcel.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rbtnExcel.setObjectName(_fromUtf8("rbtnExcel"))
        self.gridLayout.addWidget(self.rbtnExcel, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.btnSelectFile = QtGui.QPushButton(self.groupBoxFile)
        self.btnSelectFile.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectFile.sizePolicy().hasHeightForWidth())
        self.btnSelectFile.setSizePolicy(sizePolicy)
        self.btnSelectFile.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnSelectFile.setAutoDefault(False)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.horizontalLayout_4.addWidget(self.btnSelectFile)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.horizontalLayout_6.addWidget(self.groupBoxFile)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        spacerItem8 = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem8)
        self.verticalLayout_5.addWidget(self.frame)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.btnSaveClose = QtGui.QPushButton(Dialog)
        self.btnSaveClose.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnSaveClose.setAutoDefault(False)
        self.btnSaveClose.setObjectName(_fromUtf8("btnSaveClose"))
        self.horizontalLayout_3.addWidget(self.btnSaveClose)
        self.btnCancel = QtGui.QPushButton(Dialog)
        self.btnCancel.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnCancel.setAutoDefault(False)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lnedGlobalId, self.cboxLTERloc)
        Dialog.setTabOrder(self.cboxLTERloc, self.lnedMetadataUrl)
        Dialog.setTabOrder(self.lnedMetadataUrl, self.btnVerifyMeta)
        Dialog.setTabOrder(self.btnVerifyMeta, self.rbtnCsv)
        Dialog.setTabOrder(self.rbtnCsv, self.rbtnExcel)
        Dialog.setTabOrder(self.rbtnExcel, self.lnedExcelSheet)
        Dialog.setTabOrder(self.lnedExcelSheet, self.rbtnTxt)
        Dialog.setTabOrder(self.rbtnTxt, self.lnedDelimiter)
        Dialog.setTabOrder(self.lnedDelimiter, self.lnedSkipTop)
        Dialog.setTabOrder(self.lnedSkipTop, self.lnedSkipBottom)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Create Session", None))
        self.groupBoxMeta.setTitle(_translate("Dialog", "Select Metadata Record to Upload", None))
        self.lnedGlobalId.setPlaceholderText(_translate("Dialog", "Global Id", None))
        self.cboxLTERloc.setItemText(0, _translate("Dialog", "LTER Location", None))
        self.cboxLTERloc.setItemText(1, _translate("Dialog", "AND", None))
        self.cboxLTERloc.setItemText(2, _translate("Dialog", "ARC", None))
        self.cboxLTERloc.setItemText(3, _translate("Dialog", "BES", None))
        self.cboxLTERloc.setItemText(4, _translate("Dialog", "BNZ", None))
        self.cboxLTERloc.setItemText(5, _translate("Dialog", "CCE", None))
        self.cboxLTERloc.setItemText(6, _translate("Dialog", "CDR", None))
        self.cboxLTERloc.setItemText(7, _translate("Dialog", "CAP", None))
        self.cboxLTERloc.setItemText(8, _translate("Dialog", "CWT", None))
        self.cboxLTERloc.setItemText(9, _translate("Dialog", "FCE", None))
        self.cboxLTERloc.setItemText(10, _translate("Dialog", "GCE", None))
        self.cboxLTERloc.setItemText(11, _translate("Dialog", "HFR", None))
        self.cboxLTERloc.setItemText(12, _translate("Dialog", "HBR", None))
        self.cboxLTERloc.setItemText(13, _translate("Dialog", "JRN", None))
        self.cboxLTERloc.setItemText(14, _translate("Dialog", "KBS", None))
        self.cboxLTERloc.setItemText(15, _translate("Dialog", "KNZ", None))
        self.cboxLTERloc.setItemText(16, _translate("Dialog", "LNO", None))
        self.cboxLTERloc.setItemText(17, _translate("Dialog", "LUQ", None))
        self.cboxLTERloc.setItemText(18, _translate("Dialog", "MCM", None))
        self.cboxLTERloc.setItemText(19, _translate("Dialog", "MCR", None))
        self.cboxLTERloc.setItemText(20, _translate("Dialog", "NWT", None))
        self.cboxLTERloc.setItemText(21, _translate("Dialog", "NTL", None))
        self.cboxLTERloc.setItemText(22, _translate("Dialog", "PAL", None))
        self.cboxLTERloc.setItemText(23, _translate("Dialog", "PIE", None))
        self.cboxLTERloc.setItemText(24, _translate("Dialog", "SBC", None))
        self.cboxLTERloc.setItemText(25, _translate("Dialog", "SEV", None))
        self.cboxLTERloc.setItemText(26, _translate("Dialog", "SGS", None))
        self.cboxLTERloc.setItemText(27, _translate("Dialog", "VCR", None))
        self.lnedMetadataUrl.setPlaceholderText(_translate("Dialog", "Metadata URL", None))
        self.btnVerifyMeta.setText(_translate("Dialog", "Verify", None))
        self.groupBoxFile.setTitle(_translate("Dialog", "Select Raw Data Input File", None))
        self.lnedDelimiter.setPlaceholderText(_translate("Dialog", "Delimiter", None))
        self.lnedSkipBottom.setPlaceholderText(_translate("Dialog", "Skip Lines (Bottom)", None))
        self.rbtnTxt.setText(_translate("Dialog", "txt", None))
        self.ckHeader.setText(_translate("Dialog", "No Column Headers", None))
        self.lnedSkipTop.setPlaceholderText(_translate("Dialog", "Skip Lines (Top)", None))
        self.lnedExcelSheet.setPlaceholderText(_translate("Dialog", "Sheet Number", None))
        self.rbtnCsv.setText(_translate("Dialog", "csv", None))
        self.rbtnExcel.setText(_translate("Dialog", "xlsx / xls", None))
        self.btnSelectFile.setText(_translate("Dialog", "Select File", None))
        self.btnSaveClose.setText(_translate("Dialog", "Save && Close", None))
        self.btnCancel.setText(_translate("Dialog", "Cancel", None))

