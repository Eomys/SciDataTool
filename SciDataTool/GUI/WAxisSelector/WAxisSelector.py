from PySide2.QtWidgets import QWidget

from ...GUI.WAxisSelector.Ui_WAxisSelector import Ui_WAxisSelector
from PySide2.QtCore import Signal
AXES_DICT = {
    "time": "time",
    "angle": "angle",
    "z": "axial direction",
    "freqs": "frequency",
    "wavenumber": "wavenumber",
}

UNIT_DICT = {
    "elec.get_Is": ["A"],
    "mag.get_B": ["T", "G"],
    "mag.get_Per": ["H/m^2"],
    "mag.get_MMF": ["At"],
    "mag.get_Tem": ["Nm", "dB"],
    "mag.get_Phi_wind_stator": ["Wb", "Mx"],
    "force.get_AGSF": ["N/m^2", "dB"],
    "force.get_LF": ["N", "dB"],
    "force.get_LF_in": ["N", "dB"],
    "force.get_UMP": ["N", "dB"],
    "struct.get_OLC": ["dB", "N"],
    "struct.get_U_rms": ["dB", "m"],
    "struct.get_U_rms_freq": ["dB", "m"],
    "struct.get_V_rms": ["dB", "m/s"],
    "struct.get_V_rms_freq": ["dB", "m/s"],
    "struct.get_A_rms": ["dB", "m/s^2"],
    "struct.get_A_rms_freq": ["dB", "m/s^2"],
    "acoustic.get_W": ["dBA", "dB", "W"],
    "acoustic.get_W_freq": ["dBA", "dB", "W"],
    "time": ["s", "rotor mechanical angle"],
    "angle": ["°", "rad", "distance"],
    "axial direction": ["m", "x L"],
    "frequency": ["Hz", "electrical order", "mechanical order"],
    "wavenumber": ["", "space order"], #check is correct
    "rotation speed": ["rpm"],
}       #Dictionnary that contains the possible units for a given axis

class WAxisSelector(Ui_WAxisSelector, QWidget):
    """Widget to select the axis to plot"""

    refreshNeeded = Signal()
    axisChanged = Signal()

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = "X"         #Name of the axis
        self.axes_list = list() #List of the different axes of the DataND object

        self.b_filter.setDisabled(True)
        self.c_axis.currentTextChanged.connect(self.update_axis)

    def update(self,data,axis_name = "X"):
        """Method used to update the axis by calling the other method defined
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        data : DataND
            A DataND object to plot
        axis_name : string
            string that will set the text of in_name (=name of the axis)
            """
        self.c_axis.blockSignals(True)
        self.change_name(axis_name)
        self.set_axis(data)
        self.set_unit()
        self.c_axis.blockSignals(False)

    def set_axis(self,data):
        """Method that will put the axes of data in the combobox of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        data : DataND
            A DataND object that we want to plot

        """
        #Step 1 : Getting the name of the different axes of the DataND object
        self.axes_list = [AXES_DICT[axis.name] 
        for axis in data.get_axes() 
        if axis.name != "phase" and axis.get_length() > 1
        ]

        # At least one axis must be selected => impossible to have none for X axis
        if self.name.lower() != "x" : 
            self.axes_list.insert(0, "None")

        # Add fft axes
        if "time" in self.axes_list:
            self.axes_list.append("frequency")
        elif "frequency" in self.axes_list:
            self.axes_list.insert(0, "time")
        if "angle" in self.axes_list:
            self.axes_list.append("wavenumber")
        elif "wavenumber" in self.axes_list:
            self.axes_list.insert(1, "angle")
        
        #Step 2 : Replacing the items inside of the ComboBox with the axes recovered
        self.c_axis.clear()
        self.c_axis.addItems(self.axes_list)
        self.update_axis()


    def set_unit(self):
        """Method that update the unit comboxbox according to the axis selected in the other combobox
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        #Step 1 : Recovering the axis chosen 
        quantity = self.c_axis.currentText()

        #Step 2 : Adding the right units according to a dictionnary
        if quantity == "None":
            #If the axis is not selected, then we can not choose the unit
            self.c_unit.clear()
            self.c_unit.setDisabled(True)
        else:
            self.c_unit.setDisabled(False)
            self.c_unit.clear()

            if quantity in UNIT_DICT:
                self.c_unit.addItems(UNIT_DICT[quantity])
            
    def change_name(self,axis_name):
        """Method to change of the label of the widget
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        axis_name : string
            string that we will use to set the in_name of the widget

        """

        self.name = axis_name
        self.in_name.setText(axis_name)

    def update_axis(self):
        """Method called when an axis is changed that will emit a signal as well as updating the units available
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object

        """
        self.set_unit()     
        self.refreshNeeded.emit()
        self.axisChanged.emit()

    def get_current_axis_name(self):
        """Method that return the axis currently selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        string
            name of the current axis selected
        """
        return self.c_axis.currentText()

    def get_axes(self):
        """Method that return the axes that can be selected
        Parameters
        ----------
        self : WAxisSelector
            a WAxisSelector object
        Output
        ---------
        list
            name of the axes avalaible
        """
        return self.axes_list