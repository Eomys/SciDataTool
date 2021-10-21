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
        WAxisManager.resize(743, 300)
        self.widget = QWidget(WAxisManager)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(11, 11, 301, 271))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.g_axes = QGroupBox(self.widget)
        self.g_axes.setObjectName(u"g_axes")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g_axes.sizePolicy().hasHeightForWidth())
        self.g_axes.setSizePolicy(sizePolicy)
        self.g_axes.setMinimumSize(QSize(0, 0))
        self.g_axes.setMaximumSize(QSize(296, 16777215))
        self.widget1 = QWidget(self.g_axes)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(11, 21, 281, 109))
        self.verticalLayout = QVBoxLayout(self.widget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.w_axis_1 = WAxisSelector(self.widget1)
        self.w_axis_1.setObjectName(u"w_axis_1")
        self.w_axis_1.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.w_axis_1)

        self.w_axis_2 = WAxisSelector(self.widget1)
        self.w_axis_2.setObjectName(u"w_axis_2")
        self.w_axis_2.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.w_axis_2)


        self.verticalLayout_2.addWidget(self.g_axes)

        self.g_data_extract = QGroupBox(self.widget)
        self.g_data_extract.setObjectName(u"g_data_extract")
        sizePolicy.setHeightForWidth(self.g_data_extract.sizePolicy().hasHeightForWidth())
        self.g_data_extract.setSizePolicy(sizePolicy)
        self.g_data_extract.setMinimumSize(QSize(0, 0))
        self.g_data_extract.setMaximumSize(QSize(296, 16777215))

        self.verticalLayout_2.addWidget(self.g_data_extract)


        self.retranslateUi(WAxisManager)

        QMetaObject.connectSlotsByName(WAxisManager)
    # setupUi

    def retranslateUi(self, WAxisManager):
        WAxisManager.setWindowTitle(QCoreApplication.translate("WAxisManager", u"WAxisManager", None))
        self.g_axes.setTitle(QCoreApplication.translate("WAxisManager", u"Axes", None))
        self.g_data_extract.setTitle(QCoreApplication.translate("WAxisManager", u"Data Selection", None))
    # retranslateUi

