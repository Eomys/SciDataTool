from PySide2.QtWidgets import QWidget
from matplotlib.figure import Figure

from ...GUI.DDataPlotter.Ui_DDataPlotter import Ui_DDataPlotter
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar,)


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

        self.data = data

        self.fig = Figure()
        self.set_figure(self.fig)

        self.b_refresh.clicked.connect(self.update_plot)

    def set_figure(self, fig):
        "Method that set up the figure inside the GUI"
        # Set plot layout
        self.canvas = FigureCanvas(fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        

        self.plot_layout.addWidget(self.toolbar)
        self.plot_layout.addWidget(self.canvas)




    def update_plot(self):
        """Method that update the plot according to the info given by the user"""

        self.canvas.draw(self.data.plot_2D_Data("time"))
        
