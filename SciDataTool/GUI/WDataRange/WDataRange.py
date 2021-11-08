from PySide2.QtWidgets import QWidget
from matplotlib.pyplot import axes

from ...GUI.WDataRange.Ui_WDataRange import Ui_WDataRange
from ...Functions.Plot import unit_dict, ifft_dict
from PySide2.QtCore import Signal
from SciDataTool.Functions import parser


class WDataRange(Ui_WDataRange, QWidget):
    """Widget to select the Data/output range"""

    refreshNeeded = Signal()

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

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

        self.c_unit.currentTextChanged.connect(self.update_needed)
        self.lf_min.editingFinished.connect(self.update_needed)
        self.lf_max.editingFinished.connect(self.update_needed)

    def get_field_selected(self):
        """Method that will sent the operation on the field selected by the user (unit and min/max)
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

    def set_min_max(self, field, axes_selected, data_selection):
        """Method that will set the FloatEdit of the widget that are responsible for the min value and for the max value.
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        field : DataND
            the data object that hold the field that we want to plot
        axes_selected : list
            list that holds the name of the axes selected, so that we can use the method get_along/get_magnitude_along
        data_selection : list
            list that holds the name of the slices/operation selected, so that we can use the method get_along/get_magnitude_along
        """

        axes_selected_parsed = parser.read_input_strings(axes_selected, axis_data=None)

        # Recovering the minimum and the maximum of the field
        if len(axes_selected) == 1:

            # Checking if the field is plotted in fft, then we use get_magnitude_along
            # Otherwise we use get_along

            if axes_selected_parsed[0].name in ifft_dict:
                field_value = field.get_magnitude_along(
                    data_selection[0], data_selection[1], axes_selected[0]
                )
            else:
                field_value = field.get_along(
                    data_selection[0], data_selection[1], axes_selected[0]
                )

            field_min = field_value[field.symbol].min()
            field_max = field_value[field.symbol].max()

        elif len(axes_selected) == 2:

            # Checking if the field is plotted in fft, then we use get_magnitude_along
            # Otherwise we use get_along
            if (
                axes_selected_parsed[0].name in ifft_dict
                and axes_selected_parsed[1].name in ifft_dict
            ):
                field_value = field.get_magnitude_along(
                    data_selection[0], axes_selected[0], axes_selected[1]
                )
            else:
                field_value = field.get_along(
                    data_selection[0], axes_selected[0], axes_selected[1]
                )

            field_min = field_value[field.symbol].min()
            field_max = field_value[field.symbol].max()

        # Setting the FloatEdit with the value recovered
        self.lf_min.setValue(field_min)
        self.lf_max.setValue(field_max)

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

    def set_range(self, data, axes_selected, data_selection):
        """Method that set the data range widget with the value from the DataND object

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        data : DataND
            the data object that hold the field that will set the widget
        """

        self.set_name(data.name)
        self.set_unit(data)
        self.set_min_max(data, axes_selected, data_selection)

    def set_range_user_input(self, user_input_dict):
        """Method that modify the unit selected and the floatEdit according to the inputs given by the user (auto-plot)
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        user_input_dict : dictionnary
            dictionnary that stores all the argument given to have an auto-plot
        """

        if "unit" in user_input_dict:
            # Selecting the right unit inside the unit combobox
            for i in range(self.c_unit.count()):
                self.c_unit.setCurrentIndex(i)
                if self.c_unit.currentText() == user_input_dict["unit"]:
                    break

        if "zmax" in user_input_dict:
            # Setting max float edit
            self.lf_max.setValue(float(user_input_dict["zmax"]))

        if "zmin" in user_input_dict:
            # Setting min float edit
            self.lf_min.setValue(float(user_input_dict["zmin"]))

    def set_unit(self, field):
        """Method that set the unit combobox according to the unit of the field that we are plotting

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        data : DataND
            the data object that hold the field that we want to plot
        """

        # Checking if the data that we want to plot is known.
        # If so, we will use the unit stored in the dictionary to offer more specific units
        # If that is not the case, we only use the unit stored inside the DataND object
        if self.name in unit_dict:
            self.unit_list = unit_dict[self.name]
        else:
            self.unit_list = list()
            self.unit_list.append(field.unit)

        # Updating the unit combobox
        self.c_unit.clear()
        self.c_unit.addItems(self.unit_list)

    def update_needed(self):
        """Method that emit a signal to automatically refresh the plot inside the GUI
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        """
        self.refreshNeeded.emit()
