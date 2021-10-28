from PySide2.QtWidgets import QWidget

from ...GUI.WDataExtractor.Ui_WDataExtractor import Ui_WDataExtractor
from ...Functions.Plot import axes_dict


class WDataExtractor(Ui_WDataExtractor, QWidget):
    """Widget to define how to handle the 'non-plot' axis"""

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        parent : QWidget
            The parent QWidget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.name = "angle"

    def get_name(self):
        """Method that return the name of the axis of the WDataExtractor
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        """
        return self.name

    def set_name(self, name):
        """Method that set the name of the axis of the WDataExtractor
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        name : string
            string that hold the name of the axis
        """
        if name in axes_dict:
            self.in_name.setText(axes_dict[name])
        else:
            self.in_name.setText(name)

        self.name = name

    def update(self, axis):
        """Method that will update the WDataExtractor widget according to the axis given to it
        Parameters
        ----------
        self : WDataExtractor
            a WDataExtractor object
        axis : string
            string with the name of the axis that should set the WDataExtractor widget
        """

        self.set_name(axis)
