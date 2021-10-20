from PySide2.QtWidgets import QWidget

from ...GUI.WAxisSelector.Ui_WAxisSelector import Ui_WAxisSelector

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
    "wavenumber": ["", "space order"],
    "rotation speed": ["rpm"],
}       #Dictionnary that contains the possible units for a given axis

class WAxisSelector(Ui_WAxisSelector, QWidget):
    """Widget to select the axis to plot"""

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

        self.c_axis.currentTextChanged.connect(self.update_unit)

    def update_axis(self,data):
        """Method that will put the axes of data in the combobox"""
        #Step 1 : Getting the name of the different axes
        axes_list = data.get_axes()
        axes_name = ['None']
        
        for axis in axes_list:
            axes_name.append(axis.name)
        
        #Step 2 : Replacing the items inside of the ComboBox by the axes recovered
        self.c_axis.clear()
        self.c_axis.addItems(axes_name)


    def update_unit(self):
        "Method that update the unit comboxbox according to the axis selected"
        #Step 1 : Recovering the axis chosen 
        quantity = self.c_axis.currentText()

        #Step 2 : Adding the right units according to a dictionnary
        if quantity == "None":
            self.c_unit.clear()
            self.c_unit.setDisabled(True)
        else:
            self.c_unit.setDisabled(False)
            self.c_unit.clear()
            self.c_unit.addItems(UNIT_DICT[quantity])
