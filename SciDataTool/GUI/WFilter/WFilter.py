from PySide2.QtWidgets import QWidget
import matplotlib.pyplot as plt

from SciDataTool.GUI.WFilter.Ui_WFilter import Ui_WFilter
from PySide2.QtCore import Signal
from SciDataTool.Functions import parser


class WFilter(Ui_WFilter, QWidget):
    """Widget to select the Data/output range"""

    refreshNeeded = Signal()

    def __init__(self, parent=None):
        """Linking the button with their method + initializing the arguments used

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        parent : QWidget
            The parent QWidget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.b_Ok.clicked.connect(self.update_and_close)
        self.b_cancel.clicked.connect(self.cancel_and_close)

    def cancel_and_close(self):
        """Method called when the user click on the cancel button
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        self.close()

    def update_and_close(self):
        """Method called when the click on the Ok button
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        self.close()
