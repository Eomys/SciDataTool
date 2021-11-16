# -*- coding: utf-8 -*-

# File generated according to WDataRange.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ...GUI.Tools.FloatEdit import FloatEdit


class Ui_WDataRange(object):
    def setupUi(self, WDataRange):
        if not WDataRange.objectName():
            WDataRange.setObjectName(u"WDataRange")
        WDataRange.resize(164, 96)
        self.gridLayout = QGridLayout(WDataRange)
        self.gridLayout.setObjectName(u"gridLayout")
        self.in_unit = QLabel(WDataRange)
        self.in_unit.setObjectName(u"in_unit")

        self.gridLayout.addWidget(self.in_unit, 0, 0, 1, 1)

        self.c_unit = QComboBox(WDataRange)
        self.c_unit.setObjectName(u"c_unit")
        self.c_unit.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.c_unit, 0, 1, 1, 1)

        self.in_min = QLabel(WDataRange)
        self.in_min.setObjectName(u"in_min")

        self.gridLayout.addWidget(self.in_min, 1, 0, 1, 1)

        self.lf_min = FloatEdit(WDataRange)
        self.lf_min.setObjectName(u"lf_min")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lf_min.sizePolicy().hasHeightForWidth())
        self.lf_min.setSizePolicy(sizePolicy)
        self.lf_min.setMinimumSize(QSize(0, 20))
        self.lf_min.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.lf_min, 1, 1, 1, 1)

        self.in_max = QLabel(WDataRange)
        self.in_max.setObjectName(u"in_max")

        self.gridLayout.addWidget(self.in_max, 2, 0, 1, 1)

        self.lf_max = FloatEdit(WDataRange)
        self.lf_max.setObjectName(u"lf_max")
        sizePolicy.setHeightForWidth(self.lf_max.sizePolicy().hasHeightForWidth())
        self.lf_max.setSizePolicy(sizePolicy)
        self.lf_max.setMinimumSize(QSize(0, 20))
        self.lf_max.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.lf_max, 2, 1, 1, 1)

        self.retranslateUi(WDataRange)

        QMetaObject.connectSlotsByName(WDataRange)

    # setupUi

    def retranslateUi(self, WDataRange):
        WDataRange.setWindowTitle("")
        self.in_unit.setText(QCoreApplication.translate("WDataRange", u"unit", None))
        self.in_min.setText(QCoreApplication.translate("WDataRange", u"min", None))
        self.lf_min.setText(QCoreApplication.translate("WDataRange", u"0.314", None))
        self.in_max.setText(QCoreApplication.translate("WDataRange", u"max", None))
        self.lf_max.setText(QCoreApplication.translate("WDataRange", u"0.314", None))

    # retranslateUi
