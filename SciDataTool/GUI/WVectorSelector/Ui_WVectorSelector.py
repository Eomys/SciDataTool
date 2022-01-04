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
        WVectorSelector.resize(218, 122)
        self.verticalLayout_2 = QVBoxLayout(WVectorSelector)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.g_vector_comp = QGroupBox(WVectorSelector)
        self.g_vector_comp.setObjectName(u"g_vector_comp")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.g_vector_comp.sizePolicy().hasHeightForWidth()
        )
        self.g_vector_comp.setSizePolicy(sizePolicy)
        self.g_vector_comp.setMinimumSize(QSize(0, 0))
        self.g_vector_comp.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.g_vector_comp)
        self.gridLayout.setObjectName(u"gridLayout")
        self.in_component = QLabel(self.g_vector_comp)
        self.in_component.setObjectName(u"in_component")
        self.in_component.setMinimumSize(QSize(0, 21))

        self.gridLayout.addWidget(self.in_component, 0, 0, 1, 1)

        self.c_component = QComboBox(self.g_vector_comp)
        self.c_component.addItem("")
        self.c_component.addItem("")
        self.c_component.addItem("")
        self.c_component.addItem("")
        self.c_component.addItem("")
        self.c_component.addItem("")
        self.c_component.setObjectName(u"c_component")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.c_component.sizePolicy().hasHeightForWidth())
        self.c_component.setSizePolicy(sizePolicy1)
        self.c_component.setMinimumSize(QSize(0, 21))
        self.c_component.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.c_component.setFont(font)

        self.gridLayout.addWidget(self.c_component, 0, 1, 1, 1)

        self.in_referential = QLabel(self.g_vector_comp)
        self.in_referential.setObjectName(u"in_referential")
        self.in_referential.setEnabled(True)
        self.in_referential.setMinimumSize(QSize(0, 21))

        self.gridLayout.addWidget(self.in_referential, 1, 0, 1, 1)

        self.c_referential = QComboBox(self.g_vector_comp)
        self.c_referential.addItem("")
        self.c_referential.addItem("")
        self.c_referential.setObjectName(u"c_referential")
        self.c_referential.setEnabled(True)
        sizePolicy1.setHeightForWidth(
            self.c_referential.sizePolicy().hasHeightForWidth()
        )
        self.c_referential.setSizePolicy(sizePolicy1)
        self.c_referential.setMinimumSize(QSize(100, 21))

        self.gridLayout.addWidget(self.c_referential, 1, 1, 1, 1)

        self.verticalLayout_2.addWidget(self.g_vector_comp)

        self.retranslateUi(WVectorSelector)

        QMetaObject.connectSlotsByName(WVectorSelector)

    # setupUi

    def retranslateUi(self, WVectorSelector):
        WVectorSelector.setWindowTitle(
            QCoreApplication.translate("WVectorSelector", u"WVectorSelector", None)
        )
        self.g_vector_comp.setTitle("")
        self.in_component.setText(
            QCoreApplication.translate("WVectorSelector", u"Component", None)
        )
        self.c_component.setItemText(
            0, QCoreApplication.translate("WVectorSelector", u"radial", None)
        )
        self.c_component.setItemText(
            1, QCoreApplication.translate("WVectorSelector", u"tangential", None)
        )
        self.c_component.setItemText(
            2, QCoreApplication.translate("WVectorSelector", u"axial", None)
        )
        self.c_component.setItemText(
            3, QCoreApplication.translate("WVectorSelector", u"comp_x", None)
        )
        self.c_component.setItemText(
            4, QCoreApplication.translate("WVectorSelector", u"comp_y", None)
        )
        self.c_component.setItemText(
            5, QCoreApplication.translate("WVectorSelector", u"comp_z", None)
        )

        self.in_referential.setText(
            QCoreApplication.translate("WVectorSelector", u"Referential", None)
        )
        self.c_referential.setItemText(
            0, QCoreApplication.translate("WVectorSelector", u"xyz", None)
        )
        self.c_referential.setItemText(
            1, QCoreApplication.translate("WVectorSelector", u"radphiz", None)
        )

    # retranslateUi
