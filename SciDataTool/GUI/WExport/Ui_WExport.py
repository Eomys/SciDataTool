# -*- coding: utf-8 -*-

# File generated according to WExport.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_WDataRange(object):
    def setupUi(self, WDataRange):
        if not WDataRange.objectName():
            WDataRange.setObjectName(u"WDataRange")
        WDataRange.resize(265, 50)
        icon = QIcon()
        icon.addFile(
            u":/images/images/icon/Manatee.ico", QSize(), QIcon.Normal, QIcon.Off
        )
        WDataRange.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(WDataRange)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            140, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.b_export = QPushButton(WDataRange)
        self.b_export.setObjectName(u"b_export")

        self.horizontalLayout.addWidget(self.b_export)

        self.retranslateUi(WDataRange)

        QMetaObject.connectSlotsByName(WDataRange)

    # setupUi

    def retranslateUi(self, WDataRange):
        WDataRange.setWindowTitle(
            QCoreApplication.translate("WDataRange", u"MANATEE Plot", None)
        )
        self.b_export.setText(QCoreApplication.translate("WDataRange", u"Export", None))

    # retranslateUi
