from PySide2.QtWidgets import QWidget

from SciDataTool.GUI.WVectorSelector.Ui_WVectorSelector import Ui_WVectorSelector
from PySide2.QtCore import Signal
from PySide2.QtGui import QStandardItem

COMP_DICT = {
    "all": "all",
    "radial": "radial",
    "circumferential": "tangential",
    "axial": "axial",
    "x-axis component": "comp_x",
    "y-axis component": "comp_y",
    "z-axis component": "comp_z",
}

REV_COMP_DICT = {
    "radial": "radial",
    "tangential": "circumferential",
    "axial": "axial",
    "comp_x": "x-axis component",
    "comp_y": "y-axis component",
    "comp_z": "z-axis component",
}


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

    def get_component_selected(self):
        """Getting the component selected

        Parameters
        ----------
        self : WExport
            a WVectorSelector object

        """
        return COMP_DICT[self.c_component.currentText()]

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
        if REV_COMP_DICT[component_selected] in self.component_list:
            self.c_component.setCurrentText(REV_COMP_DICT[component_selected])
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
        comp_stored = data.components.keys()

        self.blockSignals(True)
        self.c_component.clear()
        self.c_component.addItems([REV_COMP_DICT[comp] for comp in comp_stored])
        model = self.c_component.model()
        if "radial" in comp_stored or "tangential" in comp_stored:
            item = QStandardItem("Polar coordinates")
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setEnabled(False)
            model.insertRow(0, item)
            try:
                data.to_xyz()
                item = QStandardItem("Cartesian coordinates")
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                item.setEnabled(False)
                model.insertRow(self.c_component.count(), item)
                self.c_component.addItem("x-axis component")
                self.c_component.addItem("y-axis component")
                if "axial" in comp_stored:
                    self.c_component.addItem("z-axis component")
            except:
                pass
        elif "comp_x" in comp_stored or "comp_y" in comp_stored:
            item = QStandardItem("Cartesian coordinates")
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setEnabled(False)
            model.insertRow(0, item)
            try:
                data.to_rphiz()
                item = QStandardItem("Polar coordinates")
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                item.setEnabled(False)
                model.insertRow(self.c_component.count(), item)
                self.c_component.addItem("radial")
                self.c_component.addItem("circumferential")
                if "comp_z" in comp_stored:
                    self.c_component.addItem("axial")
            except:
                pass

        # Recovering all the components available after the update
        self.component_list = [
            self.c_component.itemText(i)
            for i in range(self.c_component.count())
            if self.c_component.itemText(i)
            not in ["Polar coordinates", "Cartesian coordinates"]
        ]

        # Modifying the width of the dropdown list to make sure that all the element are readable
        component_list = [
            self.c_component.itemText(i) for i in range(self.c_component.count())
        ]
        width_drop_down = max([len(ac) for ac in component_list]) * 6
        self.c_component.view().setMinimumWidth(width_drop_down)

        self.c_component.setCurrentIndex(1)
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
