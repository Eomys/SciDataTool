# -*- coding: utf-8 -*-

# File generated according to WFilter.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_WFilter(object):
    def setupUi(self, WFilter):
        if not WFilter.objectName():
            WFilter.setObjectName(u"WFilter")
        WFilter.resize(831, 644)
        WFilter.setMinimumSize(QSize(630, 470))
        WFilter.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_4 = QGridLayout(WFilter)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.b_Ok = QPushButton(WFilter)
        self.b_Ok.setObjectName(u"b_Ok")

        self.horizontalLayout.addWidget(self.b_Ok)

        self.b_cancel = QPushButton(WFilter)
        self.b_cancel.setObjectName(u"b_cancel")

        self.horizontalLayout.addWidget(self.b_cancel)

        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.tab_indices = QTableView(WFilter)
        self.tab_indices.setObjectName(u"tab_indices")
        self.tab_indices.setSortingEnabled(True)
        self.tab_indices._rows = 0
        self.tab_indices._columns = 0

        self.gridLayout_4.addWidget(self.tab_indices, 0, 0, 1, 1)

        self.retranslateUi(WFilter)

        QMetaObject.connectSlotsByName(WFilter)

    # setupUi

    def retranslateUi(self, WFilter):
        WFilter.setWindowTitle(QCoreApplication.translate("WFilter", u"WFilter", None))
        self.b_Ok.setText(QCoreApplication.translate("WFilter", u"Ok", None))
        self.b_cancel.setText(QCoreApplication.translate("WFilter", u"Cancel", None))

    # retranslateUi
