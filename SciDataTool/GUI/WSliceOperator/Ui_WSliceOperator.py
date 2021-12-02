# -*- coding: utf-8 -*-

# File generated according to WSliceOperator.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ...GUI.Tools.FloatEdit import FloatEdit


class Ui_WSliceOperator(object):
    def setupUi(self, WSliceOperator):
        if not WSliceOperator.objectName():
            WSliceOperator.setObjectName(u"WSliceOperator")
        WSliceOperator.resize(318, 100)
        self.verticalLayout = QVBoxLayout(WSliceOperator)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.in_name = QLabel(WSliceOperator)
        self.in_name.setObjectName(u"in_name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.in_name.sizePolicy().hasHeightForWidth())
        self.in_name.setSizePolicy(sizePolicy)
        self.in_name.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.in_name)

        self.c_operation = QComboBox(WSliceOperator)
        self.c_operation.addItem("")
        self.c_operation.addItem("")
        self.c_operation.addItem("")
        self.c_operation.addItem("")
        self.c_operation.addItem("")
        self.c_operation.addItem("")
        self.c_operation.addItem("")
        self.c_operation.addItem("")
        self.c_operation.setObjectName(u"c_operation")
        sizePolicy.setHeightForWidth(self.c_operation.sizePolicy().hasHeightForWidth())
        self.c_operation.setSizePolicy(sizePolicy)
        self.c_operation.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.c_operation)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lf_value = FloatEdit(WSliceOperator)
        self.lf_value.setObjectName(u"lf_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(70)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lf_value.sizePolicy().hasHeightForWidth())
        self.lf_value.setSizePolicy(sizePolicy1)
        self.lf_value.setMinimumSize(QSize(0, 20))
        self.lf_value.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.lf_value)

        self.slider = QSlider(WSliceOperator)
        self.slider.setObjectName(u"slider")
        sizePolicy.setHeightForWidth(self.slider.sizePolicy().hasHeightForWidth())
        self.slider.setSizePolicy(sizePolicy)
        self.slider.setMinimumSize(QSize(0, 20))
        self.slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.b_action = QPushButton(WSliceOperator)
        self.b_action.setObjectName(u"b_action")
        sizePolicy.setHeightForWidth(self.b_action.sizePolicy().hasHeightForWidth())
        self.b_action.setSizePolicy(sizePolicy)
        self.b_action.setMinimumSize(QSize(0, 20))

        self.verticalLayout.addWidget(self.b_action)

        self.retranslateUi(WSliceOperator)

        QMetaObject.connectSlotsByName(WSliceOperator)

    # setupUi

    def retranslateUi(self, WSliceOperator):
        WSliceOperator.setWindowTitle(
            QCoreApplication.translate("WSliceOperator", u"WSliceOperator", None)
        )
        self.in_name.setText(
            QCoreApplication.translate("WSliceOperator", u"angle", None)
        )
        self.c_operation.setItemText(
            0, QCoreApplication.translate("WSliceOperator", u"slice", None)
        )
        self.c_operation.setItemText(
            1, QCoreApplication.translate("WSliceOperator", u"slice (fft)", None)
        )
        self.c_operation.setItemText(
            2, QCoreApplication.translate("WSliceOperator", u"rms", None)
        )
        self.c_operation.setItemText(
            3, QCoreApplication.translate("WSliceOperator", u"rss", None)
        )
        self.c_operation.setItemText(
            4, QCoreApplication.translate("WSliceOperator", u"sum", None)
        )
        self.c_operation.setItemText(
            5, QCoreApplication.translate("WSliceOperator", u"mean", None)
        )
        self.c_operation.setItemText(
            6, QCoreApplication.translate("WSliceOperator", u"integrate", None)
        )
        self.c_operation.setItemText(
            7, QCoreApplication.translate("WSliceOperator", u"overlay/filter", None)
        )

        self.lf_value.setText(
            QCoreApplication.translate("WSliceOperator", u"0.314", None)
        )
        self.b_action.setText(
            QCoreApplication.translate("WSliceOperator", u"Superimpose selection", None)
        )

    # retranslateUi
