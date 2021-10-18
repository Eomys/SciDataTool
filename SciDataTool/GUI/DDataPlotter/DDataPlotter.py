from PySide2.QtWidgets import QWidget

from ...GUI.DDataPlotter.Ui_DDataPlotter import Ui_DDataPlotter


class DDataPlotter(Ui_DDataPlotter, QWidget):
    """Main windows of to plot a Data object"""

    def __init__(self, data):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
        data : DataND
            A DataND object to plot
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        self.data = data
