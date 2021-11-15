# -*- coding: utf-8 -*-

# File generated according to WAxisSelector.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_WAxisSelector(object):
    def setupUi(self, WAxisSelector):
        if not WAxisSelector.objectName():
            WAxisSelector.setObjectName(u"WAxisSelector")
        WAxisSelector.resize(428, 109)
        self.horizontalLayout = QHBoxLayout(WAxisSelector)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.in_name = QLabel(WAxisSelector)
        self.in_name.setObjectName(u"in_name")

        self.horizontalLayout.addWidget(self.in_name)

        self.c_axis = QComboBox(WAxisSelector)
        self.c_axis.addItem("")
        self.c_axis.addItem("")
        self.c_axis.addItem("")
        self.c_axis.addItem("")
        self.c_axis.addItem("")
        self.c_axis.setObjectName(u"c_axis")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_axis.sizePolicy().hasHeightForWidth())
        self.c_axis.setSizePolicy(sizePolicy)
        self.c_axis.setMinimumSize(QSize(50, 0))
        self.c_axis.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.c_axis)

        self.c_action = QComboBox(WAxisSelector)
        self.c_action.addItem("")
        self.c_action.addItem("")
        self.c_action.addItem("")
        self.c_action.setObjectName(u"c_action")
        self.c_action.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.c_action)

        self.c_unit = QComboBox(WAxisSelector)
        self.c_unit.setObjectName(u"c_unit")
        sizePolicy.setHeightForWidth(self.c_unit.sizePolicy().hasHeightForWidth())
        self.c_unit.setSizePolicy(sizePolicy)
        self.c_unit.setMinimumSize(QSize(35, 0))
        self.c_unit.setMaximumSize(QSize(35, 16777215))

        self.horizontalLayout.addWidget(self.c_unit)

        self.b_filter = QPushButton(WAxisSelector)
        self.b_filter.setObjectName(u"b_filter")

        self.horizontalLayout.addWidget(self.b_filter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.retranslateUi(WAxisSelector)

        QMetaObject.connectSlotsByName(WAxisSelector)
    # setupUi

    def retranslateUi(self, WAxisSelector):
        WAxisSelector.setWindowTitle("")
        self.in_name.setText(QCoreApplication.translate("WAxisSelector", u"x", None))
        self.c_axis.setItemText(0, QCoreApplication.translate("WAxisSelector", u"time", None))
        self.c_axis.setItemText(1, QCoreApplication.translate("WAxisSelector", u"angle", None))
        self.c_axis.setItemText(2, QCoreApplication.translate("WAxisSelector", u"axial direction", None))
        self.c_axis.setItemText(3, QCoreApplication.translate("WAxisSelector", u"frequency", None))
        self.c_axis.setItemText(4, QCoreApplication.translate("WAxisSelector", u"wavenumber", None))

        self.c_action.setItemText(0, QCoreApplication.translate("WAxisSelector", u"None", None))
        self.c_action.setItemText(1, QCoreApplication.translate("WAxisSelector", u"FFT", None))
        self.c_action.setItemText(2, QCoreApplication.translate("WAxisSelector", u"Filter", None))

        self.b_filter.setText(QCoreApplication.translate("WAxisSelector", u"Filter", None))
    # retranslateUi

