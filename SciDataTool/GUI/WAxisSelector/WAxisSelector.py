from PySide2.QtWidgets import QWidget

from ...GUI.WAxisSelector.Ui_WAxisSelector import Ui_WAxisSelector


class WAxisSelector(Ui_WAxisSelector, QWidget):
    """Widget to select the axis to plot"""

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent)
        self.setupUi(self)
