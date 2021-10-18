from PySide2.QtWidgets import QWidget

from ...GUI.WDataRange.Ui_WDataRange import Ui_WDataRange


class WDataRange(Ui_WDataRange, QWidget):
    """Widget to select the Data/output range"""

    def __init__(self):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)