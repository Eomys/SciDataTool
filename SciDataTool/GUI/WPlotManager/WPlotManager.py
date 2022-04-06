from PySide2.QtWidgets import QWidget, QFileDialog, QMessageBox, QVBoxLayout
from PySide2.QtCore import Signal
from PySide2.QtCore import QByteArray, Qt
from PySide2.QtCore import QThread
from PySide2.QtGui import QMovie
from PySide2.QtWidgets import (
    QFileDialog,
    QLabel,
    QSizePolicy,
    QMessageBox,
)

from os.path import dirname, basename, join, isfile
from SciDataTool.Functions.Load.import_class import import_class
from SciDataTool.Functions.is_axes_in_order import is_axes_in_order
from SciDataTool.GUI.Tools.SaveGifWorker import SaveGifWorker
import matplotlib.pyplot as plt

from SciDataTool.GUI.WPlotManager.Ui_WPlotManager import Ui_WPlotManager

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
    updatePlotForced = Signal()

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

        self.default_file_path = None  # Path to export in csv
        self.param_dict = dict()  # Dict with param for animation to animation
        module = __import__("SciDataTool")
        DATA_DIR = getattr(module, "DATA_DIR")
        self.save_path = DATA_DIR  # Path to directory where animation are stored
        self.path_to_image = None  # Path to recover the image for the animate button
        self.main_widget = None

        self.is_test = False  # Used in test to disable showing the animation
        self.gif_path_list = list()  # List of path to the gifs created (used in test)
        self.logger = None

        # Storing each animation as a list with a QMovie, a QLabel and the path to the gif inside gif_widget_list
        self.gif_widget_list = list()

        # Building the interaction with the UI and the UI itself
        self.w_axis_manager.refreshRange.connect(self.update_range)
        self.b_export.clicked.connect(self.export)

        # Linking the signals for the autoRefresh
        self.w_axis_manager.refreshNeeded.connect(self.auto_update)
        self.w_axis_manager.generateAnimation.connect(self.gen_animate)
        self.w_range.refreshNeeded.connect(self.auto_update)

    def auto_update(self):
        """Method that update range before sending the signal to update the plot. The auto-refresh policy will be handled in the DDataPlotter
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """
        self.updatePlot.emit()

    def close_gif(self, ev, animation_label_closed):
        """Stops the gif and closes the pop up running"""

        for idx in range(len(self.gif_widget_list)):

            animation_label = self.gif_widget_list[idx][1]

            if animation_label == animation_label_closed:
                gif_widget = self.gif_widget_list[idx][0]
                widget = self.gif_widget_list[idx][3]
                break

        # Stopping the animation and resetting the gif widget (QMovie)
        gif_widget.stop()
        gif_widget.setParent(None)
        gif_widget = None
        # Closing and resetting to None the windows that pops up to show animation
        animation_label.close()
        animation_label.setParent(None)
        animation_label = None

        # Closing the widget containing the animation
        widget.close()
        widget.setParent(None)
        widget = None

        # Removing the animation from the list
        self.gif_widget_list.pop(idx)

    def close_all_gif(self):
        """Method used to close all the gif currently running. Only used in test for now"""

        for _, _, _, widget in self.gif_widget_list:
            widget.close()

    def display_gif(self, gif):
        "Method that create a display an animation and store it inside gif_widget_list"

        # Creating widget and layout that will contain the animation and its path
        widget = QWidget()
        layout = QVBoxLayout()

        # Adding the animation (QMovie inside a QLabel) inside the widget
        new_gif_widget = QMovie(gif, QByteArray(), self)
        new_gif_widget.setCacheMode(QMovie.CacheAll)
        new_gif_widget.setSpeed(100)
        # set up the movie screen on a label
        new_animation_label = QLabel(self, Qt.Window)

        # expand and center the label
        new_animation_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        new_animation_label.setAlignment(Qt.AlignCenter)
        new_animation_label.setMovie(new_gif_widget)
        new_gif_widget.start()

        layout.addWidget(new_animation_label)

        # Setting size of the widget showing the animation to the size of the gif
        widget.resize(new_gif_widget.currentImage().size())

        # Setting the rest of the widget and showing it
        widget.closeEvent = lambda ev: self.close_gif(ev, new_animation_label)
        widget.setWindowTitle(gif.split("/")[-1].replace(".gif", ""))
        widget.setLayout(layout)
        if not self.is_test:
            widget.show()

        # Hiding the "Generating..." label
        self.l_loading.setHidden(True)

        # Adding the animation to the list
        self.gif_widget_list.append([new_gif_widget, new_animation_label, gif, widget])

    def gen_animate(self):
        """Methods called after clicking on animate button to generate a gif on the axis selected and display it
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        Output
        ---------
        None
        """
        # Recovering axes and operations selected
        axes_selected = self.w_axis_manager.get_axes_selected()
        operations_selected = self.w_axis_manager.get_operation_selected()

        is_3D = len(axes_selected) == 2

        if is_3D:
            not_in_order, axes_selected = is_axes_in_order(axes_selected, self.data)
            self.param_dict["is_switch_axes"] = not_in_order

        # Recovering the axis to animate (operation axis with "to_animate")
        for idx_ope in range(len(operations_selected)):
            ope = operations_selected[idx_ope]
            if "to_animate" in ope:
                animated_axis = ope.split("to_animate")[0]
                idx_animate = idx_ope

        operations_selected.pop(idx_animate)

        # Gathering the other axes and operations selected
        plot_input = [animated_axis]
        plot_input.extend(axes_selected)
        plot_input.extend(operations_selected)

        str_format = ".gif"

        # Updating the figure to make sure that we are recovering the limit of the right figure
        self.update_plot_forced()
        fig = plt.gcf()
        if is_3D and len(plt.gcf().axes) == 2:
            # If we are animating a 3D plot, then we must keep the axes limit

            self.param_dict["x_min"] = fig.axes[0].get_xlim()[0]
            self.param_dict["x_max"] = fig.axes[0].get_xlim()[1]
            self.param_dict["y_min"] = fig.axes[0].get_ylim()[0]
            self.param_dict["y_max"] = fig.axes[0].get_ylim()[1]
            self.param_dict["z_min"] = fig.axes[1].dataLim.extents[0]
            self.param_dict["z_max"] = fig.axes[1].dataLim.extents[-1]

        elif not is_3D:

            if (
                len(axes_selected) == 1
                and axes_selected[0].split("{")[0]
                in [
                    "freqs",
                    "wavenumber",
                ]
                and len(plt.gcf().axes) == 1
            ):
                # if we are animating an FFT plot then we set the limit according to the current figure
                self.param_dict["x_min"] = fig.axes[0].get_xlim()[0]
                self.param_dict["x_max"] = fig.axes[0].get_xlim()[1]
                self.param_dict["y_min"] = fig.axes[0].get_ylim()[0]
                self.param_dict["y_max"] = fig.axes[0].get_ylim()[1]

            else:
                # if we animate a regular 2D plot then we set the limit on y-axis later
                self.param_dict["y_min"] = None
                self.param_dict["y_max"] = None

        # Recovering the suptitle of the figure and adding to the animation
        if fig._suptitle is not None:
            suptitle_ref = fig._suptitle._text
        else:
            suptitle_ref = ""

        # Recovering the name of the gif if not already given
        # if self.default_file_path is None:
        gif_name = self.get_file_name()

        # Recovering "Generating label" from the WSliceOperator with the axis that we want to animate
        for wid in self.w_axis_manager.w_slice_op:
            if wid.axis_name == animated_axis.split("[")[0]:
                self.l_loading = wid.l_loading

        gif = self.save_path + "/" + gif_name + str_format
        gif = gif.replace("\\", "/")

        # Using an index to make sure that we are generating a new gif everytime
        idx = 1
        while gif in self.gif_path_list:
            gif = gif.split(".")[0].split("(")[0] + "(" + str(idx) + ")" + str_format
            idx += 1

        self.gif_path_list.append(gif)

        # Indicating the path to the .gif in the console
        if self.logger is not None:
            self.logger.info("Gif stored at: " + gif)
        else:
            print("Gif stored at: " + gif)

        # Generating a new animation each time
        # Creating a QThread associated to the worker saving the gif
        self.th = QThread(parent=self)
        self.worker = SaveGifWorker(
            widget=self,
            main_widget=self.main_widget,
            gif=gif,
            plot_input=plot_input,
            data_selection=operations_selected,
            is_3D=is_3D,
            suptitle_ref=suptitle_ref,
        )
        self.worker.moveToThread(self.th)

        # Connecting the end of generation of GIF to display, end thread and killing process
        self.worker.gif_available.connect(self.th.finished)
        self.worker.gif_available.connect(lambda: self.worker.kill_worker())
        self.worker.gif_available.connect(lambda: self.display_gif(gif))

        self.th.started.connect(self.worker.run)
        self.th.finished.connect(self.th.quit)
        self.th.start()

        # Showing "Generating..." under the animate button
        self.l_loading.setHidden(False)

    def get_file_name(self):
        """Method that create the name of the file with the name of the field selected"""

        file_name = self.data.name
        file_name = file_name.replace("{", "[").replace("}", "]").replace(".", ",")

        return file_name

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

        if self.default_file_path is None:
            file_name = self.get_file_name()
            default_file_path = file_name + ".csv"
        else:
            default_file_path = self.default_file_path + ".csv"

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

    def set_info(
        self,
        data,
        axes_request_list=list(),
        component=None,
        unit=None,
        z_min=None,
        z_max=None,
        frozen_type=0,
        is_keep_config=False,
        is_quiver=False,
        plot_arg_dict=dict(),
        save_path="",
        logger=None,
        path_to_image=None,
        main_widget=None,
    ):
        """Method that use the info given by DDataPlotter to setup the widget

        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object
        data : DataND or VectorField object
            A DataND/VectorField object to plot
        axes_request_list:
            list of RequestedAxis which are the info given for the autoplot (for the axes and DataSelection)
        component : str
            Name of the component to plot (For VectorField only)
        unit : str
            unit in which to plot the field
        z_min : float
            Minimum value for Z axis (or Y if only one axe)
        z_max : float
            Minimum value for Z axis (or Y if only one axe)
        frozen_type : int
            0 to let the user modify the axis of the plot, 1 to let him switch them, 2 to not let him change them, 3 to freeze both axes and operations, 4 to freeze fft
        plot_arg_dict : dict
            Dictionnary with arguments that must be given to the plot (used for animated plot)
        save_path : str
            path to the folder where the animations are saved
        logger : logger
            logger used to print path to animation (if None using print instead)
        path_to_image : str
            path to the folder where the image for the animation button is saved
        """
        self.main_widget = main_widget
        # Recovering the object that we want to show and how we want to show it
        self.data = data
        self.param_dict = plot_arg_dict.copy()
        if save_path != "":
            self.save_path = save_path

        self.logger = logger
        self.path_to_image = path_to_image

        # Dynamic import to avoid import loop
        VectorField = import_class("SciDataTool.Classes", "VectorField")

        # Hide or show the comboBox related to the component of a VectorField
        if isinstance(data, VectorField):
            self.data_obj = data  # storing the Vectorfield with all the components while data will only have one component
            self.w_vect_selector.show()
            # Adding/removing axial and comp_z depending on the VectorField object
            self.w_vect_selector.update(self.data_obj)
            self.w_vect_selector.refreshComponent.connect(self.update_component)
            if component is not None:
                self.w_vect_selector.set_component(component)
                self.update_component(is_update_plot=False)
            else:
                self.update_component(is_update_plot=False)
            # Add "all" components in case of quiver plot
            if is_quiver:
                self.w_vect_selector.c_component.blockSignals(True)
                self.w_vect_selector.c_component.insertItem(0, "all")
                self.w_vect_selector.c_component.setCurrentIndex(0)
                self.w_vect_selector.c_component.blockSignals(False)
        else:
            self.w_vect_selector.hide()

        self.w_axis_manager.set_axis_widgets(
            self.data,
            axes_request_list,
            frozen_type,
            is_keep_config=is_keep_config,
            path_to_image=self.path_to_image,
        )
        self.update_range(
            unit=unit,
            z_min=z_min,
            z_max=z_max,
        )

        if is_keep_config:
            self.update_plot()

    def update_component(self, is_update_plot=True):
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
        elif component_name == "all":
            self.data = self.data_obj.components[
                list(self.data_obj.components.keys())[0]
            ]

        self.w_range.set_range(self.data)

        # Force plot refresh
        if is_update_plot:
            self.update_plot_forced()

    def update_plot(self):
        """Method that update the plot according to the info selected in the UI
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """
        # Emitting a signal meaning that the plot must be updated
        self.updatePlot.emit()

    def update_plot_forced(self):
        """Method that update the plot according to the info selected in the UI
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """
        # Emitting a signal meaning that the plot must be updated
        self.updatePlotForced.emit()

    def update_range(self, unit=None, z_min=None, z_max=None):
        """Method that will update the range widget with either the user input or the default value of the DataND object
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object
        unit : str
            unit in which to plot the field
        z_min : float
            Minimum value for Z axis (or Y if only one axe)
        z_max : float
            Minimum value for Z axis (or Y if only one axe)
        """
        self.w_range.blockSignals(True)

        # Recovering the axis selected and their units
        axes_selected = self.w_axis_manager.get_axes_selected()
        # Recovering the operation on the other axes
        data_selection = self.w_axis_manager.get_operation_selected()

        # Updating the name of the groupBox according to the number of axes selected
        if len(axes_selected) == 1:
            self.w_range.g_range.setTitle("Y Range")
        elif len(axes_selected) == 2:
            self.w_range.g_range.setTitle("Z Range")

        # Setting the WDataRange by sending the necessary info to the widget
        self.w_range.set_range(self.data, unit=unit)

        # If user inputs have been sent (auto plot), then we modify the WDataRange according to these info
        if z_min is not None or z_max is not None:
            self.w_range.set_range_user_input(z_min=z_min, z_max=z_max)

        self.w_range.blockSignals(False)
