# -*- coding: utf-8 -*-

# File generated according to DDataPlotter.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ...GUI.WDataRange.WDataRange import WDataRange
from ...GUI.WExport.WExport import WExport
from ...GUI.WAxisManager.WAxisManager import WAxisManager


class Ui_DDataPlotter(object):
    def setupUi(self, DDataPlotter):
        if not DDataPlotter.objectName():
            DDataPlotter.setObjectName(u"DDataPlotter")
        DDataPlotter.resize(872, 738)
        self.horizontalLayout = QHBoxLayout(DDataPlotter)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plot_layout = QVBoxLayout()
        self.plot_layout.setObjectName(u"plot_layout")

        self.horizontalLayout.addLayout(self.plot_layout)

        self.scrollArea = QScrollArea(DDataPlotter)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(320, 0))
        self.scrollArea.setMaximumSize(QSize(320, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 318, 714))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.in_component = QLabel(self.scrollAreaWidgetContents)
        self.in_component.setObjectName(u"in_component")

        self.horizontalLayout_2.addWidget(self.in_component)

        self.c_component = QComboBox(self.scrollAreaWidgetContents)
        self.c_component.setObjectName(u"c_component")

        self.horizontalLayout_2.addWidget(self.c_component)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.w_axis_manager = WAxisManager(self.scrollAreaWidgetContents)
        self.w_axis_manager.setObjectName(u"w_axis_manager")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_axis_manager.sizePolicy().hasHeightForWidth())
        self.w_axis_manager.setSizePolicy(sizePolicy)
        self.w_axis_manager.setMinimumSize(QSize(296, 450))
        self.w_axis_manager.setMaximumSize(QSize(296, 16777215))

        self.verticalLayout.addWidget(self.w_axis_manager)

        self.g_range = QGroupBox(self.scrollAreaWidgetContents)
        self.g_range.setObjectName(u"g_range")
        self.g_range.setMinimumSize(QSize(296, 0))
        self.g_range.setMaximumSize(QSize(296, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.g_range)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.w_range = WDataRange(self.g_range)
        self.w_range.setObjectName(u"w_range")

        self.verticalLayout_3.addWidget(self.w_range)


        self.verticalLayout.addWidget(self.g_range)

        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.refresh_layout = QHBoxLayout()
        self.refresh_layout.setObjectName(u"refresh_layout")
        self.refresh_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(182, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.refresh_layout.addItem(self.horizontalSpacer)

        self.b_refresh = QPushButton(self.scrollAreaWidgetContents)
        self.b_refresh.setObjectName(u"b_refresh")
        self.b_refresh.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy1)
        self.b_refresh.setMinimumSize(QSize(93, 0))
        self.b_refresh.setMaximumSize(QSize(93, 30))

        self.refresh_layout.addWidget(self.b_refresh)


        self.verticalLayout.addLayout(self.refresh_layout)

        self.w_export = WExport(self.scrollAreaWidgetContents)
        self.w_export.setObjectName(u"w_export")
        self.w_export.setMinimumSize(QSize(296, 0))

        self.verticalLayout.addWidget(self.w_export)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.retranslateUi(DDataPlotter)

        QMetaObject.connectSlotsByName(DDataPlotter)
    # setupUi

    def retranslateUi(self, DDataPlotter):
        DDataPlotter.setWindowTitle(QCoreApplication.translate("DDataPlotter", u"Data Plot", None))
        self.in_component.setText(QCoreApplication.translate("DDataPlotter", u"Component", None))
        self.g_range.setTitle(QCoreApplication.translate("DDataPlotter", u"Output Range", None))
        self.b_refresh.setText(QCoreApplication.translate("DDataPlotter", u"Refresh", None))
    # retranslateUi

