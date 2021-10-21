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
        WAxisManager.resize(400, 300)
        self.layoutWidget = QWidget(WAxisManager)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 11, 301, 271))
        self.lay_main = QVBoxLayout(self.layoutWidget)
        self.lay_main.setObjectName(u"lay_main")
        self.lay_main.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.g_axes = QGroupBox(self.layoutWidget)
        self.g_axes.setObjectName(u"g_axes")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_axes.sizePolicy().hasHeightForWidth())
        self.g_axes.setSizePolicy(sizePolicy)
        self.g_axes.setMinimumSize(QSize(0, 0))
        self.g_axes.setMaximumSize(QSize(296, 16777215))
        self.layoutWidget1 = QWidget(self.g_axes)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(11, 21, 281, 109))
        self.lay_axes = QVBoxLayout(self.layoutWidget1)
        self.lay_axes.setObjectName(u"lay_axes")
        self.lay_axes.setContentsMargins(0, 0, 0, 0)
        self.w_axis_1 = WAxisSelector(self.layoutWidget1)
        self.w_axis_1.setObjectName(u"w_axis_1")
        self.w_axis_1.setMinimumSize(QSize(0, 50))

        self.lay_axes.addWidget(self.w_axis_1)

        self.w_axis_2 = WAxisSelector(self.layoutWidget1)
        self.w_axis_2.setObjectName(u"w_axis_2")
        self.w_axis_2.setMinimumSize(QSize(0, 50))

        self.lay_axes.addWidget(self.w_axis_2)


        self.lay_main.addWidget(self.g_axes)

        self.g_data_extract = QGroupBox(self.layoutWidget)
        self.g_data_extract.setObjectName(u"g_data_extract")
        sizePolicy.setHeightForWidth(self.g_data_extract.sizePolicy().hasHeightForWidth())
        self.g_data_extract.setSizePolicy(sizePolicy)
        self.g_data_extract.setMinimumSize(QSize(0, 0))
        self.g_data_extract.setMaximumSize(QSize(296, 16777215))
        self.verticalLayoutWidget = QWidget(self.g_data_extract)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(19, 19, 271, 101))
        self.lay_data_extract = QVBoxLayout(self.verticalLayoutWidget)
        self.lay_data_extract.setObjectName(u"lay_data_extract")
        self.lay_data_extract.setContentsMargins(0, 0, 0, 0)

        self.lay_main.addWidget(self.g_data_extract)


        self.retranslateUi(WAxisManager)

        QMetaObject.connectSlotsByName(WAxisManager)
    # setupUi

    def retranslateUi(self, WAxisManager):
        WAxisManager.setWindowTitle(QCoreApplication.translate("WAxisManager", u"WAxisManager", None))
        self.g_axes.setTitle(QCoreApplication.translate("WAxisManager", u"Axes", None))
        self.g_data_extract.setTitle(QCoreApplication.translate("WAxisManager", u"Data Selection", None))
    # retranslateUi

