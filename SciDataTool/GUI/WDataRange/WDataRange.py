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

        self.c_unit.currentTextChanged.connect(self.update_needed)
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
        is_fft = False

        # First we need to define if we have to use get_along or get_magnitude_along depending on the axes/slice selected
        if not None in data_selection and not len(data_selection) == 0:
            data_selection_parsed = parser.read_input_strings(
                data_selection, axis_data=None
            )

            for i in range(len(data_selection_parsed)):
                if data_selection_parsed[i].name in ifft_dict:
                    is_fft = True

        for i in range(len(axes_selected_parsed)):
            if axes_selected_parsed[i].name in ifft_dict:
                is_fft = True

        # If the field is plotted in fft, then we use get_magnitude_along
        # Otherwise we use get_along
        if is_fft == True:
            field_value = field.get_magnitude_along(*[*axes_selected, *data_selection])
        else:
            field_value = field.get_along(*[*axes_selected, *data_selection])

        field_min = field_value[field.symbol].min()
        field_max = field_value[field.symbol].max()

        # IF we have a plot in 2D, then we do not want exactly min and max so we zoom out slightly
        if len(axes_selected) == 1:
            delta = field_max - field_min
            field_min -= 0.1 * delta
            field_max += 0.1 * delta

        # If the value of min and max are the same, then we don't set them up automatically
        eps = 1e-7
        if field_max - field_min > eps:
            self.lf_min.setValue(field_min)
            self.lf_max.setValue(field_max)
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

        if "unit" in user_input_dict and user_input_dict["unit"] != None:
            # Selecting the right unit inside the unit combobox
            for i in range(self.c_unit.count()):
                self.c_unit.setCurrentIndex(i)
                if self.c_unit.currentText() == user_input_dict["unit"]:
                    break

        if "zmax" in user_input_dict and user_input_dict["zmax"] != None:
            # Setting max float edit
            self.lf_max.setValue(float(user_input_dict["zmax"]))

        if "zmin" in user_input_dict and user_input_dict["zmin"] != None:
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
        # Making sure that we always have min < max
        if self.lf_min.value() != None and self.lf_max.value() != None:
            if self.lf_min.value() > self.lf_max.value():

                temp = self.lf_max.value()
                self.lf_max.setValue(self.lf_min.value())
                self.lf_min.setValue(temp)

        self.refreshNeeded.emit()
