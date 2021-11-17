from PySide2.QtWidgets import QWidget

from ...GUI.WVectorSelector.Ui_WVectorSelector import Ui_WVectorSelector
from PySide2.QtCore import Signal
from PySide2.QtGui import QStandardItem


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

        model = self.c_component.model()

        item = QStandardItem("Polar coordinates")
        font = item.font()
        font.setBold(True)
        item.setFont(font)
        item.setEnabled(False)
        model.insertRow(0, item)

        item = QStandardItem("Cartesian coordinates")
        font = item.font()
        font.setBold(True)
        item.setFont(font)
        item.setEnabled(False)
        model.insertRow(4, item)

        component_list = [
            self.c_component.itemText(i) for i in range(self.c_component.count())
        ]
        width_drop_down = max([len(ac) for ac in component_list]) * 6
        self.c_component.view().setMinimumWidth(width_drop_down)

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
        return self.c_component.currentText()
