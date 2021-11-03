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
        WDataExtractor.resize(318, 100)
        self.verticalLayout = QVBoxLayout(WDataExtractor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.in_name = QLabel(WDataExtractor)
        self.in_name.setObjectName(u"in_name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.in_name.sizePolicy().hasHeightForWidth())
        self.in_name.setSizePolicy(sizePolicy)
        self.in_name.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.in_name)

        self.c_type_extraction = QComboBox(WDataExtractor)
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.addItem("")
        self.c_type_extraction.setObjectName(u"c_type_extraction")
        sizePolicy.setHeightForWidth(self.c_type_extraction.sizePolicy().hasHeightForWidth())
        self.c_type_extraction.setSizePolicy(sizePolicy)
        self.c_type_extraction.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.c_type_extraction)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lf_value = FloatEdit(WDataExtractor)
        self.lf_value.setObjectName(u"lf_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(70)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lf_value.sizePolicy().hasHeightForWidth())
        self.lf_value.setSizePolicy(sizePolicy1)
        self.lf_value.setMinimumSize(QSize(0, 20))
        self.lf_value.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.lf_value)

        self.slider = QSlider(WDataExtractor)
        self.slider.setObjectName(u"slider")
        sizePolicy.setHeightForWidth(self.slider.sizePolicy().hasHeightForWidth())
        self.slider.setSizePolicy(sizePolicy)
        self.slider.setMinimumSize(QSize(0, 20))
        self.slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.b_action = QPushButton(WDataExtractor)
        self.b_action.setObjectName(u"b_action")
        sizePolicy.setHeightForWidth(self.b_action.sizePolicy().hasHeightForWidth())
        self.b_action.setSizePolicy(sizePolicy)
        self.b_action.setMinimumSize(QSize(0, 20))

        self.verticalLayout.addWidget(self.b_action)


        self.retranslateUi(WDataExtractor)

        QMetaObject.connectSlotsByName(WDataExtractor)
    # setupUi

    def retranslateUi(self, WDataExtractor):
        WDataExtractor.setWindowTitle("")
        self.in_name.setText(QCoreApplication.translate("WDataExtractor", u"angle", None))
        self.c_type_extraction.setItemText(0, QCoreApplication.translate("WDataExtractor", u"slice", None))
        self.c_type_extraction.setItemText(1, QCoreApplication.translate("WDataExtractor", u"slice (fft)", None))
        self.c_type_extraction.setItemText(2, QCoreApplication.translate("WDataExtractor", u"rms", None))
        self.c_type_extraction.setItemText(3, QCoreApplication.translate("WDataExtractor", u"rss", None))
        self.c_type_extraction.setItemText(4, QCoreApplication.translate("WDataExtractor", u"sum", None))
        self.c_type_extraction.setItemText(5, QCoreApplication.translate("WDataExtractor", u"mean", None))
        self.c_type_extraction.setItemText(6, QCoreApplication.translate("WDataExtractor", u"integrate", None))
        self.c_type_extraction.setItemText(7, QCoreApplication.translate("WDataExtractor", u"superimpose/filter", None))

        self.lf_value.setText(QCoreApplication.translate("WDataExtractor", u"0.314", None))
        self.b_action.setText(QCoreApplication.translate("WDataExtractor", u"Superimpose selection", None))
    # retranslateUi

