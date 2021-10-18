from PySide2.QtWidgets import QWidget

from ...GUI.WDataExtractor.Ui_WDataExtractor import Ui_WDataExtractor


class WDataExtractor(Ui_WDataExtractor, QWidget):
    """Widget to define how to handle the 'non-plot' axis"""

    def __init__(self):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)