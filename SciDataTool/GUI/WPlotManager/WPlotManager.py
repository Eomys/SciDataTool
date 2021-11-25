from PySide2.QtWidgets import QWidget, QFileDialog, QMessageBox
from os.path import dirname, basename
from ...Functions.Load.import_class import import_class


from PySide2.QtCore import Signal
from ...GUI.WPlotManager.Ui_WPlotManager import Ui_WPlotManager

SYMBOL_DICT = {
    "time": "t",
    "angle": "\\alpha",
    "axial direction": "z",
    "frequency": "f",
    "wavenumber": "r",
    "rotation speed": "N0",
    "stator current along d-axis": "I_d",
    "stator current along q-axis": "I_q",
    "speed": "N0",
    "torque": "T",
    "a-weighted sound power level": "ASWL",
    "velocity level": "V",
    "reference torque": "T_{ref}",
}


def latex(string):
    """format a string for latex"""
    if "_" in string or "^" in string or "\\" in string:
        string = r"$" + string + "$"
    return string


class WPlotManager(Ui_WPlotManager, QWidget):
    """Main widget of the SciDataTool UI"""

    updatePlot = Signal()

    def __init__(self, parent=None):
        """Initialize the widget by linking buttons to methods

        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        # Building the interaction with the UI and the UI itself
        self.w_axis_manager.refreshRange.connect(self.update_range)
        self.b_export.clicked.connect(self.export)

        # Linking the signals for the autoRefresh
        self.w_axis_manager.refreshNeeded.connect(self.auto_update)
        self.w_range.refreshNeeded.connect(self.auto_update)

    def auto_update(self):
        """Method that update range before sending the signal to update the plot. The auto-refresh policy will be handled in the DDataPlotter
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """
        self.update_range()
        self.updatePlot.emit()

    def export(self, save_file_path=False):
        """Method that export the plot as a csv file
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object
        """
        # Getting the inputs of the user to export the plot + for the name of the csv file
        param_list = [
            *self.w_axis_manager.get_axes_selected(),
            *self.w_axis_manager.get_operation_selected(),
        ]

        file_name = "plot_" + self.data.symbol + "_" + "_".join(param_list)

        default_file_path = file_name + ".csv"

        # Opening a dialog window to select the directory where the file will be saved if we are not testing
        if save_file_path == False:
            save_file_path = QFileDialog.getSaveFileName(
                self,
                self.tr("Export plot data"),
                default_file_path,
                filter="csv (*.csv)",
            )[0]
        else:
            save_file_path += "\\" + default_file_path

        # Exporting the file to the right folder
        if save_file_path not in ["", False]:
            save_path = dirname(save_file_path)
            file_name = basename(save_file_path).split(".")[0]
            try:
                self.data.export_along(
                    *param_list, save_path=save_path, file_name=file_name
                )
            except Exception as e:
                # Displaying the error inside  abox instead of the console
                err_msg = "Error while exporting Data:\n" + str(e)

                QMessageBox().critical(
                    self,
                    self.tr("Error"),
                    err_msg,
                )

    def get_plot_info(self):
        """Method that gather all the information necessary to plot the new graph.
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        Output
        ----------
        data : DataND
            DataND object that we want to plot
        axes_selected : list
            a list of string corresponding to the axis/axes of the new plot
        data_selection : list
            a list of string corresponding to the operations on the remaining axes for the new plot
        output_range : dict
            a dictionnary with all the info related to WDataRange for the new plot
        """

        # Recovering the axis selected and their units
        axes_selected = self.w_axis_manager.get_axes_selected()

        # Recovering the operation on the other axes
        data_selection = self.w_axis_manager.get_operation_selected()

        # Recovering the operation on the field values
        output_range = self.w_range.get_field_selected()

        return self.data, axes_selected, data_selection, output_range

    def set_auto_refresh(self):
        """Method that update the refresh policy according to the checkbox inside the UI

        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """

        self.is_auto_refresh = self.c_auto_refresh.isChecked()

    def set_info(self, data, user_input_list, user_input_dict):
        """Method that use the info given by DDataPlotter to setup the widget

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
        data : DataND or VectorField object
            A DataND/VectorField object to plot
        user_input_list:
            list of RequestedAxis which are the info given for the autoplot (for the axes and DataSelection)
        user_input_dict:
            dict of info which are given for the auto-plot (setting up WDataRange)
        """
        # Recovering the object that we want to show
        self.data = data

        # Setting the auto_refresh functionality to False by default
        self.is_auto_refresh = False

        # Dynamic import to avoid import loop
        VectorField = import_class("SciDataTool.Classes", "VectorField")

        # Hide or show the comboBox related to the component of a VectorField
        if isinstance(data, VectorField):
            self.data_obj = data  # storing the Vectorfield with all the components while data will only have one component
            self.w_vect_selector.show()
            # Adding/removing axial and comp_z depending on the VectorField object
            self.w_vect_selector.update(self.data_obj)
            self.w_vect_selector.refreshComponent.connect(self.update_component)
            if "component" in user_input_dict:
                self.w_vect_selector.set_component(user_input_dict)
                self.update_component()
            else:
                self.update_component()
        else:
            self.w_vect_selector.hide()

        self.w_axis_manager.set_axis_widgets(self.data, user_input_list)
        self.update_range(user_input_dict)

    def update_component(self):
        """Method that update data according to the component selected in w_vect_selector.
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """
        component_name = self.w_vect_selector.get_component_selected()

        if component_name in ["radial", "tangential", "axial"]:
            self.data = self.data_obj.to_rphiz().components[component_name]
        elif component_name in ["comp_x", "comp_y", "comp_z"]:
            self.data = self.data_obj.to_xyz().components[component_name]

        self.w_axis_manager.set_axis_widgets(self.data, list())

    def update_plot(self):
        """Method that update the plot according to the info selected in the UI
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """
        # Emitting a signal meaning that the plot must be updated
        self.updatePlot.emit()

    def update_range(self, user_input_dict=dict()):
        """Method that will update the range widget with either the user input or the default value of the DataND object
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object
        """
        self.w_range.blockSignals(True)

        # Recovering the axis selected and their units
        axes_selected = self.w_axis_manager.get_axes_selected()
        # Recovering the operation on the other axes
        data_selection = self.w_axis_manager.get_operation_selected()

        # Updating the name of the groupBox according to the number of axes selected
        if len(axes_selected) == 1:
            self.w_range.g_range.setTitle("Y")
        elif len(axes_selected) == 2:
            self.w_range.g_range.setTitle("Z")

        # Setting the WDataRange by sending the necessary info to the widget
        self.w_range.set_range(self.data, axes_selected, data_selection)

        # If user inputs have been sent (auto plot), then we modify the WDataRange according to these info
        if len(user_input_dict) != 0:
            self.w_range.set_range_user_input(user_input_dict)

        self.w_range.blockSignals(False)
