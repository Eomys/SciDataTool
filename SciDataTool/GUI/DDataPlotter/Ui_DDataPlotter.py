# -*- coding: utf-8 -*-

# File generated according to DDataPlotter.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from SciDataTool.GUI.WPlotManager.WPlotManager import WPlotManager


class Ui_DDataPlotter(object):
    def setupUi(self, DDataPlotter):
        if not DDataPlotter.objectName():
            DDataPlotter.setObjectName("DDataPlotter")
        DDataPlotter.setEnabled(True)
        DDataPlotter.resize(1246, 884)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DDataPlotter.sizePolicy().hasHeightForWidth())
        DDataPlotter.setSizePolicy(sizePolicy)
        DDataPlotter.setCursor(QCursor(Qt.ArrowCursor))
        self.gridLayout = QGridLayout(DDataPlotter)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.is_auto_refresh = QCheckBox(DDataPlotter)
        self.is_auto_refresh.setObjectName("is_auto_refresh")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.is_auto_refresh.sizePolicy().hasHeightForWidth()
        )
        self.is_auto_refresh.setSizePolicy(sizePolicy1)
        self.is_auto_refresh.setMinimumSize(QSize(0, 24))
        self.is_auto_refresh.setMaximumSize(QSize(16777215, 24))
        self.is_auto_refresh.setChecked(False)

        self.horizontalLayout_2.addWidget(self.is_auto_refresh)

        self.b_refresh = QPushButton(DDataPlotter)
        self.b_refresh.setObjectName("b_refresh")
        self.b_refresh.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy1)
        self.b_refresh.setMinimumSize(QSize(0, 0))
        self.b_refresh.setMaximumSize(QSize(16777215, 16777215))
        self.b_refresh.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_2.addWidget(self.b_refresh)

        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.w_scroll = QScrollArea(DDataPlotter)
        self.w_scroll.setObjectName("w_scroll")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.w_scroll.sizePolicy().hasHeightForWidth())
        self.w_scroll.setSizePolicy(sizePolicy2)
        self.w_scroll.setMinimumSize(QSize(200, 0))
        self.w_scroll.setMaximumSize(QSize(400, 16777215))
        self.w_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.w_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 398, 823))
        self.lay_scroll = QVBoxLayout(self.scrollAreaWidgetContents)
        self.lay_scroll.setObjectName("lay_scroll")
        self.lay_scroll.setContentsMargins(0, 0, 0, 0)
        self.w_plot_manager = WPlotManager(self.scrollAreaWidgetContents)
        self.w_plot_manager.setObjectName("w_plot_manager")
        sizePolicy1.setHeightForWidth(
            self.w_plot_manager.sizePolicy().hasHeightForWidth()
        )
        self.w_plot_manager.setSizePolicy(sizePolicy1)
        self.w_plot_manager.setMinimumSize(QSize(0, 0))

        self.lay_scroll.addWidget(self.w_plot_manager)

        self.w_scroll.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.w_scroll, 0, 1, 1, 1)

        self.plot_layout = QVBoxLayout()
        self.plot_layout.setObjectName("plot_layout")

        self.gridLayout.addLayout(self.plot_layout, 0, 0, 2, 1)

        self.retranslateUi(DDataPlotter)

        QMetaObject.connectSlotsByName(DDataPlotter)

    # setupUi

    def retranslateUi(self, DDataPlotter):
        DDataPlotter.setWindowTitle(
            QCoreApplication.translate("DDataPlotter", "Data Plot", None)
        )
        self.is_auto_refresh.setText(
            QCoreApplication.translate("DDataPlotter", "Auto Refresh", None)
        )
        self.b_refresh.setText(
            QCoreApplication.translate("DDataPlotter", "Refresh", None)
        )

    # retranslateUi
