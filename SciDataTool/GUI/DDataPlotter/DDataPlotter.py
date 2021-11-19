from PySide2.QtWidgets import QWidget
from matplotlib.figure import Figure

from ...GUI.DDataPlotter.Ui_DDataPlotter import Ui_DDataPlotter
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from ...Functions.Plot.init_fig import init_fig
from matplotlib.widgets import Cursor
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.collections import PathCollection, QuadMesh
from numpy import array

from ...Functions.Plot import TEXT_BOX

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


class DDataPlotter(Ui_DDataPlotter, QWidget):
    """Main windows of the SciDataTool UI"""

    def __init__(
        self,
        data,
        user_input_list,
        user_input_dict,
        is_auto_refresh=False,
        is_VectorField=False,
    ):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
        data : DataND
            A DataND object to plot
        user_input_list:
            list of RequestedAxis which are the info given for the autoplot (for the axes and DataSelection)
        user_input_dict:
            dict of info which are given for the auto-plot (setting up WDataRange)
        is_auto_refresh : bool
            True to remove
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        # Recovering the object that we want to show
        self.data = data
        self.is_auto_refresh = is_auto_refresh

        # Adding an argument for testing autorefresh
        self.is_plot_updated = False

        # Initializing the figure inside the UI
        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)

        # Hide or show the ComboBox related to the component of a VectorField
        if is_VectorField:
            self.data_obj = data  # storing the Vectorfield with all the components while data will only have one component
            self.w_vect_selector.show()
            self.w_vect_selector.update(self.data_obj)
            self.w_vect_selector.refreshComponent.connect(self.update_component)
            self.update_component()
        else:
            self.w_vect_selector.hide()

        # If only one axis is given with the object, then we hide w_axis_2
        if len(self.data.get_axes()) == 1:
            self.w_axis_manager.w_axis_2.hide()
            self.w_axis_manager.g_data_extract.hide()
        else:
            self.w_axis_manager.w_axis_2.show()
            self.w_axis_manager.g_data_extract.show()

        # Building the interaction with the UI and the UI itself
        self.b_refresh.clicked.connect(self.update_plot)
        self.w_axis_manager.refreshRange.connect(self.update_range)

        self.w_axis_manager.set_axis_widgets(self.data, user_input_list)
        self.update_range(user_input_dict)
        self.update_plot()

        # Linking the signals for the autoRefresh
        self.c_auto_refresh.toggled.connect(self.set_auto_refresh)
        self.w_axis_manager.refreshNeeded.connect(self.auto_update)
        self.w_range.refreshNeeded.connect(self.auto_update)

    def update_component(self):
        """Method that update data according to the component selected in w_vect_selector.
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """
        component_name = self.w_vect_selector.get_component_selected()

        if component_name in ["radial", "tangential", "axial"]:
            self.data = self.data_obj.to_rphiz().components[component_name]
        elif component_name in ["comp_x", "comp_y", "comp_z"]:
            self.data = self.data_obj.to_xyz().components[component_name]

        self.w_axis_manager.set_axis_widgets(self.data, list())

    def auto_update(self):
        """Method that checks if the autorefresh is enabled.If true; then it updates the plot.
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """

        if self.is_auto_refresh == True:
            self.update_range()
            self.update_plot()
            self.is_plot_updated = True
        else:
            self.is_plot_updated = False

    def set_auto_refresh(self):
        """Method that update the refresh policy according to the checkbox inside the UI

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """

        self.is_auto_refresh = self.c_auto_refresh.isChecked()

    def set_figure(self, fig):
        """Method that set up the figure inside the GUI

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
        fig : Figure
            A Figure object to put inside the UI

        """
        # Set plot layout
        self.canvas = FigureCanvas(fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot_layout.addWidget(self.toolbar)
        self.plot_layout.addWidget(self.canvas)

        self.text = None
        self.circle = None
        self.line = None

        # Set labels for cursor and coordinates
        ######################################
        def format_coord(x, y, z=None, sep=", "):
            if (
                self.w_axis_manager.w_axis_1.get_current_axis_name().lower()
                in SYMBOL_DICT
            ):
                xlabel = latex(
                    SYMBOL_DICT[
                        self.w_axis_manager.w_axis_1.get_current_axis_name().lower()
                    ]
                )
            else:
                xlabel = latex(self.w_axis_manager.w_axis_1.get_current_axis_name())
            xunit = "[" + latex(self.w_axis_manager.w_axis_1.get_current_unit()) + "]"

            if self.w_axis_manager.w_axis_2.get_current_axis_name() != "None":
                if (
                    self.w_axis_manager.w_axis_2.get_current_axis_name().lower()
                    in SYMBOL_DICT
                ):
                    ylabel = latex(
                        SYMBOL_DICT[
                            self.w_axis_manager.w_axis_2.get_current_axis_name().lower()
                        ]
                    )
                else:
                    ylabel = latex(self.w_axis_manager.w_axis_2.get_current_axis_name())
                yunit = (
                    "[" + latex(self.w_axis_manager.w_axis_2.get_current_unit()) + "]"
                )

            else:
                ylabel = self.data.symbol

                if self.data._name.lower() in SYMBOL_DICT:
                    ylabel = latex(SYMBOL_DICT[self.data._name.lower()])

                yunit = "[" + latex(self.data.unit) + "]"

                if ylabel == "W" and "dBA" in yunit:
                    ylabel = "ASWL"
                elif ylabel == "W" and "dB" in yunit:
                    ylabel = "SWL"

            label = (
                xlabel
                + " = "
                + format(x, ".4g")
                + " "
                + xunit
                + sep
                + ylabel
                + " = "
                + format(y, ".4g")
                + " "
                + yunit
            )

            if z is not None:
                if hasattr(self, "data") and self.data is not None:
                    zlabel = latex(self.data.symbol)
                elif self.data._name.lower() in SYMBOL_DICT:
                    zlabel = latex(SYMBOL_DICT[self.data._name.lower()])
                else:
                    zlabel = latex(self.data._name)

                zunit = "[" + latex(self.data.unit) + "]"

                if zlabel == "W" and "dBA" in zunit:
                    zlabel = "ASWL"
                elif zlabel == "W" and "dB" in zunit:
                    zlabel = "SWL"

                label += sep + zlabel + " = " + format(z, ".4g") + " " + zunit

            # Remove latex marks for top right corner
            if sep == ", ":
                label = label.replace("$", "").replace("{", "").replace("}", "")

            return label

        # Set cursor
        ######################################
        def set_cursor(event):
            plot_obj = event.artist
            Z = None
            if isinstance(plot_obj, Line2D):
                ind = event.ind
                xdata = plot_obj.get_xdata()
                ydata = plot_obj.get_ydata()
                X = xdata[ind][0]  # X position of the click
                Y = ydata[ind][0]  # Y position of the click
            elif isinstance(plot_obj, PathCollection):
                ind = event.ind
                X = plot_obj.get_offsets().data[ind][0][0]
                Y = plot_obj.get_offsets().data[ind][0][1]
                Z = plot_obj.get_array().data[ind][0]
            elif isinstance(plot_obj, Rectangle):
                X = plot_obj.get_x() + plot_obj.get_width() / 2
                Y = plot_obj.get_height()
            elif isinstance(plot_obj, QuadMesh):
                ind = event.ind
                if plot_obj._coordinates.shape[0] > 2:
                    # pcolormesh case
                    l = ind[0] // plot_obj._coordinates.shape[1]
                    X = plot_obj._coordinates[
                        l, ind[0] - l * plot_obj._coordinates.shape[1] + 1, 0
                    ]
                    Y = plot_obj._coordinates[
                        l, ind[0] - l * plot_obj._coordinates.shape[1] + 1, 1
                    ]
                else:
                    X = (
                        plot_obj._coordinates[0, ind[0] + 1, 0]
                        + plot_obj._coordinates[1, ind[0] + 1, 0]
                    ) / 2
                    Y = (
                        plot_obj._coordinates[0, ind[0] + 1, 1]
                        + plot_obj._coordinates[1, ind[0] + 1, 1]
                    ) / 2
                Z = plot_obj.get_array().data[ind[0]]

            # Offset for the label
            x_min, x_max = self.ax.get_xlim()
            dx = (x_max - x_min) / 50
            if X is not None and Y is not None:
                label = format_coord(X, Y, Z, sep="\n")
                if self.text is None:
                    # Create label in box and black cross
                    self.text = self.ax.text(
                        X + dx,
                        Y,
                        label,
                        ha="left",
                        va="center",
                        bbox=TEXT_BOX,
                    )
                    # Draw line
                    self.line = self.ax.plot(
                        [X, X + dx],
                        [Y, Y],
                        color="k",
                        linestyle="-",
                        linewidth=0.5,
                    )
                    # Draw circle
                    self.circle = self.ax.plot(
                        X,
                        Y,
                        ".",
                        markerfacecolor="w",
                        markeredgecolor="k",
                        markeredgewidth=0.5,
                        markersize=12,
                    )
                else:
                    # Update label, line and circle
                    self.text._x = X + dx
                    self.text._y = Y
                    self.text._text = label
                    self.circle[0].set_xdata(array(X))
                    self.circle[0].set_ydata(array(Y))
                    self.line[0].set_xdata(array([X, X + dx]))
                    self.line[0].set_ydata(array([Y, Y]))

            self.ax.texts[-1].set_visible(True)
            self.ax.lines[-1].set_visible(True)
            self.ax.lines[-2].set_visible(True)
            self.canvas.draw()

        def delete_cursor(event):
            if event.button.name == "RIGHT":
                if self.text is not None:
                    self.ax.texts[-1].set_visible(False)
                if self.line is not None:
                    self.ax.lines[-1].set_visible(False)
                if self.circle is not None:
                    self.ax.lines[-2].set_visible(False)
            self.canvas.draw()

        self.ax.format_coord = format_coord
        self.canvas.mpl_connect("pick_event", set_cursor)
        self.canvas.mpl_connect("button_press_event", delete_cursor)

    def update_plot(self):
        """Method that update the plot according to the info selected in the UI
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """
        # Clear plots
        for i in reversed(range(self.plot_layout.count())):
            if self.plot_layout.itemAt(i).widget() is not None:
                widgetToRemove = self.plot_layout.itemAt(i).widget()
                widgetToRemove.deleteLater()

        if self.fig.get_axes():
            self.fig.clear()

        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)

        # Recovering the axis selected and their units
        axes_selected = self.w_axis_manager.get_axes_selected()

        # Recovering the operation on the other axes
        data_selection = self.w_axis_manager.get_operation_selected()

        # Recovering the operation on the field values
        output_range = self.w_range.get_field_selected()

        # To improve the code, we use a list with the inputs of the user to pass as parameters thanks to *list
        # We have to take into account the
        if len(axes_selected) == 1:
            self.data.plot_2D_Data(
                *[*axes_selected, *data_selection],
                unit=output_range["unit"],
                fig=self.fig,
                ax=self.ax,
                y_min=output_range["min"],
                y_max=output_range["max"],
            )

        elif len(axes_selected) == 2:
            self.data.plot_3D_Data(
                *[*axes_selected, *data_selection],
                unit=output_range["unit"],
                fig=self.fig,
                ax=self.ax,
                is_2D_view=True,
                z_min=output_range["min"],
                z_max=output_range["max"],
            )

        else:
            print("Operation not implemented yet, plot could not be updated")

    def update_range(self, user_input_dict=dict()):
        """Method that will update the range widget with either the user input or the default value of the DataND object
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
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
