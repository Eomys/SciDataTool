# -*- coding: utf-8 -*-

# File generated according to WVectorSelector.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_WVectorSelector(object):
    def setupUi(self, WVectorSelector):
        if not WVectorSelector.objectName():
            WVectorSelector.setObjectName(u"WVectorSelector")
        WVectorSelector.resize(456, 255)
        self.widget = QWidget(WVectorSelector)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 261, 51))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.in_component = QLabel(self.widget)
        self.in_component.setObjectName(u"in_component")

        self.gridLayout.addWidget(self.in_component, 0, 0, 1, 1)

        self.c_component = QComboBox(self.widget)
        self.c_component.setObjectName(u"c_component")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_component.sizePolicy().hasHeightForWidth())
        self.c_component.setSizePolicy(sizePolicy)
        self.c_component.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.c_component, 0, 1, 1, 1)

        self.in_referential = QLabel(self.widget)
        self.in_referential.setObjectName(u"in_referential")

        self.gridLayout.addWidget(self.in_referential, 1, 0, 1, 1)

        self.c_referential = QComboBox(self.widget)
        self.c_referential.addItem("")
        self.c_referential.addItem("")
        self.c_referential.addItem("")
        self.c_referential.setObjectName(u"c_referential")
        sizePolicy.setHeightForWidth(self.c_referential.sizePolicy().hasHeightForWidth())
        self.c_referential.setSizePolicy(sizePolicy)
        self.c_referential.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.c_referential, 1, 1, 1, 1)


        self.retranslateUi(WVectorSelector)

        QMetaObject.connectSlotsByName(WVectorSelector)
    # setupUi

    def retranslateUi(self, WVectorSelector):
        WVectorSelector.setWindowTitle(QCoreApplication.translate("WVectorSelector", u"WVectorSelector", None))
        self.in_component.setText(QCoreApplication.translate("WVectorSelector", u"Component", None))
        self.in_referential.setText(QCoreApplication.translate("WVectorSelector", u"Referential", None))
        self.c_referential.setItemText(0, QCoreApplication.translate("WVectorSelector", u"xyz", None))
        self.c_referential.setItemText(1, QCoreApplication.translate("WVectorSelector", u"radtanz", None))
        self.c_referential.setItemText(2, "")

    # retranslateUi

