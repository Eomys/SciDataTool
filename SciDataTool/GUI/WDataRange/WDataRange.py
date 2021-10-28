from PySide2.QtWidgets import QWidget

from ...GUI.WDataRange.Ui_WDataRange import Ui_WDataRange
from ...Functions.Plot import unit_dict


class WDataRange(Ui_WDataRange, QWidget):
    """Widget to select the Data/output range"""

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

    def set_range(self, data):
        """Method that set the data range widget with the value from data

        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        data : DataND
            the data object that hold the field that will set the widget
        """

        self.set_name(data.name)
        self.set_unit(data)
        self.set_min_max(data)

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

    def set_min_max(self, field):
        """Method that will set the FloatEdit of the widget that are responsible for the min value and for the max value.
        Parameters
        ----------
        self : WDataRange
            a WDataRange object
        field : DataND
            the data object that hold the field that we want to plot
        """

        # Recovering the minimum and the maximum of the
        field_value = field.values

        min_field = min(field_value.flatten())
        max_field = max(field_value.flatten())

        # Setting the FloatEdit with the right value
        self.lf_min.setValue(min_field)
        self.lf_max.setValue(max_field)
