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
        self.horizontalSpacer = QSpacerItem(190, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.b_export = QPushButton(WExport)
        self.b_export.setObjectName(u"b_export")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_export.sizePolicy().hasHeightForWidth())
        self.b_export.setSizePolicy(sizePolicy)
        self.b_export.setMinimumSize(QSize(72, 24))
        self.b_export.setMaximumSize(QSize(72, 16777215))

        self.horizontalLayout.addWidget(self.b_export)


        self.retranslateUi(WExport)

        QMetaObject.connectSlotsByName(WExport)
    # setupUi

    def retranslateUi(self, WExport):
        self.b_export.setText(QCoreApplication.translate("WExport", u"Export", None))
        pass
    # retranslateUi

