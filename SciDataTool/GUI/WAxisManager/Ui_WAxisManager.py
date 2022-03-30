# -*- coding: utf-8 -*-

# File generated according to WAxisManager.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from SciDataTool.GUI.WAxisSelector.WAxisSelector import WAxisSelector


class Ui_WAxisManager(object):
    def setupUi(self, WAxisManager):
        if not WAxisManager.objectName():
            WAxisManager.setObjectName("WAxisManager")
        WAxisManager.resize(461, 266)
        self.verticalLayout_2 = QVBoxLayout(WAxisManager)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.g_axes = QGroupBox(WAxisManager)
        self.g_axes.setObjectName("g_axes")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_axes.sizePolicy().hasHeightForWidth())
        self.g_axes.setSizePolicy(sizePolicy)
        self.g_axes.setMinimumSize(QSize(0, 0))
        self.g_axes.setMaximumSize(QSize(16777215, 16777215))
        self.lay_axes = QHBoxLayout(self.g_axes)
        self.lay_axes.setSpacing(4)
        self.lay_axes.setObjectName("lay_axes")
        self.lay_axes.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.g_axes)
        self.label.setObjectName("label")
        self.label.setMinimumSize(QSize(0, 24))

        self.verticalLayout.addWidget(self.label)

        self.label_4 = QLabel(self.g_axes)
        self.label_4.setObjectName("label_4")
        self.label_4.setMinimumSize(QSize(0, 18))

        self.verticalLayout.addWidget(self.label_4)

        self.label_2 = QLabel(self.g_axes)
        self.label_2.setObjectName("label_2")
        self.label_2.setMinimumSize(QSize(0, 20))

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.g_axes)
        self.label_3.setObjectName("label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(0, 18))

        self.verticalLayout.addWidget(self.label_3)

        self.label_5 = QLabel(self.g_axes)
        self.label_5.setObjectName("label_5")
        self.label_5.setMinimumSize(QSize(0, 23))

        self.verticalLayout.addWidget(self.label_5)

        self.lay_axes.addLayout(self.verticalLayout)

        self.w_axis_1 = WAxisSelector(self.g_axes)
        self.w_axis_1.setObjectName("w_axis_1")
        sizePolicy.setHeightForWidth(self.w_axis_1.sizePolicy().hasHeightForWidth())
        self.w_axis_1.setSizePolicy(sizePolicy)
        self.w_axis_1.setMinimumSize(QSize(150, 0))
        self.w_axis_1.setMaximumSize(QSize(150, 16777215))

        self.lay_axes.addWidget(self.w_axis_1)

        self.w_axis_2 = WAxisSelector(self.g_axes)
        self.w_axis_2.setObjectName("w_axis_2")
        sizePolicy.setHeightForWidth(self.w_axis_2.sizePolicy().hasHeightForWidth())
        self.w_axis_2.setSizePolicy(sizePolicy)
        self.w_axis_2.setMinimumSize(QSize(150, 0))
        self.w_axis_2.setMaximumSize(QSize(150, 16777215))

        self.lay_axes.addWidget(self.w_axis_2)

        self.verticalLayout_2.addWidget(self.g_axes)

        self.g_data_extract = QGroupBox(WAxisManager)
        self.g_data_extract.setObjectName("g_data_extract")
        sizePolicy.setHeightForWidth(
            self.g_data_extract.sizePolicy().hasHeightForWidth()
        )
        self.g_data_extract.setSizePolicy(sizePolicy)
        self.g_data_extract.setMinimumSize(QSize(0, 0))
        self.g_data_extract.setMaximumSize(QSize(16777215, 16777215))
        self.lay_data_extract = QVBoxLayout(self.g_data_extract)
        self.lay_data_extract.setObjectName("lay_data_extract")

        self.verticalLayout_2.addWidget(self.g_data_extract)

        self.retranslateUi(WAxisManager)

        QMetaObject.connectSlotsByName(WAxisManager)

    # setupUi

    def retranslateUi(self, WAxisManager):
        WAxisManager.setWindowTitle(
            QCoreApplication.translate("WAxisManager", "WAxisManager", None)
        )
        self.g_axes.setTitle(
            QCoreApplication.translate("WAxisManager", "Axes Selection", None)
        )
        self.label.setText("")
        self.label_4.setText(QCoreApplication.translate("WAxisManager", "Axis", None))
        self.label_2.setText(QCoreApplication.translate("WAxisManager", "Action", None))
        self.label_3.setText(QCoreApplication.translate("WAxisManager", "Unit", None))
        self.label_5.setText("")
        self.g_data_extract.setTitle(
            QCoreApplication.translate("WAxisManager", "Axes Operations", None)
        )

    # retranslateUi
