from PySide2.QtWidgets import QWidget
from matplotlib.figure import Figure

from SciDataTool.Classes.VectorField import VectorField
import matplotlib.pyplot as plt

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
    if "_" in string or "^" in string:
        string = r"$" + string + "$"
    return string


class DDataPlotter(Ui_DDataPlotter, QWidget):
    """Main windows of to plot a Data object"""

    def __init__(self, data, is_auto_refresh=False):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
        data : DataND
            A DataND object to plot
        is_auto_refresh : bool
            True to remove
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        # Recovering the object that we want to show
        self.data = data
        self.is_auto_refresh = is_auto_refresh

        # Initializing the figure inside the UI
        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)

        # Building the interaction with the UI
        self.b_refresh.clicked.connect(self.update_plot)
        self.w_axis_manager.set_axes(self.data)
        self.w_range.set_range(self.data)

        self.update_plot()

        # Linking the signals for the autoRefresh
        self.c_autoRefresh.toggled.connect(self.updateAutoRefresh)
        self.w_axis_manager.refreshNeeded.connect(self.autoUpdate)
        self.w_range.refreshNeeded.connect(self.autoUpdate)

    def autoUpdate(self):
        """Method that checks if the autorefresh is enabled.If true; then it updates the plot.
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """

        if self.is_auto_refresh == True:
            self.update_plot()

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

        # Hide or show the ComboBox related to the component of a VectorField
        if not isinstance(self.data, VectorField):
            self.w_vect_selector.hide()
        else:
            self.w_vect_selector.show()

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

    def updateAutoRefresh(self):
        """Method that update the refresh policy by enabling or disabling the autorefresh of the plot

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """

        self.is_auto_refresh = self.c_autoRefresh.isChecked()

    def update_plot(self):
        """Method that update the plot according to the info given by the user
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """
        # Clear plots
        for i in reversed(range(self.plot_layout.count())):
            if self.plot_layout.itemAt(i).widget() is not None:
                widgetToRemove = self.plot_layout.itemAt(i).widget()
                # widgetToRemove.setParent(None)
                widgetToRemove.deleteLater()

        # plt.close()
        if self.fig.get_axes():
            self.fig.clear()

        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)

        # Recovering the axis selected and their units
        axes_selected = self.w_axis_manager.get_axes_selected()
        print(axes_selected)

        # Recovering the operation on the other axes
        data_selection = self.w_axis_manager.get_dataselection_action()
        print(data_selection)

        # Recovering the operation on the field values
        output_range = self.w_range.get_field_selected()
        print(output_range)

        if len(axes_selected) == 1:
            self.data.plot_2D_Data(
                axes_selected[0],
                data_selection[0],
                data_selection[1],
                unit=output_range["unit"],
                fig=self.fig,
                ax=self.ax,
                # y_min=output_range["min"],
                # y_max=output_range["max"],
            )

        if len(axes_selected) == 2:
            self.data.plot_3D_Data(
                axes_selected[0],
                axes_selected[1],
                data_selection[0],
                unit=output_range["unit"],
                fig=self.fig,
                ax=self.ax,
                is_2D_view=True,
                # y_min=output_range["min"],
                # y_max=output_range["max"],
            )
