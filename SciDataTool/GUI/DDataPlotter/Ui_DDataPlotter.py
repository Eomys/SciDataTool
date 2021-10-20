# -*- coding: utf-8 -*-

# File generated according to DDataPlotter.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ...GUI.WAxisSelector.WAxisSelector import WAxisSelector
from ...GUI.WDataRange.WDataRange import WDataRange
from ...GUI.WExport.WExport import WExport


class Ui_DDataPlotter(object):
    def setupUi(self, DDataPlotter):
        if not DDataPlotter.objectName():
            DDataPlotter.setObjectName(u"DDataPlotter")
        DDataPlotter.resize(798, 523)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 318, 499))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.g_range = QGroupBox(self.scrollAreaWidgetContents)
        self.g_range.setObjectName(u"g_range")
        self.g_range.setMinimumSize(QSize(296, 0))
        self.g_range.setMaximumSize(QSize(296, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.g_range)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.w_range = WDataRange(self.g_range)
        self.w_range.setObjectName(u"w_range")

        self.verticalLayout_3.addWidget(self.w_range)


        self.gridLayout.addWidget(self.g_range, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 153, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.g_axes = QGroupBox(self.scrollAreaWidgetContents)
        self.g_axes.setObjectName(u"g_axes")
        self.g_axes.setMinimumSize(QSize(296, 0))
        self.g_axes.setMaximumSize(QSize(296, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.g_axes)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.w_axis_1 = WAxisSelector(self.g_axes)
        self.w_axis_1.setObjectName(u"w_axis_1")

        self.verticalLayout_2.addWidget(self.w_axis_1)

        self.w_axis_2 = WAxisSelector(self.g_axes)
        self.w_axis_2.setObjectName(u"w_axis_2")

        self.verticalLayout_2.addWidget(self.w_axis_2)


        self.gridLayout.addWidget(self.g_axes, 0, 0, 1, 1)

        self.w_export = WExport(self.scrollAreaWidgetContents)
        self.w_export.setObjectName(u"w_export")
        self.w_export.setMinimumSize(QSize(296, 0))

        self.gridLayout.addWidget(self.w_export, 5, 0, 1, 1)

        self.refresh_layout = QHBoxLayout()
        self.refresh_layout.setObjectName(u"refresh_layout")
        self.refresh_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(182, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.refresh_layout.addItem(self.horizontalSpacer)

        self.b_refresh = QPushButton(self.scrollAreaWidgetContents)
        self.b_refresh.setObjectName(u"b_refresh")
        self.b_refresh.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy)
        self.b_refresh.setMinimumSize(QSize(93, 0))
        self.b_refresh.setMaximumSize(QSize(93, 16777215))

        self.refresh_layout.addWidget(self.b_refresh)


        self.gridLayout.addLayout(self.refresh_layout, 4, 0, 1, 1)

        self.g_data_extract = QGroupBox(self.scrollAreaWidgetContents)
        self.g_data_extract.setObjectName(u"g_data_extract")
        self.g_data_extract.setMinimumSize(QSize(296, 0))
        self.g_data_extract.setMaximumSize(QSize(296, 16777215))

        self.gridLayout.addWidget(self.g_data_extract, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.retranslateUi(DDataPlotter)

        QMetaObject.connectSlotsByName(DDataPlotter)
    # setupUi

    def retranslateUi(self, DDataPlotter):
        DDataPlotter.setWindowTitle(QCoreApplication.translate("DDataPlotter", u"Data Plot", None))
        self.g_range.setTitle(QCoreApplication.translate("DDataPlotter", u"Output Range", None))
        self.g_axes.setTitle(QCoreApplication.translate("DDataPlotter", u"Axes", None))
        self.b_refresh.setText(QCoreApplication.translate("DDataPlotter", u"Refresh", None))
        self.g_data_extract.setTitle(QCoreApplication.translate("DDataPlotter", u"Data Selection", None))
    # retranslateUi

