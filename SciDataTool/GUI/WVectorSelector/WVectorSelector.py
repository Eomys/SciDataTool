from PySide2.QtWidgets import QWidget

from SciDataTool.GUI.WVectorSelector.Ui_WVectorSelector import Ui_WVectorSelector
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

        self.c_referential.hide()
        self.in_referential.hide()

        # self.c_referential.currentTextChanged.connect(self.update_needed)

        self.component_selected = None
        self.component_list = list()

        # Adding items inside the combobox to name the two sets of coordinates
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

        # Modifying the width of the dropdown list to make sure that all the element are readable
        component_list = [
            self.c_component.itemText(i) for i in range(self.c_component.count())
        ]
        width_drop_down = max([len(ac) for ac in component_list]) * 6
        self.c_component.view().setMinimumWidth(width_drop_down)

    def get_component_selected(self):
        """Getting the component selected

        Parameters
        ----------
        self : WExport
            a WVectorSelector object

        """
        return self.c_component.currentText()

    def set_component(self, component_selected):
        """Method that set the component selected according to the input of the user (auto-plot)
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
        component_selected : str
            Component to select
        """

        # Setting the combobox with the right component
        if component_selected in self.component_list:
            self.c_component.setCurrentIndex(
                self.component_list.index(component_selected)
            )
        else:
            print(
                "WARNING : Trying to set the vector to "
                + component_selected
                + " a component which is not available. Setting to default component"
            )
            self.c_component.setCurrentIndex(1)

    def update(self, data):
        """Updating the combobox according to the components store in the VectorField

        Parameters
        ----------
        self : WExport
            a WVectorSelector object
        data : VectorField
            the object that we want to plot
        """
        comp_stored = data.components

        self.blockSignals(True)
        self.c_component.clear()
        self.c_component.addItems(comp_stored)
        if "radial" in comp_stored or "tangential" in comp_stored:
            try:
                data.to_xyz()
                self.c_component.addItem("comp_x")
                self.c_component.addItem("comp_y")
            except:
                pass
        elif "comp_x" in comp_stored or "comp_y" in comp_stored:
            try:
                data.to_rphiz()
                self.c_component.addItem("radial")
                self.c_component.addItem("tangential")
            except:
                pass

        # Recovering all the components available after the update
        self.component_list = [
            self.c_component.itemText(i) for i in range(self.c_component.count())
        ]

        self.c_component.setCurrentIndex(0)
        self.blockSignals(False)

    def update_needed(self):
        """Emit a signal when the component must be changed

        Parameters
        ----------
        self : WExport
            a WVectorSelector object

        """
        # if self.c_component.currentText() in [
        #     "Polar coordinates",
        #     "Cartesian coordinates",
        # ]:
        #     self.c_component.setCurrentIndex(self.c_component.currentIndex() + 1)

        self.refreshComponent.emit()
