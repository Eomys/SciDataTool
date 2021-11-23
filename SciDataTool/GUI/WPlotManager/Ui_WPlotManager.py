# -*- coding: utf-8 -*-

# File generated according to WPlotManager.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ...GUI.WDataRange.WDataRange import WDataRange
from ...GUI.WAxisManager.WAxisManager import WAxisManager
from ...GUI.WVectorSelector.WVectorSelector import WVectorSelector


class Ui_WPlotManager(object):
    def setupUi(self, WPlotManager):
        if not WPlotManager.objectName():
            WPlotManager.setObjectName(u"WPlotManager")
        WPlotManager.resize(342, 683)
        self.horizontalLayout = QHBoxLayout(WPlotManager)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scrollArea = QScrollArea(WPlotManager)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 318, 659))
        self.scrollAreaWidgetContents.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.w_vect_selector = WVectorSelector(self.scrollAreaWidgetContents)
        self.w_vect_selector.setObjectName(u"w_vect_selector")
        sizePolicy.setHeightForWidth(self.w_vect_selector.sizePolicy().hasHeightForWidth())
        self.w_vect_selector.setSizePolicy(sizePolicy)
        self.w_vect_selector.setMinimumSize(QSize(0, 0))
        self.w_vect_selector.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.w_vect_selector)

        self.w_axis_manager = WAxisManager(self.scrollAreaWidgetContents)
        self.w_axis_manager.setObjectName(u"w_axis_manager")
        sizePolicy.setHeightForWidth(self.w_axis_manager.sizePolicy().hasHeightForWidth())
        self.w_axis_manager.setSizePolicy(sizePolicy)
        self.w_axis_manager.setMinimumSize(QSize(0, 0))
        self.w_axis_manager.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.w_axis_manager)

        self.w_range = WDataRange(self.scrollAreaWidgetContents)
        self.w_range.setObjectName(u"w_range")
        sizePolicy.setHeightForWidth(self.w_range.sizePolicy().hasHeightForWidth())
        self.w_range.setSizePolicy(sizePolicy)
        self.w_range.setMinimumSize(QSize(0, 0))
        self.w_range.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.w_range)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(11, 11, 10, 11)
        self.c_auto_refresh = QCheckBox(self.scrollAreaWidgetContents)
        self.c_auto_refresh.setObjectName(u"c_auto_refresh")
        sizePolicy.setHeightForWidth(self.c_auto_refresh.sizePolicy().hasHeightForWidth())
        self.c_auto_refresh.setSizePolicy(sizePolicy)
        self.c_auto_refresh.setMinimumSize(QSize(0, 0))
        self.c_auto_refresh.setMaximumSize(QSize(16777215, 16777215))
        self.c_auto_refresh.setChecked(False)

        self.gridLayout_2.addWidget(self.c_auto_refresh, 0, 0, 1, 1)

        self.b_animate = QPushButton(self.scrollAreaWidgetContents)
        self.b_animate.setObjectName(u"b_animate")
        sizePolicy.setHeightForWidth(self.b_animate.sizePolicy().hasHeightForWidth())
        self.b_animate.setSizePolicy(sizePolicy)
        self.b_animate.setMinimumSize(QSize(0, 0))
        self.b_animate.setMaximumSize(QSize(16777215, 16777215))
        self.b_animate.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_2.addWidget(self.b_animate, 1, 1, 1, 1)

        self.b_export = QPushButton(self.scrollAreaWidgetContents)
        self.b_export.setObjectName(u"b_export")
        sizePolicy.setHeightForWidth(self.b_export.sizePolicy().hasHeightForWidth())
        self.b_export.setSizePolicy(sizePolicy)
        self.b_export.setMinimumSize(QSize(0, 0))
        self.b_export.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_2.addWidget(self.b_export, 2, 1, 1, 1)

        self.b_refresh = QPushButton(self.scrollAreaWidgetContents)
        self.b_refresh.setObjectName(u"b_refresh")
        self.b_refresh.setEnabled(True)
        sizePolicy.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy)
        self.b_refresh.setMinimumSize(QSize(0, 0))
        self.b_refresh.setMaximumSize(QSize(16777215, 16777215))
        self.b_refresh.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_2.addWidget(self.b_refresh, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.retranslateUi(WPlotManager)

        QMetaObject.connectSlotsByName(WPlotManager)
    # setupUi

    def retranslateUi(self, WPlotManager):
        WPlotManager.setWindowTitle(QCoreApplication.translate("WPlotManager", u"WPlotManager", None))
        self.c_auto_refresh.setText(QCoreApplication.translate("WPlotManager", u"Auto Refresh", None))
        self.b_animate.setText(QCoreApplication.translate("WPlotManager", u"Animate", None))
        self.b_export.setText(QCoreApplication.translate("WPlotManager", u"Export", None))
        self.b_refresh.setText(QCoreApplication.translate("WPlotManager", u"Refresh", None))
    # retranslateUi

