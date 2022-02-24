from PySide2.QtWidgets import QWidget
import matplotlib.pyplot as plt

from SciDataTool.GUI.WDataRange.Ui_WDataRange import Ui_WDataRange
from PySide2.QtCore import Signal
from SciDataTool.Functions import parser


class WDataRange(Ui_WDataRange, QWidget):
    """Widget to select the Data/output range"""

    refreshNeeded = Signal()

    def __init__(self, parent=None):
        """Linking the button with their method + initializing the arguments used

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        parent : QWidget
            The parent QWidget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.name = ""
        self.unit_list = list()
        self.unit = None

        self.c_unit.currentTextChanged.connect(self.update_unit)
        self.lf_min.editingFinished.connect(self.update_needed)
        self.lf_max.editingFinished.connect(self.update_needed)

    def get_field_selected(self):
        """Method that will sent the parameters on the field selected by the user (unit and min/max)
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        Output
        ---------
        string
            name of the action on the field
        """

        return {
            "unit": self.c_unit.currentText(),
            "min": self.lf_min.value(),
            "max": self.lf_max.value(),
        }

    def set_min_max(self):
        """Method that will set the FloatEdit of the widget that are responsible for the min value and for the max value.
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """

        field_min = None
        field_max = None

        # Get limits from figure
        fig = plt.gcf()
        if fig is not None:
            if len(fig.axes) == 1:
                field_min = fig.axes[0].get_ylim()[0]
                field_max = fig.axes[0].get_ylim()[1]
            else:
                field_min = fig.axes[1].dataLim.extents[0]
                field_max = fig.axes[1].dataLim.extents[-1]

        if field_min is not None:
            is_dB = "dB" in self.unit
            self.lf_min.setValue(field_min, is_dB)
            self.lf_max.setValue(field_max, is_dB)
        else:
            self.lf_min.clear()
            self.lf_max.clear()

    def set_name(self, field_name):
        """Method that set the name of the widget which is the name of the field that we are plotting

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        field : DataND
            the data object that hold the field that we want to plot
        """
        self.name = field_name

    def set_range(self, data, unit=None):
        """Method that set the data range widget with the value from the DataND object

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        data : DataND
            the data object that hold the field that will set the widget
        """
        if unit is not None:
            self.unit = unit
            self.set_unit(data)
            if unit != "SI":  # Adding unit to unit combobox
                if self.c_unit.currentText() != unit:
                    self.c_unit.insertItem(0, unit)
            if unit == "dBA" and self.c_unit.count() > 1:  # Also adding dB
                self.c_unit.insertItem(1, "dB")
            self.c_unit.setCurrentIndex(0)
        # else:
        #     self.set_unit(data)
        self.lf_min.clear()
        self.lf_max.clear()

    def set_range_user_input(
        self,
        z_min=None,
        z_max=None,
    ):
        """Method that modify the unit selected and the floatEdit according to the inputs given by the user (auto-plot)
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        z_min : float
            Minimum value for Z axis (or Y if only one axe)
        z_max : float
            Minimum value for Z axis (or Y if only one axe)
        """
        is_dB = "dB" in self.unit
        if z_max is not None:
            # Setting max float edit
            self.lf_max.setValue(z_max, is_dB)
        if z_min is not None:
            # Setting min float edit
            self.lf_min.setValue(z_min, is_dB)

    def set_unit(self, field):
        """Method that set the unit combobox according to the unit of the field that we are plotting

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        data : DataND
            the data object that hold the field that we want to plot
        """

        # # Updating the unit combobox
        self.c_unit.clear()
        self.c_unit.addItem(field.unit)
        self.unit = field.unit

    def update_unit(self):
        """Method that clears min/max then calls update_needed
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """
        self.lf_max.clear()
        self.lf_min.clear()
        self.update_needed()

    def update_needed(self):
        """Method that emit a signal to automatically refresh the plot inside the GUI
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """
        # Making sure that we always have min < max
        if self.lf_min.value() != None and self.lf_max.value() != None:
            if self.lf_min.value() > self.lf_max.value():
                is_dB = "dB" in self.unit
                self.blockSignals(True)
                temp = self.lf_max.value()
                self.lf_max.setValue(self.lf_min.value(), is_dB)
                self.lf_min.setValue(temp, is_dB)
                self.blockSignals(False)

        self.refreshNeeded.emit()
