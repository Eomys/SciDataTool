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
from ...GUI.WVectorSelector.WVectorSelector import WVectorSelector


class Ui_DDataPlotter(object):
    def setupUi(self, DDataPlotter):
        if not DDataPlotter.objectName():
            DDataPlotter.setObjectName(u"DDataPlotter")
        DDataPlotter.resize(879, 794)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -18, 318, 797))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.w_vect_selector = WVectorSelector(self.scrollAreaWidgetContents)
        self.w_vect_selector.setObjectName(u"w_vect_selector")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_vect_selector.sizePolicy().hasHeightForWidth())
        self.w_vect_selector.setSizePolicy(sizePolicy)
        self.w_vect_selector.setMinimumSize(QSize(0, 70))
        self.w_vect_selector.setMaximumSize(QSize(296, 70))

        self.verticalLayout.addWidget(self.w_vect_selector)

        self.w_axis_manager = WAxisManager(self.scrollAreaWidgetContents)
        self.w_axis_manager.setObjectName(u"w_axis_manager")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_axis_manager.sizePolicy().hasHeightForWidth())
        self.w_axis_manager.setSizePolicy(sizePolicy1)
        self.w_axis_manager.setMinimumSize(QSize(296, 420))
        self.w_axis_manager.setMaximumSize(QSize(296, 16777215))

        self.verticalLayout.addWidget(self.w_axis_manager)

        self.g_range = QGroupBox(self.scrollAreaWidgetContents)
        self.g_range.setObjectName(u"g_range")
        sizePolicy1.setHeightForWidth(self.g_range.sizePolicy().hasHeightForWidth())
        self.g_range.setSizePolicy(sizePolicy1)
        self.g_range.setMinimumSize(QSize(296, 120))
        self.g_range.setMaximumSize(QSize(296, 120))
        self.verticalLayout_3 = QVBoxLayout(self.g_range)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.w_range = WDataRange(self.g_range)
        self.w_range.setObjectName(u"w_range")
        self.w_range.setMinimumSize(QSize(0, 60))

        self.verticalLayout_3.addWidget(self.w_range)


        self.verticalLayout.addWidget(self.g_range)

        self.verticalSpacer = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.refresh_layout = QHBoxLayout()
        self.refresh_layout.setObjectName(u"refresh_layout")
        self.refresh_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(182, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.refresh_layout.addItem(self.horizontalSpacer)

        self.b_refresh = QPushButton(self.scrollAreaWidgetContents)
        self.b_refresh.setObjectName(u"b_refresh")
        self.b_refresh.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy2)
        self.b_refresh.setMinimumSize(QSize(93, 0))
        self.b_refresh.setMaximumSize(QSize(93, 30))

        self.refresh_layout.addWidget(self.b_refresh)


        self.verticalLayout.addLayout(self.refresh_layout)

        self.w_export = WExport(self.scrollAreaWidgetContents)
        self.w_export.setObjectName(u"w_export")
        self.w_export.setMinimumSize(QSize(296, 0))

        self.verticalLayout.addWidget(self.w_export)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.g_range.raise_()
        self.w_axis_manager.raise_()
        self.w_export.raise_()
        self.w_vect_selector.raise_()

        self.horizontalLayout.addWidget(self.scrollArea)


        self.retranslateUi(DDataPlotter)

        QMetaObject.connectSlotsByName(DDataPlotter)
    # setupUi

    def retranslateUi(self, DDataPlotter):
        DDataPlotter.setWindowTitle(QCoreApplication.translate("DDataPlotter", u"Data Plot", None))
        self.g_range.setTitle(QCoreApplication.translate("DDataPlotter", u"Output Range", None))
        self.b_refresh.setText(QCoreApplication.translate("DDataPlotter", u"Refresh", None))
    # retranslateUi

