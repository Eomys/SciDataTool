# -*- coding: utf-8 -*-

# File generated according to WDataRange.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from SciDataTool.GUI.Tools.FloatEdit import FloatEdit


class Ui_WDataRange(object):
    def setupUi(self, WDataRange):
        if not WDataRange.objectName():
            WDataRange.setObjectName("WDataRange")
        WDataRange.resize(300, 132)
        self.verticalLayout = QVBoxLayout(WDataRange)
        self.verticalLayout.setObjectName("verticalLayout")
        self.g_range = QGroupBox(WDataRange)
        self.g_range.setObjectName("g_range")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_range.sizePolicy().hasHeightForWidth())
        self.g_range.setSizePolicy(sizePolicy)
        self.g_range.setMinimumSize(QSize(0, 0))
        self.g_range.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.g_range)
        self.gridLayout.setObjectName("gridLayout")
        self.in_unit = QLabel(self.g_range)
        self.in_unit.setObjectName("in_unit")

        self.gridLayout.addWidget(self.in_unit, 0, 0, 1, 1)

        self.c_unit = QComboBox(self.g_range)
        self.c_unit.setObjectName("c_unit")
        self.c_unit.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.c_unit, 0, 1, 1, 1)

        self.in_min = QLabel(self.g_range)
        self.in_min.setObjectName("in_min")

        self.gridLayout.addWidget(self.in_min, 1, 0, 1, 1)

        self.lf_min = FloatEdit(self.g_range)
        self.lf_min.setObjectName("lf_min")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(70)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lf_min.sizePolicy().hasHeightForWidth())
        self.lf_min.setSizePolicy(sizePolicy1)
        self.lf_min.setMinimumSize(QSize(0, 20))
        self.lf_min.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.lf_min, 1, 1, 1, 1)

        self.in_max = QLabel(self.g_range)
        self.in_max.setObjectName("in_max")

        self.gridLayout.addWidget(self.in_max, 2, 0, 1, 1)

        self.lf_max = FloatEdit(self.g_range)
        self.lf_max.setObjectName("lf_max")
        sizePolicy1.setHeightForWidth(self.lf_max.sizePolicy().hasHeightForWidth())
        self.lf_max.setSizePolicy(sizePolicy1)
        self.lf_max.setMinimumSize(QSize(0, 20))
        self.lf_max.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.lf_max, 2, 1, 1, 1)

        self.verticalLayout.addWidget(self.g_range)

        self.retranslateUi(WDataRange)

        QMetaObject.connectSlotsByName(WDataRange)

    # setupUi

    def retranslateUi(self, WDataRange):
        WDataRange.setWindowTitle("")
        self.g_range.setTitle(QCoreApplication.translate("WDataRange", "Range", None))
        self.in_unit.setText(QCoreApplication.translate("WDataRange", "unit", None))
        self.in_min.setText(QCoreApplication.translate("WDataRange", "min", None))
        self.lf_min.setText(QCoreApplication.translate("WDataRange", "0.314", None))
        self.in_max.setText(QCoreApplication.translate("WDataRange", "max", None))
        self.lf_max.setText(QCoreApplication.translate("WDataRange", "0.314", None))

    # retranslateUi
