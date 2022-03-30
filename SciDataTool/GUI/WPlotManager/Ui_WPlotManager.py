# -*- coding: utf-8 -*-

# File generated according to WPlotManager.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from SciDataTool.GUI.WDataRange.WDataRange import WDataRange
from SciDataTool.GUI.WAxisManager.WAxisManager import WAxisManager
from SciDataTool.GUI.WVectorSelector.WVectorSelector import WVectorSelector


class Ui_WPlotManager(object):
    def setupUi(self, WPlotManager):
        if not WPlotManager.objectName():
            WPlotManager.setObjectName("WPlotManager")
        WPlotManager.resize(376, 683)
        self.verticalLayout = QVBoxLayout(WPlotManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.w_vect_selector = WVectorSelector(WPlotManager)
        self.w_vect_selector.setObjectName("w_vect_selector")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w_vect_selector.sizePolicy().hasHeightForWidth()
        )
        self.w_vect_selector.setSizePolicy(sizePolicy)
        self.w_vect_selector.setMinimumSize(QSize(0, 0))
        self.w_vect_selector.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.w_vect_selector)

        self.w_axis_manager = WAxisManager(WPlotManager)
        self.w_axis_manager.setObjectName("w_axis_manager")
        sizePolicy.setHeightForWidth(
            self.w_axis_manager.sizePolicy().hasHeightForWidth()
        )
        self.w_axis_manager.setSizePolicy(sizePolicy)
        self.w_axis_manager.setMinimumSize(QSize(0, 0))
        self.w_axis_manager.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.w_axis_manager)

        self.w_range = WDataRange(WPlotManager)
        self.w_range.setObjectName("w_range")
        sizePolicy.setHeightForWidth(self.w_range.sizePolicy().hasHeightForWidth())
        self.w_range.setSizePolicy(sizePolicy)
        self.w_range.setMinimumSize(QSize(0, 0))
        self.w_range.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.w_range)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(11, 11, 10, 11)
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.b_export = QPushButton(WPlotManager)
        self.b_export.setObjectName("b_export")
        sizePolicy.setHeightForWidth(self.b_export.sizePolicy().hasHeightForWidth())
        self.b_export.setSizePolicy(sizePolicy)
        self.b_export.setMinimumSize(QSize(0, 0))
        self.b_export.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_2.addWidget(self.b_export, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(WPlotManager)

        QMetaObject.connectSlotsByName(WPlotManager)

    # setupUi

    def retranslateUi(self, WPlotManager):
        WPlotManager.setWindowTitle(
            QCoreApplication.translate("WPlotManager", "WPlotManager", None)
        )
        self.b_export.setText(
            QCoreApplication.translate("WPlotManager", "Export", None)
        )

    # retranslateUi
