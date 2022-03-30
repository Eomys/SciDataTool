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
            WAxisSelector.setObjectName("WAxisSelector")
        WAxisSelector.resize(152, 160)
        self.verticalLayout = QVBoxLayout(WAxisSelector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.in_name = QLabel(WAxisSelector)
        self.in_name.setObjectName("in_name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.in_name.sizePolicy().hasHeightForWidth())
        self.in_name.setSizePolicy(sizePolicy)
        self.in_name.setMinimumSize(QSize(0, 0))
        self.in_name.setMaximumSize(QSize(16777215, 16777215))
        self.in_name.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.in_name)

        self.c_axis = QComboBox(WAxisSelector)
        self.c_axis.setObjectName("c_axis")
        sizePolicy.setHeightForWidth(self.c_axis.sizePolicy().hasHeightForWidth())
        self.c_axis.setSizePolicy(sizePolicy)
        self.c_axis.setMinimumSize(QSize(0, 0))
        self.c_axis.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.c_axis)

        self.c_action = QComboBox(WAxisSelector)
        self.c_action.addItem("")
        self.c_action.addItem("")
        self.c_action.addItem("")
        self.c_action.setObjectName("c_action")
        sizePolicy.setHeightForWidth(self.c_action.sizePolicy().hasHeightForWidth())
        self.c_action.setSizePolicy(sizePolicy)
        self.c_action.setMinimumSize(QSize(0, 0))
        self.c_action.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.c_action)

        self.c_unit = QComboBox(WAxisSelector)
        self.c_unit.setObjectName("c_unit")
        sizePolicy.setHeightForWidth(self.c_unit.sizePolicy().hasHeightForWidth())
        self.c_unit.setSizePolicy(sizePolicy)
        self.c_unit.setMinimumSize(QSize(0, 0))
        self.c_unit.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.c_unit)

        self.b_filter = QPushButton(WAxisSelector)
        self.b_filter.setObjectName("b_filter")
        sizePolicy.setHeightForWidth(self.b_filter.sizePolicy().hasHeightForWidth())
        self.b_filter.setSizePolicy(sizePolicy)
        self.b_filter.setMinimumSize(QSize(0, 0))
        self.b_filter.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.b_filter)

        self.retranslateUi(WAxisSelector)

        QMetaObject.connectSlotsByName(WAxisSelector)

    # setupUi

    def retranslateUi(self, WAxisSelector):
        WAxisSelector.setWindowTitle("")
        self.in_name.setText(QCoreApplication.translate("WAxisSelector", "X", None))
        self.c_action.setItemText(
            0, QCoreApplication.translate("WAxisSelector", "None", None)
        )
        self.c_action.setItemText(
            1, QCoreApplication.translate("WAxisSelector", "FFT", None)
        )
        self.c_action.setItemText(
            2, QCoreApplication.translate("WAxisSelector", "Filter", None)
        )

        self.b_filter.setText(
            QCoreApplication.translate("WAxisSelector", "Filter", None)
        )

    # retranslateUi
