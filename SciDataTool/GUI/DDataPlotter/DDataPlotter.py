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
        # is_auto_refresh = False

        # Initializing the figure inside the UI
        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)

        # Building the interaction with the UI
        self.b_refresh.clicked.connect(self.update_plot)
        self.w_axis_manager.set_axes(self.data)
        self.w_range.set_range(self.data)

        # if is_auto_refresh:
        # Update Graph
        #     refreshNeeded.connect(self.refresh)
        # else:  # Enable refresh button
        #     refreshNeeded.connect(refresh_enable)

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
        # print(axes_selected)

        # Recovering the operation on the other axes
        data_selection = self.w_axis_manager.get_dataselection_action()
        # print(data_selection)

        # Recovering the operation on the field values
        output_range = self.w_range.get_field_selected()
        # print(output_range)

        if len(axes_selected) == 1:
            self.data.plot_2D_Data(
                axes_selected[0],
                data_selection[0],
                data_selection[1],
                unit=output_range["unit"],
                fig=self.fig,
                ax=self.ax,
            )

        if len(axes_selected) == 2:
            self.data.plot_3D_Data(
                axes_selected[0],
                axes_selected[1],
                data_selection[0],
                unit=output_range["unit"],
                fig=self.fig,
                ax=self.ax,
            )
