from PySide2.QtWidgets import QWidget
from SciDataTool.Functions import parser

from ...GUI.DDataPlotter.Ui_DDataPlotter import Ui_DDataPlotter
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from ...Functions.Plot.init_fig import init_fig
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
    """Main window of the SciDataTool UI"""

    def __init__(
        self,
        data,
        user_input_list,
        user_input_dict,
        is_auto_refresh=False,
    ):
        """Initialize the UI according to the input given by the user

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

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        self.is_auto_refresh = is_auto_refresh

        # Initializing the figure inside the UI
        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)

        # Initializing the WPlotManager
        self.w_plot_manager.set_info(data, user_input_list, user_input_dict)

        # Building the interaction with the UI and the UI itself
        self.b_refresh.clicked.connect(self.update_plot)
        self.w_plot_manager.updatePlot.connect(self.auto_update)
        self.update_plot()

        # Adding an argument for testing autorefresh
        self.is_plot_updated = False
        self.c_auto_refresh.toggled.connect(self.set_auto_refresh)

    def auto_update(self):
        """Method that checks if the autorefresh is enabled. If true, then it updates the plot.
        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

        """
        if self.is_auto_refresh == True:
            self.update_plot()
            self.is_plot_updated = True
        else:
            self.is_plot_updated = False

    def set_auto_refresh(self):
        """Method that update the refresh policy according to the checkbox inside the UI

        Parameters
        ----------
        self : WPlotManager
            a WPlotManager object

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

            # Recovering the input of the user
            [
                self.data,
                axes_selected,
                _,
                _,
            ] = self.w_plot_manager.get_plot_info()

            # Checking if the axes are following the order inside the data object
            axes_selected_parsed = parser.read_input_strings(
                axes_selected, axis_data=None
            )

            if axes_selected_parsed[0].name.lower() in SYMBOL_DICT:
                xlabel = latex(SYMBOL_DICT[axes_selected_parsed[0].name.lower()])
            else:
                xlabel = latex(axes_selected_parsed[0].name)
            xunit = "[" + latex(axes_selected_parsed[0].unit) + "]"

            if len(axes_selected) == 2:
                if axes_selected_parsed[1].name.lower():
                    ylabel = latex(SYMBOL_DICT[axes_selected_parsed[1].name.lower()])
                else:
                    ylabel = latex(axes_selected_parsed[1].name)
                yunit = "[" + latex(axes_selected_parsed[1].unit) + "]"

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

        # Recovering the input of the user
        [
            self.data,
            axes_selected,
            data_selection,
            output_range,
        ] = self.w_plot_manager.get_plot_info()

        # Checking if the axes are following the order inside the data object
        axes_selected_parsed = parser.read_input_strings(axes_selected, axis_data=None)
        axes_name = [ax.name for ax in self.data.get_axes()]
        not_in_order = False
        if (
            len(axes_selected) == 2
            and axes_selected_parsed[0].name in axes_name
            and axes_selected_parsed[1].name in axes_name
        ):
            if axes_name.index(axes_selected_parsed[0].name) > axes_name.index(
                axes_selected_parsed[1].name
            ):
                not_in_order = True
                axes_selected = [axes_selected[1], axes_selected[0]]

        # To improve the code, we use a list with the inputs of the user to pass as parameters thanks to *list
        if not None in data_selection:
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
                    is_switch_axes=not_in_order,
                )

        else:
            print("Operation not implemented yet, plot could not be updated")
