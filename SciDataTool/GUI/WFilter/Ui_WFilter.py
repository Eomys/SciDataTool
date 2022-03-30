# -*- coding: utf-8 -*-

# File generated according to WFilter.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from SciDataTool.GUI.Tools.CheckBox import CheckBox


class Ui_WFilter(object):
    def setupUi(self, WFilter):
        if not WFilter.objectName():
            WFilter.setObjectName("WFilter")
        WFilter.resize(831, 644)
        WFilter.setMinimumSize(QSize(630, 470))
        WFilter.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(WFilter)
        self.gridLayout.setObjectName("gridLayout")
        self.tab_indices = QTableView(WFilter)
        self.tab_indices.setObjectName("tab_indices")

        self.gridLayout.addWidget(self.tab_indices, 0, 0, 1, 1)

        self.cb_all = CheckBox(WFilter)
        self.cb_all.setObjectName("cb_all")
        self.cb_all.setTristate(True)

        self.gridLayout.addWidget(self.cb_all, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.b_Ok = QPushButton(WFilter)
        self.b_Ok.setObjectName("b_Ok")

        self.horizontalLayout.addWidget(self.b_Ok)

        self.b_cancel = QPushButton(WFilter)
        self.b_cancel.setObjectName("b_cancel")

        self.horizontalLayout.addWidget(self.b_cancel)

        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(WFilter)

        QMetaObject.connectSlotsByName(WFilter)

    # setupUi

    def retranslateUi(self, WFilter):
        WFilter.setWindowTitle(QCoreApplication.translate("WFilter", "WFilter", None))
        self.cb_all.setText(
            QCoreApplication.translate("WFilter", "Select/Deselect all", None)
        )
        self.b_Ok.setText(QCoreApplication.translate("WFilter", "Ok", None))
        self.b_cancel.setText(QCoreApplication.translate("WFilter", "Cancel", None))

    # retranslateUi
