# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\MillerLab\Desktop\database-development\test\Views\ui_dialog_taxa.ui'
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
        Dialog.resize(483, 515)
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
        self.verticalLayout_4 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.frame = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(378, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(13, 335, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
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
        self.formLayout_9 = QtGui.QFormLayout()
        self.formLayout_9.setVerticalSpacing(20)
        self.formLayout_9.setObjectName(_fromUtf8("formLayout_9"))
        self.ckCreateTaxa = QtGui.QCheckBox(self.groupBox)
        self.ckCreateTaxa.setObjectName(_fromUtf8("ckCreateTaxa"))
        self.formLayout_9.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckCreateTaxa)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.ckSppCode = QtGui.QCheckBox(self.groupBox)
        self.ckSppCode.setObjectName(_fromUtf8("ckSppCode"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckSppCode)
        self.lnedSppCode = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedSppCode.sizePolicy().hasHeightForWidth())
        self.lnedSppCode.setSizePolicy(sizePolicy)
        self.lnedSppCode.setObjectName(_fromUtf8("lnedSppCode"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedSppCode)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.formLayout_5 = QtGui.QFormLayout()
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.ckOrder = QtGui.QCheckBox(self.groupBox)
        self.ckOrder.setObjectName(_fromUtf8("ckOrder"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckOrder)
        self.lnedOrder = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedOrder.sizePolicy().hasHeightForWidth())
        self.lnedOrder.setSizePolicy(sizePolicy)
        self.lnedOrder.setObjectName(_fromUtf8("lnedOrder"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedOrder)
        self.gridLayout.addLayout(self.formLayout_5, 0, 1, 1, 1)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.ckKingdom = QtGui.QCheckBox(self.groupBox)
        self.ckKingdom.setObjectName(_fromUtf8("ckKingdom"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckKingdom)
        self.lnedKingdom = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedKingdom.sizePolicy().hasHeightForWidth())
        self.lnedKingdom.setSizePolicy(sizePolicy)
        self.lnedKingdom.setObjectName(_fromUtf8("lnedKingdom"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedKingdom)
        self.gridLayout.addLayout(self.formLayout_2, 1, 0, 1, 1)
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.ckFamily = QtGui.QCheckBox(self.groupBox)
        self.ckFamily.setObjectName(_fromUtf8("ckFamily"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckFamily)
        self.lnedFamily = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedFamily.sizePolicy().hasHeightForWidth())
        self.lnedFamily.setSizePolicy(sizePolicy)
        self.lnedFamily.setObjectName(_fromUtf8("lnedFamily"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedFamily)
        self.gridLayout.addLayout(self.formLayout_6, 1, 1, 1, 1)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.ckPhylum = QtGui.QCheckBox(self.groupBox)
        self.ckPhylum.setObjectName(_fromUtf8("ckPhylum"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckPhylum)
        self.lnedPhylum = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedPhylum.sizePolicy().hasHeightForWidth())
        self.lnedPhylum.setSizePolicy(sizePolicy)
        self.lnedPhylum.setObjectName(_fromUtf8("lnedPhylum"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedPhylum)
        self.gridLayout.addLayout(self.formLayout_3, 2, 0, 1, 1)
        self.formLayout_7 = QtGui.QFormLayout()
        self.formLayout_7.setObjectName(_fromUtf8("formLayout_7"))
        self.ckGenus = QtGui.QCheckBox(self.groupBox)
        self.ckGenus.setObjectName(_fromUtf8("ckGenus"))
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckGenus)
        self.lnedGenus = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedGenus.sizePolicy().hasHeightForWidth())
        self.lnedGenus.setSizePolicy(sizePolicy)
        self.lnedGenus.setObjectName(_fromUtf8("lnedGenus"))
        self.formLayout_7.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedGenus)
        self.gridLayout.addLayout(self.formLayout_7, 2, 1, 1, 1)
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.ckClass = QtGui.QCheckBox(self.groupBox)
        self.ckClass.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ckClass.setObjectName(_fromUtf8("ckClass"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckClass)
        self.lnedClass = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedClass.sizePolicy().hasHeightForWidth())
        self.lnedClass.setSizePolicy(sizePolicy)
        self.lnedClass.setObjectName(_fromUtf8("lnedClass"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedClass)
        self.gridLayout.addLayout(self.formLayout_4, 3, 0, 1, 1)
        self.formLayout_8 = QtGui.QFormLayout()
        self.formLayout_8.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_8.setObjectName(_fromUtf8("formLayout_8"))
        self.ckSpp = QtGui.QCheckBox(self.groupBox)
        self.ckSpp.setObjectName(_fromUtf8("ckSpp"))
        self.formLayout_8.setWidget(0, QtGui.QFormLayout.LabelRole, self.ckSpp)
        self.lnedSpp = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedSpp.sizePolicy().hasHeightForWidth())
        self.lnedSpp.setSizePolicy(sizePolicy)
        self.lnedSpp.setObjectName(_fromUtf8("lnedSpp"))
        self.formLayout_8.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lnedSpp)
        self.gridLayout.addLayout(self.formLayout_8, 3, 1, 1, 1)
        self.formLayout_9.setLayout(1, QtGui.QFormLayout.LabelRole, self.gridLayout)
        self.verticalLayout.addLayout(self.formLayout_9)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem2 = QtGui.QSpacerItem(13, 335, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem3 = QtGui.QSpacerItem(13, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnTaxasubmit = QtGui.QPushButton(Dialog)
        self.btnTaxasubmit.setObjectName(_fromUtf8("btnTaxasubmit"))
        self.horizontalLayout_3.addWidget(self.btnTaxasubmit)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.btnSaveClose = QtGui.QPushButton(Dialog)
        self.btnSaveClose.setObjectName(_fromUtf8("btnSaveClose"))
        self.horizontalLayout_3.addWidget(self.btnSaveClose)
        self.btnCancel = QtGui.QPushButton(Dialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.ckCreateTaxa, self.ckSppCode)
        Dialog.setTabOrder(self.ckSppCode, self.lnedSppCode)
        Dialog.setTabOrder(self.lnedSppCode, self.ckKingdom)
        Dialog.setTabOrder(self.ckKingdom, self.lnedKingdom)
        Dialog.setTabOrder(self.lnedKingdom, self.ckPhylum)
        Dialog.setTabOrder(self.ckPhylum, self.lnedPhylum)
        Dialog.setTabOrder(self.lnedPhylum, self.ckClass)
        Dialog.setTabOrder(self.ckClass, self.lnedClass)
        Dialog.setTabOrder(self.lnedClass, self.ckOrder)
        Dialog.setTabOrder(self.ckOrder, self.lnedOrder)
        Dialog.setTabOrder(self.lnedOrder, self.ckFamily)
        Dialog.setTabOrder(self.ckFamily, self.lnedFamily)
        Dialog.setTabOrder(self.lnedFamily, self.ckGenus)
        Dialog.setTabOrder(self.ckGenus, self.lnedGenus)
        Dialog.setTabOrder(self.lnedGenus, self.ckSpp)
        Dialog.setTabOrder(self.ckSpp, self.lnedSpp)
        Dialog.setTabOrder(self.lnedSpp, self.btnTaxasubmit)
        Dialog.setTabOrder(self.btnTaxasubmit, self.btnSaveClose)
        Dialog.setTabOrder(self.btnSaveClose, self.btnCancel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Taxonomic Information", None))
        self.groupBox.setTitle(_translate("Dialog", "Identify Taxa Information", None))
        self.ckCreateTaxa.setText(_translate("Dialog", "Create Taxonomic Labels", None))
        self.ckSppCode.setText(_translate("Dialog", "Species Code", None))
        self.ckOrder.setText(_translate("Dialog", "Order", None))
        self.ckKingdom.setText(_translate("Dialog", "Kingom", None))
        self.ckFamily.setText(_translate("Dialog", "Family", None))
        self.ckPhylum.setText(_translate("Dialog", "Phylum", None))
        self.ckGenus.setText(_translate("Dialog", "Genus", None))
        self.ckClass.setText(_translate("Dialog", "Class", None))
        self.ckSpp.setText(_translate("Dialog", "Species Name", None))
        self.btnTaxasubmit.setText(_translate("Dialog", "Preview", None))
        self.btnSaveClose.setText(_translate("Dialog", "Save && Close", None))
        self.btnCancel.setText(_translate("Dialog", "Cancel", None))

