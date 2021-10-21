from PySide2.QtWidgets import QWidget
from matplotlib.figure import Figure

from SciDataTool.Classes.VectorField import VectorField

from ...GUI.DDataPlotter.Ui_DDataPlotter import Ui_DDataPlotter
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar,)
from ...Functions.Plot.init_fig import init_fig


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

        #Recovering the object that we want to show
        self.data = data
        # is_auto_refresh = False

        #Initializing the figure inside the UI
        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)
 

        #Building the interaction with the UI
        self.b_refresh.clicked.connect(self.update_plot)
        self.w_axis_1.update(self.data)
        self.w_axis_2.update(self.data, "Y")


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

        #Hide or show the ComboBox related to the component of a VectorField
        if not isinstance(self.data, VectorField):
            self.c_component.hide()
            self.in_component.hide()
        else:
            self.c_component.show()
            self.in_component.show()   
           
    def update_plot(self):
        """Method that update the plot according to the info given by the user
        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object

        """

        self.data.plot_2D_Data("time",fig = self.fig, ax=self.ax) #Mandatory to give the figure and the axes to plot
        


