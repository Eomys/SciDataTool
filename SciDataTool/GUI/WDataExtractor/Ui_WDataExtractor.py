# -*- coding: utf-8 -*-

# File generated according to WDataExtractor.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ...GUI.Tools.FloatEdit import FloatEdit


class Ui_WDataExtractor(object):
    def setupUi(self, WDataExtractor):
        if not WDataExtractor.objectName():
            WDataExtractor.setObjectName(u"WDataExtractor")
        WDataExtractor.resize(324, 112)
        self.verticalLayout = QVBoxLayout(WDataExtractor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.in_name = QLabel(WDataExtractor)
        self.in_name.setObjectName(u"in_name")

        self.horizontalLayout.addWidget(self.in_name)

        self.c_type_extraction = QComboBox(WDataExtractor)
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.setObjectName(u"c_type_extraction")

        self.horizontalLayout.addWidget(self.c_type_extraction)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lf_value = FloatEdit(WDataExtractor)
        self.lf_value.setObjectName(u"lf_value")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lf_value.sizePolicy().hasHeightForWidth())
        self.lf_value.setSizePolicy(sizePolicy)
        self.lf_value.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.lf_value)

        self.slider = QSlider(WDataExtractor)
        self.slider.setObjectName(u"slider")
        self.slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.b_action = QPushButton(WDataExtractor)
        self.b_action.setObjectName(u"b_action")

        self.verticalLayout.addWidget(self.b_action)

        self.retranslateUi(WDataExtractor)

        QMetaObject.connectSlotsByName(WDataExtractor)

    # setupUi

    def retranslateUi(self, WDataExtractor):
        WDataExtractor.setWindowTitle("")
        self.in_name.setText(
            QCoreApplication.translate("WDataExtractor", u"angle", None)
        )
        self.c_type_extraction.setItemText(
            0, QCoreApplication.translate("WDataExtractor", u"slice", None)
        )
        self.c_type_extraction.setItemText(
            1, QCoreApplication.translate("WDataExtractor", u"sum", None)
        )
        self.c_type_extraction.setItemText(
            2, QCoreApplication.translate("WDataExtractor", u"mean", None)
        )
        self.c_type_extraction.setItemText(
            3, QCoreApplication.translate("WDataExtractor", u"superimpose", None)
        )
        self.c_type_extraction.setItemText(
            4, QCoreApplication.translate("WDataExtractor", u"animate", None)
        )
        self.c_type_extraction.setItemText(5, "")

        self.lf_value.setText(
            QCoreApplication.translate("WDataExtractor", u"0.314", None)
        )
        self.b_action.setText(
            QCoreApplication.translate(
                "WDataExtractor", u"Superimpose selection / Animate", None
            )
        )

    # retranslateUi
