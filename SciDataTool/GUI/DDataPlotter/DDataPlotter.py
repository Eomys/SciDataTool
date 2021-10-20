from PySide2.QtWidgets import QWidget
from matplotlib.figure import Figure

from SciDataTool.Classes.VectorField import VectorField

from ...GUI.DDataPlotter.Ui_DDataPlotter import Ui_DDataPlotter
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar,)
from ...Functions.Plot.init_fig import init_fig


class DDataPlotter(Ui_DDataPlotter, QWidget):
    """Main windows of to plot a Data object"""

    def __init__(self, data):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : DDataPlotter
            a DDataPlotter object
        data : DataND
            A DataND object to plot
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        #Recovering the object that we want to show
        self.data = data

        #Initializing the figure inside the UI
        (self.fig, self.ax, _, _) = init_fig()
        self.set_figure(self.fig)
 

        #Building the interaction with the UI
        self.b_refresh.clicked.connect(self.update_plot)
        self.w_axis_1.update_axis(self.data)
        self.w_axis_2.update_axis(self.data)
        self.w_axis_2.change_name("y")

    def set_figure(self, fig):
        "Method that set up the figure inside the GUI"
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
        """Method that update the plot according to the info given by the user"""

        self.data.plot_2D_Data("time",fig = self.fig, ax=self.ax) #Mandatory to give the figure and the axes to plot
        


