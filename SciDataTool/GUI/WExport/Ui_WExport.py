# -*- coding: utf-8 -*-

# File generated according to WExport.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_WExport(object):
    def setupUi(self, WExport):
        if not WExport.objectName():
            WExport.setObjectName(u"WExport")
        WExport.resize(265, 50)
        self.horizontalLayout = QHBoxLayout(WExport)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            140, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.b_export = QPushButton(WExport)
        self.b_export.setObjectName(u"b_export")

        self.horizontalLayout.addWidget(self.b_export)

        self.retranslateUi(WExport)

        QMetaObject.connectSlotsByName(WExport)

    # setupUi

    def retranslateUi(self, WExport):
        self.b_export.setText(QCoreApplication.translate("WExport", u"Export", None))
        pass

    # retranslateUi
