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
        DDataPlotter.setEnabled(True)
        DDataPlotter.resize(1102, 811)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DDataPlotter.sizePolicy().hasHeightForWidth())
        DDataPlotter.setSizePolicy(sizePolicy)
        DDataPlotter.setCursor(QCursor(Qt.ArrowCursor))
        self.gridLayout = QGridLayout(DDataPlotter)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = QScrollArea(DDataPlotter)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(320, 0))
        self.scrollArea.setMaximumSize(QSize(320, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 318, 787))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.w_vect_selector = WVectorSelector(self.scrollAreaWidgetContents)
        self.w_vect_selector.setObjectName(u"w_vect_selector")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_vect_selector.sizePolicy().hasHeightForWidth())
        self.w_vect_selector.setSizePolicy(sizePolicy1)
        self.w_vect_selector.setMinimumSize(QSize(296, 100))
        self.w_vect_selector.setMaximumSize(QSize(296, 70))

        self.verticalLayout.addWidget(self.w_vect_selector)

        self.w_axis_manager = WAxisManager(self.scrollAreaWidgetContents)
        self.w_axis_manager.setObjectName(u"w_axis_manager")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.w_axis_manager.sizePolicy().hasHeightForWidth())
        self.w_axis_manager.setSizePolicy(sizePolicy2)
        self.w_axis_manager.setMinimumSize(QSize(296, 360))
        self.w_axis_manager.setMaximumSize(QSize(296, 16777215))

        self.verticalLayout.addWidget(self.w_axis_manager)

        self.w_range = WDataRange(self.scrollAreaWidgetContents)
        self.w_range.setObjectName(u"w_range")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.w_range.sizePolicy().hasHeightForWidth())
        self.w_range.setSizePolicy(sizePolicy3)
        self.w_range.setMinimumSize(QSize(296, 130))
        self.w_range.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout.addWidget(self.w_range)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.b_animate = QPushButton(self.scrollAreaWidgetContents)
        self.b_animate.setObjectName(u"b_animate")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.b_animate.sizePolicy().hasHeightForWidth())
        self.b_animate.setSizePolicy(sizePolicy4)
        self.b_animate.setMinimumSize(QSize(72, 24))
        self.b_animate.setMaximumSize(QSize(72, 24))

        self.gridLayout_2.addWidget(self.b_animate, 1, 1, 1, 1)

        self.c_auto_refresh = QCheckBox(self.scrollAreaWidgetContents)
        self.c_auto_refresh.setObjectName(u"c_auto_refresh")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.c_auto_refresh.sizePolicy().hasHeightForWidth())
        self.c_auto_refresh.setSizePolicy(sizePolicy5)
        self.c_auto_refresh.setMinimumSize(QSize(170, 24))
        self.c_auto_refresh.setMaximumSize(QSize(16777215, 24))
        self.c_auto_refresh.setChecked(False)

        self.gridLayout_2.addWidget(self.c_auto_refresh, 0, 0, 1, 1)

        self.b_refresh = QPushButton(self.scrollAreaWidgetContents)
        self.b_refresh.setObjectName(u"b_refresh")
        self.b_refresh.setEnabled(True)
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy6)
        self.b_refresh.setMinimumSize(QSize(72, 24))
        self.b_refresh.setMaximumSize(QSize(72, 24))
        self.b_refresh.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_2.addWidget(self.b_refresh, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.w_export = WExport(self.scrollAreaWidgetContents)
        self.w_export.setObjectName(u"w_export")
        sizePolicy3.setHeightForWidth(self.w_export.sizePolicy().hasHeightForWidth())
        self.w_export.setSizePolicy(sizePolicy3)
        self.w_export.setMinimumSize(QSize(280, 40))
        self.w_export.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout.addWidget(self.w_export)

        self.vertical_spacer = QSpacerItem(20, 120, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.vertical_spacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.w_axis_manager.raise_()
        self.w_vect_selector.raise_()
        self.w_export.raise_()
        self.w_range.raise_()

        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)

        self.plot_layout = QVBoxLayout()
        self.plot_layout.setObjectName(u"plot_layout")

        self.gridLayout.addLayout(self.plot_layout, 0, 0, 1, 1)


        self.retranslateUi(DDataPlotter)

        QMetaObject.connectSlotsByName(DDataPlotter)
    # setupUi

    def retranslateUi(self, DDataPlotter):
        DDataPlotter.setWindowTitle(QCoreApplication.translate("DDataPlotter", u"Data Plot", None))
        self.b_animate.setText(QCoreApplication.translate("DDataPlotter", u"Animate", None))
        self.c_auto_refresh.setText(QCoreApplication.translate("DDataPlotter", u"Auto Refresh", None))
        self.b_refresh.setText(QCoreApplication.translate("DDataPlotter", u"Refresh", None))
    # retranslateUi

