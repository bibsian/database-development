# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\MillerLab\Dropbox\database-development\test\Views\ui_dialog_obs.ui'
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
        Dialog.resize(751, 512)
        Dialog.setFocusPolicy(QtCore.Qt.TabFocus)
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
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lnedRaw = QtGui.QLineEdit(self.groupBox)
        self.lnedRaw.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedRaw.sizePolicy().hasHeightForWidth())
        self.lnedRaw.setSizePolicy(sizePolicy)
        self.lnedRaw.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedRaw.setInputMask(_fromUtf8(""))
        self.lnedRaw.setText(_fromUtf8(""))
        self.lnedRaw.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedRaw.setReadOnly(False)
        self.lnedRaw.setPlaceholderText(_fromUtf8(""))
        self.lnedRaw.setObjectName(_fromUtf8("lnedRaw"))
        self.gridLayout.addWidget(self.lnedRaw, 7, 1, 1, 1)
        self.lnedStructure = QtGui.QLineEdit(self.groupBox)
        self.lnedStructure.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedStructure.sizePolicy().hasHeightForWidth())
        self.lnedStructure.setSizePolicy(sizePolicy)
        self.lnedStructure.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedStructure.setInputMask(_fromUtf8(""))
        self.lnedStructure.setText(_fromUtf8(""))
        self.lnedStructure.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedStructure.setReadOnly(False)
        self.lnedStructure.setPlaceholderText(_fromUtf8(""))
        self.lnedStructure.setObjectName(_fromUtf8("lnedStructure"))
        self.gridLayout.addWidget(self.lnedStructure, 5, 1, 1, 1)
        self.ckStructure = QtGui.QCheckBox(self.groupBox)
        self.ckStructure.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckStructure.setObjectName(_fromUtf8("ckStructure"))
        self.gridLayout.addWidget(self.ckStructure, 5, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.ckRep4 = QtGui.QCheckBox(self.groupBox)
        self.ckRep4.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckRep4.setObjectName(_fromUtf8("ckRep4"))
        self.gridLayout.addWidget(self.ckRep4, 4, 2, 1, 1)
        self.lnedRep4 = QtGui.QLineEdit(self.groupBox)
        self.lnedRep4.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedRep4.sizePolicy().hasHeightForWidth())
        self.lnedRep4.setSizePolicy(sizePolicy)
        self.lnedRep4.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedRep4.setInputMask(_fromUtf8(""))
        self.lnedRep4.setText(_fromUtf8(""))
        self.lnedRep4.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedRep4.setReadOnly(False)
        self.lnedRep4.setPlaceholderText(_fromUtf8(""))
        self.lnedRep4.setObjectName(_fromUtf8("lnedRep4"))
        self.gridLayout.addWidget(self.lnedRep4, 4, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lnedRep2 = QtGui.QLineEdit(self.groupBox)
        self.lnedRep2.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedRep2.sizePolicy().hasHeightForWidth())
        self.lnedRep2.setSizePolicy(sizePolicy)
        self.lnedRep2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedRep2.setInputMask(_fromUtf8(""))
        self.lnedRep2.setText(_fromUtf8(""))
        self.lnedRep2.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedRep2.setReadOnly(False)
        self.lnedRep2.setPlaceholderText(_fromUtf8(""))
        self.lnedRep2.setObjectName(_fromUtf8("lnedRep2"))
        self.gridLayout.addWidget(self.lnedRep2, 2, 1, 1, 1)
        self.ckRep3 = QtGui.QCheckBox(self.groupBox)
        self.ckRep3.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckRep3.setObjectName(_fromUtf8("ckRep3"))
        self.gridLayout.addWidget(self.ckRep3, 3, 2, 1, 1)
        self.ckRep2 = QtGui.QCheckBox(self.groupBox)
        self.ckRep2.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckRep2.setObjectName(_fromUtf8("ckRep2"))
        self.gridLayout.addWidget(self.ckRep2, 2, 2, 1, 1)
        self.lnedRep3 = QtGui.QLineEdit(self.groupBox)
        self.lnedRep3.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedRep3.sizePolicy().hasHeightForWidth())
        self.lnedRep3.setSizePolicy(sizePolicy)
        self.lnedRep3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedRep3.setInputMask(_fromUtf8(""))
        self.lnedRep3.setText(_fromUtf8(""))
        self.lnedRep3.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedRep3.setReadOnly(False)
        self.lnedRep3.setPlaceholderText(_fromUtf8(""))
        self.lnedRep3.setObjectName(_fromUtf8("lnedRep3"))
        self.gridLayout.addWidget(self.lnedRep3, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.ckIndividual = QtGui.QCheckBox(self.groupBox)
        self.ckIndividual.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckIndividual.setObjectName(_fromUtf8("ckIndividual"))
        self.gridLayout.addWidget(self.ckIndividual, 6, 2, 1, 1)
        self.lnedIndividual = QtGui.QLineEdit(self.groupBox)
        self.lnedIndividual.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedIndividual.sizePolicy().hasHeightForWidth())
        self.lnedIndividual.setSizePolicy(sizePolicy)
        self.lnedIndividual.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lnedIndividual.setInputMask(_fromUtf8(""))
        self.lnedIndividual.setText(_fromUtf8(""))
        self.lnedIndividual.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedIndividual.setReadOnly(False)
        self.lnedIndividual.setPlaceholderText(_fromUtf8(""))
        self.lnedIndividual.setObjectName(_fromUtf8("lnedIndividual"))
        self.gridLayout.addWidget(self.lnedIndividual, 6, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.lnedRep1 = QtGui.QLineEdit(self.groupBox)
        self.lnedRep1.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedRep1.sizePolicy().hasHeightForWidth())
        self.lnedRep1.setSizePolicy(sizePolicy)
        self.lnedRep1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lnedRep1.setInputMask(_fromUtf8(""))
        self.lnedRep1.setText(_fromUtf8(""))
        self.lnedRep1.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedRep1.setReadOnly(False)
        self.lnedRep1.setObjectName(_fromUtf8("lnedRep1"))
        self.gridLayout.addWidget(self.lnedRep1, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
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
        self.btnPreview = QtGui.QPushButton(Dialog)
        self.btnPreview.setObjectName(_fromUtf8("btnPreview"))
        self.horizontalLayout_7.addWidget(self.btnPreview)
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
        Dialog.setTabOrder(self.lnedRep1, self.lnedRep2)
        Dialog.setTabOrder(self.lnedRep2, self.ckRep2)
        Dialog.setTabOrder(self.ckRep2, self.lnedRep3)
        Dialog.setTabOrder(self.lnedRep3, self.ckRep3)
        Dialog.setTabOrder(self.ckRep3, self.lnedRep4)
        Dialog.setTabOrder(self.lnedRep4, self.ckRep4)
        Dialog.setTabOrder(self.ckRep4, self.lnedStructure)
        Dialog.setTabOrder(self.lnedStructure, self.ckStructure)
        Dialog.setTabOrder(self.ckStructure, self.lnedIndividual)
        Dialog.setTabOrder(self.lnedIndividual, self.ckIndividual)
        Dialog.setTabOrder(self.ckIndividual, self.lnedRaw)
        Dialog.setTabOrder(self.lnedRaw, self.btnPreview)
        Dialog.setTabOrder(self.btnPreview, self.btnSaveClose)
        Dialog.setTabOrder(self.btnSaveClose, self.btnCancel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Observation Information", None))
        self.groupBox.setTitle(_translate("Dialog", "Raw Observations", None))
        self.label_2.setText(_translate("Dialog", "Replication Level 1", None))
        self.ckStructure.setText(_translate("Dialog", "Structure Data Note Present", None))
        self.label_5.setText(_translate("Dialog", "Replication Level 4", None))
        self.ckRep4.setText(_translate("Dialog", "Level 4 Not Present", None))
        self.label_3.setText(_translate("Dialog", "Replication Level 2", None))
        self.ckRep3.setText(_translate("Dialog", "Level 3 Not Present", None))
        self.ckRep2.setText(_translate("Dialog", "Level 2 Not Present", None))
        self.label_4.setText(_translate("Dialog", "Replication Level 3", None))
        self.label_6.setText(_translate("Dialog", "Organisms Structure", None))
        self.label_7.setText(_translate("Dialog", "Indiviual ID", None))
        self.ckIndividual.setText(_translate("Dialog", "Indivdual ID\'s Not Present", None))
        self.label_8.setText(_translate("Dialog", "Raw Observations", None))
        self.lnedRep1.setPlaceholderText(_translate("Dialog", "Site Column", None))
        self.label.setText(_translate("Dialog", "Columns", None))
        self.btnPreview.setText(_translate("Dialog", "Preview", None))
        self.btnSaveClose.setText(_translate("Dialog", "Save && Close", None))
        self.btnCancel.setText(_translate("Dialog", "Cancel", None))

