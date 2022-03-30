# -*- coding: utf-8 -*-

# File generated according to WSliceOperator.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from SciDataTool.GUI.Tools.FloatEdit import FloatEdit
from SciDataTool.GUI.Tools.ButtonLabel import ButtonLabel

from SciDataTool.GUI.Resources import SDT_rc


class Ui_WSliceOperator(object):
    def setupUi(self, WSliceOperator):
        if not WSliceOperator.objectName():
            WSliceOperator.setObjectName("WSliceOperator")
        WSliceOperator.resize(375, 133)
        self.gridLayout = QGridLayout(WSliceOperator)
        self.gridLayout.setObjectName("gridLayout")
        self.b_action = QPushButton(WSliceOperator)
        self.b_action.setObjectName("b_action")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_action.sizePolicy().hasHeightForWidth())
        self.b_action.setSizePolicy(sizePolicy)
        self.b_action.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.b_action, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lf_value = FloatEdit(WSliceOperator)
        self.lf_value.setObjectName("lf_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(70)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lf_value.sizePolicy().hasHeightForWidth())
        self.lf_value.setSizePolicy(sizePolicy1)
        self.lf_value.setMinimumSize(QSize(0, 20))
        self.lf_value.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.lf_value)

        self.in_unit = QLabel(WSliceOperator)
        self.in_unit.setObjectName("in_unit")

        self.horizontalLayout_2.addWidget(self.in_unit)

        self.slider = QSlider(WSliceOperator)
        self.slider.setObjectName("slider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.slider.sizePolicy().hasHeightForWidth())
        self.slider.setSizePolicy(sizePolicy2)
        self.slider.setMinimumSize(QSize(0, 20))
        self.slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider)

        self.b_animate = ButtonLabel(WSliceOperator)
        self.b_animate.setObjectName("b_animate")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.b_animate.sizePolicy().hasHeightForWidth())
        self.b_animate.setSizePolicy(sizePolicy3)
        self.b_animate.setMinimumSize(QSize(20, 20))
        self.b_animate.setMaximumSize(QSize(20, 20))
        self.b_animate.setFrameShadow(QFrame.Sunken)
        self.b_animate.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.b_animate)

        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.in_name = QLabel(WSliceOperator)
        self.in_name.setObjectName("in_name")
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
        self.c_operation.setObjectName("c_operation")
        sizePolicy.setHeightForWidth(self.c_operation.sizePolicy().hasHeightForWidth())
        self.c_operation.setSizePolicy(sizePolicy)
        self.c_operation.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.c_operation)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.l_loading = QLabel(WSliceOperator)
        self.l_loading.setObjectName("l_loading")
        self.l_loading.setEnabled(True)

        self.gridLayout.addWidget(self.l_loading, 3, 0, 1, 1)

        self.retranslateUi(WSliceOperator)

        QMetaObject.connectSlotsByName(WSliceOperator)

    # setupUi

    def retranslateUi(self, WSliceOperator):
        WSliceOperator.setWindowTitle(
            QCoreApplication.translate("WSliceOperator", "WSliceOperator", None)
        )
        self.b_action.setText(
            QCoreApplication.translate("WSliceOperator", "Overlay", None)
        )
        self.lf_value.setText(
            QCoreApplication.translate("WSliceOperator", "0.314", None)
        )
        self.in_unit.setText(QCoreApplication.translate("WSliceOperator", "[m]", None))
        self.b_animate.setText("")
        self.in_name.setText(
            QCoreApplication.translate("WSliceOperator", "angle", None)
        )
        self.c_operation.setItemText(
            0, QCoreApplication.translate("WSliceOperator", "slice", None)
        )
        self.c_operation.setItemText(
            1, QCoreApplication.translate("WSliceOperator", "slice (fft)", None)
        )
        self.c_operation.setItemText(
            2, QCoreApplication.translate("WSliceOperator", "rms", None)
        )
        self.c_operation.setItemText(
            3, QCoreApplication.translate("WSliceOperator", "rss", None)
        )
        self.c_operation.setItemText(
            4, QCoreApplication.translate("WSliceOperator", "sum", None)
        )
        self.c_operation.setItemText(
            5, QCoreApplication.translate("WSliceOperator", "mean", None)
        )
        self.c_operation.setItemText(
            6, QCoreApplication.translate("WSliceOperator", "integrate", None)
        )
        self.c_operation.setItemText(
            7, QCoreApplication.translate("WSliceOperator", "overlay/filter", None)
        )

        self.l_loading.setText(
            QCoreApplication.translate("WSliceOperator", "Generating...", None)
        )

    # retranslateUi
