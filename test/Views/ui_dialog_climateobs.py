# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/bibsian/Desktop/git/database-development/test/Views/ui_dialog_climateobs.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1210, 548)
        Form.setStyleSheet(_fromUtf8(".QLabel{\n"
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
""))
        self.layoutWidget = QtGui.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(23, 13, 1149, 518))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.frame = QtGui.QFrame(self.layoutWidget)
        self.frame.setStyleSheet(_fromUtf8(""))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
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
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 5, -1, -1)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_10 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        self.lnedTitle = QtGui.QLineEdit(self.groupBox)
        self.lnedTitle.setObjectName(_fromUtf8("lnedTitle"))
        self.gridLayout.addWidget(self.lnedTitle, 2, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 1, 1, 1)
        self.lnedMetarecordid = QtGui.QLineEdit(self.groupBox)
        self.lnedMetarecordid.setObjectName(_fromUtf8("lnedMetarecordid"))
        self.gridLayout.addWidget(self.lnedMetarecordid, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(-1, 5, -1, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.rbtnAggregate = QtGui.QRadioButton(self.groupBox)
        self.rbtnAggregate.setObjectName(_fromUtf8("rbtnAggregate"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.rbtnAggregate)
        self.rbtNoaggregate = QtGui.QRadioButton(self.groupBox)
        self.rbtNoaggregate.setObjectName(_fromUtf8("rbtNoaggregate"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.rbtNoaggregate)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.btnDateformat = QtGui.QPushButton(self.groupBox)
        self.btnDateformat.setObjectName(_fromUtf8("btnDateformat"))
        self.horizontalLayout_3.addWidget(self.btnDateformat)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.formLayout.setLayout(2, QtGui.QFormLayout.LabelRole, self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(10, 10, 0, 10)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.ckWatertempmin = QtGui.QCheckBox(self.groupBox)
        self.ckWatertempmin.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckWatertempmin.setObjectName(_fromUtf8("ckWatertempmin"))
        self.gridLayout_2.addWidget(self.ckWatertempmin, 5, 7, 1, 1)
        self.ckAirmin = QtGui.QCheckBox(self.groupBox)
        self.ckAirmin.setObjectName(_fromUtf8("ckAirmin"))
        self.gridLayout_2.addWidget(self.ckAirmin, 1, 7, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 9, 0, 1, 1)
        self.lnedCondavg = QtGui.QLineEdit(self.groupBox)
        self.lnedCondavg.setObjectName(_fromUtf8("lnedCondavg"))
        self.gridLayout_2.addWidget(self.lnedCondavg, 7, 2, 1, 1)
        self.lnedAirmax = QtGui.QLineEdit(self.groupBox)
        self.lnedAirmax.setObjectName(_fromUtf8("lnedAirmax"))
        self.gridLayout_2.addWidget(self.lnedAirmax, 1, 4, 1, 1)
        self.lnedPrecipavg = QtGui.QLineEdit(self.groupBox)
        self.lnedPrecipavg.setObjectName(_fromUtf8("lnedPrecipavg"))
        self.gridLayout_2.addWidget(self.lnedPrecipavg, 2, 2, 1, 1)
        self.ckAirmax = QtGui.QCheckBox(self.groupBox)
        self.ckAirmax.setObjectName(_fromUtf8("ckAirmax"))
        self.gridLayout_2.addWidget(self.ckAirmax, 1, 5, 1, 1)
        self.lnedWatertempavg = QtGui.QLineEdit(self.groupBox)
        self.lnedWatertempavg.setObjectName(_fromUtf8("lnedWatertempavg"))
        self.gridLayout_2.addWidget(self.lnedWatertempavg, 5, 2, 1, 1)
        self.lnedCovmin = QtGui.QLineEdit(self.groupBox)
        self.lnedCovmin.setObjectName(_fromUtf8("lnedCovmin"))
        self.gridLayout_2.addWidget(self.lnedCovmin, 9, 6, 1, 1)
        self.ckCondmin = QtGui.QCheckBox(self.groupBox)
        self.ckCondmin.setObjectName(_fromUtf8("ckCondmin"))
        self.gridLayout_2.addWidget(self.ckCondmin, 7, 7, 1, 1)
        self.ckWindmax = QtGui.QCheckBox(self.groupBox)
        self.ckWindmax.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckWindmax.setObjectName(_fromUtf8("ckWindmax"))
        self.gridLayout_2.addWidget(self.ckWindmax, 3, 5, 1, 1)
        self.ckTurbidityavg = QtGui.QCheckBox(self.groupBox)
        self.ckTurbidityavg.setObjectName(_fromUtf8("ckTurbidityavg"))
        self.gridLayout_2.addWidget(self.ckTurbidityavg, 8, 3, 1, 1)
        self.lnedTurbidityavg = QtGui.QLineEdit(self.groupBox)
        self.lnedTurbidityavg.setObjectName(_fromUtf8("lnedTurbidityavg"))
        self.gridLayout_2.addWidget(self.lnedTurbidityavg, 8, 2, 1, 1)
        self.lnedCovmax = QtGui.QLineEdit(self.groupBox)
        self.lnedCovmax.setObjectName(_fromUtf8("lnedCovmax"))
        self.gridLayout_2.addWidget(self.lnedCovmax, 9, 4, 1, 1)
        self.ckLightavg = QtGui.QCheckBox(self.groupBox)
        self.ckLightavg.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckLightavg.setObjectName(_fromUtf8("ckLightavg"))
        self.gridLayout_2.addWidget(self.ckLightavg, 4, 3, 1, 1)
        self.lnedPrecipmin = QtGui.QLineEdit(self.groupBox)
        self.lnedPrecipmin.setObjectName(_fromUtf8("lnedPrecipmin"))
        self.gridLayout_2.addWidget(self.lnedPrecipmin, 2, 6, 1, 1)
        self.lnedPhunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedPhunits.sizePolicy().hasHeightForWidth())
        self.lnedPhunits.setSizePolicy(sizePolicy)
        self.lnedPhunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedPhunits.setObjectName(_fromUtf8("lnedPhunits"))
        self.gridLayout_2.addWidget(self.lnedPhunits, 6, 1, 1, 1)
        self.lnedWatertempmax = QtGui.QLineEdit(self.groupBox)
        self.lnedWatertempmax.setObjectName(_fromUtf8("lnedWatertempmax"))
        self.gridLayout_2.addWidget(self.lnedWatertempmax, 5, 4, 1, 1)
        self.lnedLightmin = QtGui.QLineEdit(self.groupBox)
        self.lnedLightmin.setObjectName(_fromUtf8("lnedLightmin"))
        self.gridLayout_2.addWidget(self.lnedLightmin, 4, 6, 1, 1)
        self.ckCondmax = QtGui.QCheckBox(self.groupBox)
        self.ckCondmax.setObjectName(_fromUtf8("ckCondmax"))
        self.gridLayout_2.addWidget(self.ckCondmax, 7, 5, 1, 1)
        self.ckPrecipmin = QtGui.QCheckBox(self.groupBox)
        self.ckPrecipmin.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckPrecipmin.setObjectName(_fromUtf8("ckPrecipmin"))
        self.gridLayout_2.addWidget(self.ckPrecipmin, 2, 7, 1, 1)
        self.lnedCovunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedCovunits.sizePolicy().hasHeightForWidth())
        self.lnedCovunits.setSizePolicy(sizePolicy)
        self.lnedCovunits.setStyleSheet(_fromUtf8("QLineEdit{\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid black;\n"
"    margin: 0px;\n"
"}\n"
"\n"
""))
        self.lnedCovunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedCovunits.setObjectName(_fromUtf8("lnedCovunits"))
        self.gridLayout_2.addWidget(self.lnedCovunits, 9, 1, 1, 1)
        self.lnedCondmin = QtGui.QLineEdit(self.groupBox)
        self.lnedCondmin.setObjectName(_fromUtf8("lnedCondmin"))
        self.gridLayout_2.addWidget(self.lnedCondmin, 7, 6, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 7, 0, 1, 1)
        self.ckWindmin = QtGui.QCheckBox(self.groupBox)
        self.ckWindmin.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckWindmin.setObjectName(_fromUtf8("ckWindmin"))
        self.gridLayout_2.addWidget(self.ckWindmin, 3, 7, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)
        self.ckPrecipmax = QtGui.QCheckBox(self.groupBox)
        self.ckPrecipmax.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckPrecipmax.setObjectName(_fromUtf8("ckPrecipmax"))
        self.gridLayout_2.addWidget(self.ckPrecipmax, 2, 5, 1, 1)
        self.lnedWindunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedWindunits.sizePolicy().hasHeightForWidth())
        self.lnedWindunits.setSizePolicy(sizePolicy)
        self.lnedWindunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedWindunits.setObjectName(_fromUtf8("lnedWindunits"))
        self.gridLayout_2.addWidget(self.lnedWindunits, 3, 1, 1, 1)
        self.ckPhmax = QtGui.QCheckBox(self.groupBox)
        self.ckPhmax.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckPhmax.setObjectName(_fromUtf8("ckPhmax"))
        self.gridLayout_2.addWidget(self.ckPhmax, 6, 5, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 6, 0, 1, 1)
        self.lnedWindmax = QtGui.QLineEdit(self.groupBox)
        self.lnedWindmax.setObjectName(_fromUtf8("lnedWindmax"))
        self.gridLayout_2.addWidget(self.lnedWindmax, 3, 4, 1, 1)
        self.lnedPrecipunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedPrecipunits.sizePolicy().hasHeightForWidth())
        self.lnedPrecipunits.setSizePolicy(sizePolicy)
        self.lnedPrecipunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedPrecipunits.setObjectName(_fromUtf8("lnedPrecipunits"))
        self.gridLayout_2.addWidget(self.lnedPrecipunits, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lnedLightunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedLightunits.sizePolicy().hasHeightForWidth())
        self.lnedLightunits.setSizePolicy(sizePolicy)
        self.lnedLightunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedLightunits.setObjectName(_fromUtf8("lnedLightunits"))
        self.gridLayout_2.addWidget(self.lnedLightunits, 4, 1, 1, 1)
        self.lnedCondunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedCondunits.sizePolicy().hasHeightForWidth())
        self.lnedCondunits.setSizePolicy(sizePolicy)
        self.lnedCondunits.setStyleSheet(_fromUtf8("QLineEdit{\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid black;\n"
"    margin: 0px;\n"
"}\n"
"\n"
""))
        self.lnedCondunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedCondunits.setObjectName(_fromUtf8("lnedCondunits"))
        self.gridLayout_2.addWidget(self.lnedCondunits, 7, 1, 1, 1)
        self.ckWindavg = QtGui.QCheckBox(self.groupBox)
        self.ckWindavg.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckWindavg.setObjectName(_fromUtf8("ckWindavg"))
        self.gridLayout_2.addWidget(self.ckWindavg, 3, 3, 1, 1)
        self.ckPhmin = QtGui.QCheckBox(self.groupBox)
        self.ckPhmin.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckPhmin.setObjectName(_fromUtf8("ckPhmin"))
        self.gridLayout_2.addWidget(self.ckPhmin, 6, 7, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.ckPhavg = QtGui.QCheckBox(self.groupBox)
        self.ckPhavg.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckPhavg.setObjectName(_fromUtf8("ckPhavg"))
        self.gridLayout_2.addWidget(self.ckPhavg, 6, 3, 1, 1)
        self.ckWatertempavg = QtGui.QCheckBox(self.groupBox)
        self.ckWatertempavg.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckWatertempavg.setObjectName(_fromUtf8("ckWatertempavg"))
        self.gridLayout_2.addWidget(self.ckWatertempavg, 5, 3, 1, 1)
        self.lnedTurbidityunits = QtGui.QLineEdit(self.groupBox)
        self.lnedTurbidityunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedTurbidityunits.setObjectName(_fromUtf8("lnedTurbidityunits"))
        self.gridLayout_2.addWidget(self.lnedTurbidityunits, 8, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.lnedPhmin = QtGui.QLineEdit(self.groupBox)
        self.lnedPhmin.setObjectName(_fromUtf8("lnedPhmin"))
        self.gridLayout_2.addWidget(self.lnedPhmin, 6, 6, 1, 1)
        self.lnedPrecipmax = QtGui.QLineEdit(self.groupBox)
        self.lnedPrecipmax.setObjectName(_fromUtf8("lnedPrecipmax"))
        self.gridLayout_2.addWidget(self.lnedPrecipmax, 2, 4, 1, 1)
        self.lnedPhmax = QtGui.QLineEdit(self.groupBox)
        self.lnedPhmax.setObjectName(_fromUtf8("lnedPhmax"))
        self.gridLayout_2.addWidget(self.lnedPhmax, 6, 4, 1, 1)
        self.ckPrecipavg = QtGui.QCheckBox(self.groupBox)
        self.ckPrecipavg.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckPrecipavg.setObjectName(_fromUtf8("ckPrecipavg"))
        self.gridLayout_2.addWidget(self.ckPrecipavg, 2, 3, 1, 1)
        self.lnedWwatertempunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedWwatertempunits.sizePolicy().hasHeightForWidth())
        self.lnedWwatertempunits.setSizePolicy(sizePolicy)
        self.lnedWwatertempunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedWwatertempunits.setObjectName(_fromUtf8("lnedWwatertempunits"))
        self.gridLayout_2.addWidget(self.lnedWwatertempunits, 5, 1, 1, 1)
        self.ckCondavg = QtGui.QCheckBox(self.groupBox)
        self.ckCondavg.setObjectName(_fromUtf8("ckCondavg"))
        self.gridLayout_2.addWidget(self.ckCondavg, 7, 3, 1, 1)
        self.lnedCovavg = QtGui.QLineEdit(self.groupBox)
        self.lnedCovavg.setObjectName(_fromUtf8("lnedCovavg"))
        self.gridLayout_2.addWidget(self.lnedCovavg, 9, 2, 1, 1)
        self.lnedCondmax = QtGui.QLineEdit(self.groupBox)
        self.lnedCondmax.setObjectName(_fromUtf8("lnedCondmax"))
        self.gridLayout_2.addWidget(self.lnedCondmax, 7, 4, 1, 1)
        self.ckAiravg = QtGui.QCheckBox(self.groupBox)
        self.ckAiravg.setObjectName(_fromUtf8("ckAiravg"))
        self.gridLayout_2.addWidget(self.ckAiravg, 1, 3, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_2.addWidget(self.label_14, 0, 6, 1, 1)
        self.lnedAirunits = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedAirunits.sizePolicy().hasHeightForWidth())
        self.lnedAirunits.setSizePolicy(sizePolicy)
        self.lnedAirunits.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedAirunits.setObjectName(_fromUtf8("lnedAirunits"))
        self.gridLayout_2.addWidget(self.lnedAirunits, 1, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 0, 4, 1, 1)
        self.lnedWindavg = QtGui.QLineEdit(self.groupBox)
        self.lnedWindavg.setObjectName(_fromUtf8("lnedWindavg"))
        self.gridLayout_2.addWidget(self.lnedWindavg, 3, 2, 1, 1)
        self.lnedPhavg = QtGui.QLineEdit(self.groupBox)
        self.lnedPhavg.setObjectName(_fromUtf8("lnedPhavg"))
        self.gridLayout_2.addWidget(self.lnedPhavg, 6, 2, 1, 1)
        self.lnedLightavg = QtGui.QLineEdit(self.groupBox)
        self.lnedLightavg.setObjectName(_fromUtf8("lnedLightavg"))
        self.gridLayout_2.addWidget(self.lnedLightavg, 4, 2, 1, 1)
        self.lnedWindmin = QtGui.QLineEdit(self.groupBox)
        self.lnedWindmin.setObjectName(_fromUtf8("lnedWindmin"))
        self.gridLayout_2.addWidget(self.lnedWindmin, 3, 6, 1, 1)
        self.lnedLightmax = QtGui.QLineEdit(self.groupBox)
        self.lnedLightmax.setObjectName(_fromUtf8("lnedLightmax"))
        self.gridLayout_2.addWidget(self.lnedLightmax, 4, 4, 1, 1)
        self.ckWatertempmax = QtGui.QCheckBox(self.groupBox)
        self.ckWatertempmax.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckWatertempmax.setObjectName(_fromUtf8("ckWatertempmax"))
        self.gridLayout_2.addWidget(self.ckWatertempmax, 5, 5, 1, 1)
        self.ckLightmax = QtGui.QCheckBox(self.groupBox)
        self.ckLightmax.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckLightmax.setObjectName(_fromUtf8("ckLightmax"))
        self.gridLayout_2.addWidget(self.ckLightmax, 4, 5, 1, 1)
        self.ckLightmin = QtGui.QCheckBox(self.groupBox)
        self.ckLightmin.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ckLightmin.setObjectName(_fromUtf8("ckLightmin"))
        self.gridLayout_2.addWidget(self.ckLightmin, 4, 7, 1, 1)
        self.lnedAirmin = QtGui.QLineEdit(self.groupBox)
        self.lnedAirmin.setObjectName(_fromUtf8("lnedAirmin"))
        self.gridLayout_2.addWidget(self.lnedAirmin, 1, 6, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lnedWatertempmin = QtGui.QLineEdit(self.groupBox)
        self.lnedWatertempmin.setObjectName(_fromUtf8("lnedWatertempmin"))
        self.gridLayout_2.addWidget(self.lnedWatertempmin, 5, 6, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 0, 2, 1, 1)
        self.lnedAiravg = QtGui.QLineEdit(self.groupBox)
        self.lnedAiravg.setObjectName(_fromUtf8("lnedAiravg"))
        self.gridLayout_2.addWidget(self.lnedAiravg, 1, 2, 1, 1)
        self.lnedTurbiditymax = QtGui.QLineEdit(self.groupBox)
        self.lnedTurbiditymax.setObjectName(_fromUtf8("lnedTurbiditymax"))
        self.gridLayout_2.addWidget(self.lnedTurbiditymax, 8, 4, 1, 1)
        self.lnedTurbiditymin = QtGui.QLineEdit(self.groupBox)
        self.lnedTurbiditymin.setObjectName(_fromUtf8("lnedTurbiditymin"))
        self.gridLayout_2.addWidget(self.lnedTurbiditymin, 8, 6, 1, 1)
        self.ckTurbiditymax = QtGui.QCheckBox(self.groupBox)
        self.ckTurbiditymax.setObjectName(_fromUtf8("ckTurbiditymax"))
        self.gridLayout_2.addWidget(self.ckTurbiditymax, 8, 5, 1, 1)
        self.ckTurbiditymin = QtGui.QCheckBox(self.groupBox)
        self.ckTurbiditymin.setObjectName(_fromUtf8("ckTurbiditymin"))
        self.gridLayout_2.addWidget(self.ckTurbiditymin, 8, 7, 1, 1)
        self.ckCovavg = QtGui.QCheckBox(self.groupBox)
        self.ckCovavg.setObjectName(_fromUtf8("ckCovavg"))
        self.gridLayout_2.addWidget(self.ckCovavg, 9, 3, 1, 1)
        self.ckCovmax = QtGui.QCheckBox(self.groupBox)
        self.ckCovmax.setObjectName(_fromUtf8("ckCovmax"))
        self.gridLayout_2.addWidget(self.ckCovmax, 9, 5, 1, 1)
        self.ckCovmin = QtGui.QCheckBox(self.groupBox)
        self.ckCovmin.setObjectName(_fromUtf8("ckCovmin"))
        self.gridLayout_2.addWidget(self.ckCovmin, 9, 7, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_2.addWidget(self.label_16, 8, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.btnPreview = QtGui.QPushButton(self.layoutWidget)
        self.btnPreview.setObjectName(_fromUtf8("btnPreview"))
        self.horizontalLayout_7.addWidget(self.btnPreview)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnSaveClose = QtGui.QPushButton(self.layoutWidget)
        self.btnSaveClose.setObjectName(_fromUtf8("btnSaveClose"))
        self.horizontalLayout.addWidget(self.btnSaveClose)
        self.btnCancel = QtGui.QPushButton(self.layoutWidget)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout.addWidget(self.btnCancel)
        self.horizontalLayout_7.addLayout(self.horizontalLayout)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lnedTitle, self.lnedMetarecordid)
        Form.setTabOrder(self.lnedMetarecordid, self.rbtnAggregate)
        Form.setTabOrder(self.rbtnAggregate, self.rbtNoaggregate)
        Form.setTabOrder(self.rbtNoaggregate, self.btnDateformat)
        Form.setTabOrder(self.btnDateformat, self.lnedAirunits)
        Form.setTabOrder(self.lnedAirunits, self.lnedAiravg)
        Form.setTabOrder(self.lnedAiravg, self.ckAiravg)
        Form.setTabOrder(self.ckAiravg, self.lnedAirmax)
        Form.setTabOrder(self.lnedAirmax, self.ckAirmax)
        Form.setTabOrder(self.ckAirmax, self.lnedAirmin)
        Form.setTabOrder(self.lnedAirmin, self.ckAirmin)
        Form.setTabOrder(self.ckAirmin, self.lnedPrecipunits)
        Form.setTabOrder(self.lnedPrecipunits, self.lnedPrecipavg)
        Form.setTabOrder(self.lnedPrecipavg, self.ckPrecipavg)
        Form.setTabOrder(self.ckPrecipavg, self.lnedPrecipmax)
        Form.setTabOrder(self.lnedPrecipmax, self.ckPrecipmax)
        Form.setTabOrder(self.ckPrecipmax, self.lnedPrecipmin)
        Form.setTabOrder(self.lnedPrecipmin, self.ckPrecipmin)
        Form.setTabOrder(self.ckPrecipmin, self.lnedWindunits)
        Form.setTabOrder(self.lnedWindunits, self.lnedWindavg)
        Form.setTabOrder(self.lnedWindavg, self.ckWindavg)
        Form.setTabOrder(self.ckWindavg, self.lnedWindmax)
        Form.setTabOrder(self.lnedWindmax, self.ckWindmax)
        Form.setTabOrder(self.ckWindmax, self.lnedWindmin)
        Form.setTabOrder(self.lnedWindmin, self.ckWindmin)
        Form.setTabOrder(self.ckWindmin, self.lnedLightunits)
        Form.setTabOrder(self.lnedLightunits, self.lnedLightavg)
        Form.setTabOrder(self.lnedLightavg, self.ckLightavg)
        Form.setTabOrder(self.ckLightavg, self.lnedLightmax)
        Form.setTabOrder(self.lnedLightmax, self.ckLightmax)
        Form.setTabOrder(self.ckLightmax, self.lnedLightmin)
        Form.setTabOrder(self.lnedLightmin, self.ckLightmin)
        Form.setTabOrder(self.ckLightmin, self.lnedWwatertempunits)
        Form.setTabOrder(self.lnedWwatertempunits, self.lnedWatertempavg)
        Form.setTabOrder(self.lnedWatertempavg, self.ckWatertempavg)
        Form.setTabOrder(self.ckWatertempavg, self.lnedWatertempmax)
        Form.setTabOrder(self.lnedWatertempmax, self.ckWatertempmax)
        Form.setTabOrder(self.ckWatertempmax, self.lnedWatertempmin)
        Form.setTabOrder(self.lnedWatertempmin, self.ckWatertempmin)
        Form.setTabOrder(self.ckWatertempmin, self.lnedPhunits)
        Form.setTabOrder(self.lnedPhunits, self.lnedPhavg)
        Form.setTabOrder(self.lnedPhavg, self.ckPhavg)
        Form.setTabOrder(self.ckPhavg, self.lnedPhmax)
        Form.setTabOrder(self.lnedPhmax, self.ckPhmax)
        Form.setTabOrder(self.ckPhmax, self.lnedPhmin)
        Form.setTabOrder(self.lnedPhmin, self.ckPhmin)
        Form.setTabOrder(self.ckPhmin, self.lnedCondunits)
        Form.setTabOrder(self.lnedCondunits, self.lnedCondavg)
        Form.setTabOrder(self.lnedCondavg, self.ckCondavg)
        Form.setTabOrder(self.ckCondavg, self.lnedCondmax)
        Form.setTabOrder(self.lnedCondmax, self.ckCondmax)
        Form.setTabOrder(self.ckCondmax, self.lnedCondmin)
        Form.setTabOrder(self.lnedCondmin, self.ckCondmin)
        Form.setTabOrder(self.ckCondmin, self.lnedTurbidityunits)
        Form.setTabOrder(self.lnedTurbidityunits, self.lnedTurbidityavg)
        Form.setTabOrder(self.lnedTurbidityavg, self.ckTurbidityavg)
        Form.setTabOrder(self.ckTurbidityavg, self.lnedTurbiditymax)
        Form.setTabOrder(self.lnedTurbiditymax, self.ckTurbiditymax)
        Form.setTabOrder(self.ckTurbiditymax, self.lnedTurbiditymin)
        Form.setTabOrder(self.lnedTurbiditymin, self.ckTurbiditymin)
        Form.setTabOrder(self.ckTurbiditymin, self.lnedCovunits)
        Form.setTabOrder(self.lnedCovunits, self.lnedCovavg)
        Form.setTabOrder(self.lnedCovavg, self.ckCovavg)
        Form.setTabOrder(self.ckCovavg, self.lnedCovmax)
        Form.setTabOrder(self.lnedCovmax, self.ckCovmax)
        Form.setTabOrder(self.ckCovmax, self.lnedCovmin)
        Form.setTabOrder(self.lnedCovmin, self.ckCovmin)
        Form.setTabOrder(self.ckCovmin, self.btnPreview)
        Form.setTabOrder(self.btnPreview, self.btnSaveClose)
        Form.setTabOrder(self.btnSaveClose, self.btnCancel)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Climate Observations", None))
        self.label_10.setText(_translate("Form", "Dataset Title", None))
        self.label_11.setText(_translate("Form", "Metarecord ID", None))
        self.rbtnAggregate.setText(_translate("Form", "Aggregate Records", None))
        self.rbtNoaggregate.setText(_translate("Form", "Daily Records Present", None))
        self.btnDateformat.setText(_translate("Form", "Format Date Columns", None))
        self.ckWatertempmin.setText(_translate("Form", "No Min. Water Temp", None))
        self.ckAirmin.setText(_translate("Form", "No Min. Air Temp", None))
        self.label_8.setText(_translate("Form", "Covariates", None))
        self.ckAirmax.setText(_translate("Form", "No Max. Air Temp", None))
        self.ckCondmin.setText(_translate("Form", "No Min. Cond.", None))
        self.ckWindmax.setText(_translate("Form", "No Max. Wind", None))
        self.ckTurbidityavg.setText(_translate("Form", "No Avg. Turbidity", None))
        self.ckLightavg.setText(_translate("Form", "No Avg. Irradiance", None))
        self.lnedPhunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.ckCondmax.setText(_translate("Form", "No Max. Cond.", None))
        self.ckPrecipmin.setText(_translate("Form", "No Min. Precip", None))
        self.lnedCovunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.label_9.setText(_translate("Form", "Conductivity", None))
        self.ckWindmin.setText(_translate("Form", "No Min. Wind", None))
        self.label_6.setText(_translate("Form", "Water Temperature", None))
        self.ckPrecipmax.setText(_translate("Form", "No Max. Precip", None))
        self.lnedWindunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.ckPhmax.setText(_translate("Form", "No Max. pH", None))
        self.label_7.setText(_translate("Form", "pH", None))
        self.lnedPrecipunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.label_4.setText(_translate("Form", "Wind", None))
        self.label_2.setText(_translate("Form", "Air Temperature", None))
        self.lnedLightunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.lnedCondunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.ckWindavg.setText(_translate("Form", "No Avg. Wind", None))
        self.ckPhmin.setText(_translate("Form", "No Min. pH", None))
        self.label_3.setText(_translate("Form", "Precipitation", None))
        self.ckPhavg.setText(_translate("Form", "No Avg. pH", None))
        self.ckWatertempavg.setText(_translate("Form", "No Avg. Water Temp", None))
        self.lnedTurbidityunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.label_5.setText(_translate("Form", "Irradiance (light)", None))
        self.ckPrecipavg.setText(_translate("Form", "No Avg. Precip", None))
        self.lnedWwatertempunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.ckCondavg.setText(_translate("Form", "No Avg. Cond.", None))
        self.ckAiravg.setText(_translate("Form", "No Avg. Air Temp", None))
        self.label_14.setText(_translate("Form", "Minimum Values", None))
        self.lnedAirunits.setPlaceholderText(_translate("Form", "Enter Units", None))
        self.label_13.setText(_translate("Form", "Maximum Values", None))
        self.ckWatertempmax.setText(_translate("Form", "No Max. Water Temp", None))
        self.ckLightmax.setText(_translate("Form", "No Max. irradiance", None))
        self.ckLightmin.setText(_translate("Form", "No Min. Irradiance", None))
        self.label.setText(_translate("Form", "Columns", None))
        self.label_12.setText(_translate("Form", "Averages", None))
        self.ckTurbiditymax.setText(_translate("Form", "No Max. Turbidity", None))
        self.ckTurbiditymin.setText(_translate("Form", "No Min. Turbidity", None))
        self.ckCovavg.setText(_translate("Form", "No Covariate Avgs", None))
        self.ckCovmax.setText(_translate("Form", "No Covariate Max.\'s", None))
        self.ckCovmin.setText(_translate("Form", "No Covariate Min.\'s", None))
        self.label_16.setText(_translate("Form", "Turbidity", None))
        self.btnPreview.setText(_translate("Form", "Preview", None))
        self.btnSaveClose.setText(_translate("Form", "Save && Close", None))
        self.btnCancel.setText(_translate("Form", "Cancel", None))
