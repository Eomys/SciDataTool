# -*- coding: utf-8 -*-

# File generated according to WAxisManager.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ...GUI.WAxisSelector.WAxisSelector import WAxisSelector


class Ui_WAxisManager(object):
    def setupUi(self, WAxisManager):
        if not WAxisManager.objectName():
            WAxisManager.setObjectName(u"WAxisManager")
        WAxisManager.resize(414, 543)
        self.g_data_extract = QGroupBox(WAxisManager)
        self.g_data_extract.setObjectName(u"g_data_extract")
        self.g_data_extract.setGeometry(QRect(10, 180, 271, 211))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_data_extract.sizePolicy().hasHeightForWidth())
        self.g_data_extract.setSizePolicy(sizePolicy)
        self.g_data_extract.setMinimumSize(QSize(0, 210))
        self.g_data_extract.setMaximumSize(QSize(296, 16777215))
        self.verticalLayoutWidget = QWidget(self.g_data_extract)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 251, 181))
        self.lay_data_extract = QVBoxLayout(self.verticalLayoutWidget)
        self.lay_data_extract.setSpacing(2)
        self.lay_data_extract.setObjectName(u"lay_data_extract")
        self.lay_data_extract.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lay_data_extract.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.lay_data_extract.addItem(self.verticalSpacer)

        self.g_axes = QGroupBox(WAxisManager)
        self.g_axes.setObjectName(u"g_axes")
        self.g_axes.setGeometry(QRect(11, 11, 271, 161))
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.g_axes.sizePolicy().hasHeightForWidth())
        self.g_axes.setSizePolicy(sizePolicy1)
        self.g_axes.setMinimumSize(QSize(0, 120))
        self.g_axes.setMaximumSize(QSize(296, 16777215))
        self.layoutWidget = QWidget(self.g_axes)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 21, 251, 137))
        self.lay_axes = QHBoxLayout(self.layoutWidget)
        self.lay_axes.setObjectName(u"lay_axes")
        self.lay_axes.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 35, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 18))

        self.verticalLayout.addWidget(self.label_4)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setMinimumSize(QSize(0, 18))

        self.verticalLayout.addWidget(self.label_3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.lay_axes.addLayout(self.verticalLayout)

        self.w_axis_1 = WAxisSelector(self.layoutWidget)
        self.w_axis_1.setObjectName(u"w_axis_1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.w_axis_1.sizePolicy().hasHeightForWidth())
        self.w_axis_1.setSizePolicy(sizePolicy3)
        self.w_axis_1.setMinimumSize(QSize(0, 30))

        self.lay_axes.addWidget(self.w_axis_1)

        self.w_axis_2 = WAxisSelector(self.layoutWidget)
        self.w_axis_2.setObjectName(u"w_axis_2")
        sizePolicy3.setHeightForWidth(self.w_axis_2.sizePolicy().hasHeightForWidth())
        self.w_axis_2.setSizePolicy(sizePolicy3)
        self.w_axis_2.setMinimumSize(QSize(0, 30))

        self.lay_axes.addWidget(self.w_axis_2)


        self.retranslateUi(WAxisManager)

        QMetaObject.connectSlotsByName(WAxisManager)
    # setupUi

    def retranslateUi(self, WAxisManager):
        WAxisManager.setWindowTitle(QCoreApplication.translate("WAxisManager", u"WAxisManager", None))
        self.g_data_extract.setTitle(QCoreApplication.translate("WAxisManager", u"Slices/Operations", None))
        self.g_axes.setTitle(QCoreApplication.translate("WAxisManager", u"Axes", None))
        self.label_4.setText(QCoreApplication.translate("WAxisManager", u"Axis", None))
        self.label_2.setText(QCoreApplication.translate("WAxisManager", u"Action", None))
        self.label_3.setText(QCoreApplication.translate("WAxisManager", u"Unit", None))
    # retranslateUi

