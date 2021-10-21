from PySide2.QtWidgets import QWidget

from ...GUI.WAxisManager.Ui_WAxisManager import Ui_WAxisManager

class WAxisManager(Ui_WAxisManager, QWidget):
    """Widget that will handle the selection of the axis as well as generating WDataExtractor"""

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.w_axis_1.axisChanged.connect(self.update_axes)


    def set_axes(self,data):
        """Method used to set the axes of the Axes group box (e.g setting up the comboboxes + labels)
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            The DataND object that we want to plot
        """
        self.w_axis_1.update(data)
        self.w_axis_2.update(data,"Y")

    def update_axes(self,data):
        """Method that will check if the axes chosen are correct and if true it will update the comboboxes
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            the DataND object that we want to plot
        
        """
        axis1 = self.w_axis_1.get_current_axis()
        axis2 = self.w_axis_2.get_current_axis()

