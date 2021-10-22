from PySide2.QtWidgets import QWidget

from ...GUI.WDataExtractor.Ui_WDataExtractor import Ui_WDataExtractor


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

        return self.in_name.text()

    def set_name (self,name):

        self.name = name
        self.in_name.setText(name)

    def update(self,name):

        self.set_name(name)

