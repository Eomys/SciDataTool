from PySide2.QtWidgets import QWidget

from ...GUI.WVectorSelector.Ui_WVectorSelector import Ui_WVectorSelector
from PySide2.QtCore import Signal


class WVectorSelector(Ui_WVectorSelector, QWidget):
    """Widget to select how to export the data"""

    refreshComponent = Signal()

    def __init__(self, parent=None):
        """Initialize the UI and linking buttons to their methods

        Parameters
        ----------
        self : WExport
            a WVectorSelector object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.c_component.currentTextChanged.connect(self.update_needed)
        # self.c_referential.currentTextChanged.connect(self.update_needed)

        self.component_selected = None

    def update(self, data):
        """Initialize the component combobox

        Parameters
        ----------
        self : WExport
            a WVectorSelector object
        data : VectorField
            the object that we want to plot
        """

        self.c_component.blockSignals(True)
        components_list = data.components
        self.c_component.addItems(components_list)
        self.c_component.blockSignals(False)
        self.update_needed()

    def update_needed(self):
        """Emit a signal when the component must be changed

        Parameters
        ----------
        self : WExport
            a WVectorSelector object
        data : VectorField
            the object that we want to plot
        """

        self.refreshComponent.emit()

    def get_component_selected(self):
        """Getting the component selected

        Parameters
        ----------
        self : WExport
            a WVectorSelector object

        """
        return self.c_component.currentText(), self.c_referential.currentText()
