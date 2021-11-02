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
        WAxisManager.resize(330, 600)
        self.g_data_extract = QGroupBox(WAxisManager)
        self.g_data_extract.setObjectName(u"g_data_extract")
        self.g_data_extract.setGeometry(QRect(11, 138, 271, 450))
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_data_extract.sizePolicy().hasHeightForWidth())
        self.g_data_extract.setSizePolicy(sizePolicy)
        self.g_data_extract.setMinimumSize(QSize(0, 450))
        self.g_data_extract.setMaximumSize(QSize(296, 16777215))
        self.verticalLayoutWidget = QWidget(self.g_data_extract)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 251, 411))
        self.lay_data_extract = QVBoxLayout(self.verticalLayoutWidget)
        self.lay_data_extract.setSpacing(2)
        self.lay_data_extract.setObjectName(u"lay_data_extract")
        self.lay_data_extract.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lay_data_extract.setContentsMargins(0, 0, 0, 0)
        self.g_axes = QGroupBox(WAxisManager)
        self.g_axes.setObjectName(u"g_axes")
        self.g_axes.setGeometry(QRect(11, 11, 271, 120))
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.g_axes.sizePolicy().hasHeightForWidth())
        self.g_axes.setSizePolicy(sizePolicy1)
        self.g_axes.setMinimumSize(QSize(0, 120))
        self.g_axes.setMaximumSize(QSize(296, 16777215))
        self.layoutWidget = QWidget(self.g_axes)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 251, 92))
        self.lay_axes = QVBoxLayout(self.layoutWidget)
        self.lay_axes.setObjectName(u"lay_axes")
        self.lay_axes.setContentsMargins(0, 0, 0, 0)
        self.w_axis_1 = WAxisSelector(self.layoutWidget)
        self.w_axis_1.setObjectName(u"w_axis_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.w_axis_1.sizePolicy().hasHeightForWidth())
        self.w_axis_1.setSizePolicy(sizePolicy2)
        self.w_axis_1.setMinimumSize(QSize(0, 30))

        self.lay_axes.addWidget(self.w_axis_1)

        self.w_axis_2 = WAxisSelector(self.layoutWidget)
        self.w_axis_2.setObjectName(u"w_axis_2")
        sizePolicy2.setHeightForWidth(self.w_axis_2.sizePolicy().hasHeightForWidth())
        self.w_axis_2.setSizePolicy(sizePolicy2)
        self.w_axis_2.setMinimumSize(QSize(0, 30))

        self.lay_axes.addWidget(self.w_axis_2)


        self.retranslateUi(WAxisManager)

        QMetaObject.connectSlotsByName(WAxisManager)
    # setupUi

    def retranslateUi(self, WAxisManager):
        WAxisManager.setWindowTitle(QCoreApplication.translate("WAxisManager", u"WAxisManager", None))
        self.g_data_extract.setTitle(QCoreApplication.translate("WAxisManager", u"Slices/Operations", None))
        self.g_axes.setTitle(QCoreApplication.translate("WAxisManager", u"Axes", None))
    # retranslateUi

