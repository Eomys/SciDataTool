from PySide2.QtCore import QObject, Signal, Slot
from SciDataTool.GUI.Tools.ThreadKillable import ThreadKillable
import multiprocessing
from SciDataTool.GUI.Tools.GifHandler import GifHandler
from logging.handlers import QueueListener

from pytest import param


def save_gif(
    queue, widget, main_widget, gif, plot_input, data_selection, is_3D, suptitle_ref
):

    animated_axis = plot_input.pop(0)

    param_dict = widget.param_dict.copy()

    param_dict["save_path"] = gif

    [
        _,
        _,
        _,
        output_range,
    ] = widget.get_plot_info()

    if "type_plot" in param_dict and param_dict["type_plot"] == "quiver":
        param_dict = main_widget.plot_arg_dict.copy()
        param_dict["save_path"] = gif
        if widget.w_vect_selector.get_component_selected() != "all":
            component_list = [widget.w_vect_selector.get_component_selected()]
        else:
            component_list = None
        angle_str = "angle"
        if "is_smallestperiod" in param_dict:
            if param_dict["is_smallestperiod"]:
                angle_str = "angle[smallestperiod]"
            del param_dict["is_smallestperiod"]
        if "fig" in param_dict:
            fig = param_dict["fig"]
            ax = fig.get_axes()[0]
            del param_dict["fig"]
        else:
            fig = None
            ax = None
        if "colormap" in param_dict:
            del param_dict["colormap"]
        main_widget.data_orig.plot_2D_Data_Animated(
            animated_axis,
            *[*[angle_str], *data_selection],
            **param_dict,
            unit=output_range["unit"],
            fig=fig,
            ax=ax,
            y_min=output_range["min"],
            y_max=output_range["max"],
            component_list=component_list,
        )

    else:

        param_dict["unit"] = output_range["unit"]

        if "component_list" in param_dict:
            param_dict.pop("component_list")

        if is_3D:
            widget.data.plot_3D_Data_Animated(
                animated_axis, suptitle_ref, *plot_input, **param_dict
            )
        else:
            widget.data.plot_2D_Data_Animated(
                animated_axis, suptitle_ref, *plot_input, **param_dict
            )
    queue.put("gif generated")


class SaveGifWorker(QObject):
    """Worker that saves a gif plot"""

    gif_available = Signal()

    def __init__(
        self,
        widget=None,
        main_widget=None,
        gif="",
        plot_input=list(),
        data_selection=list(),
        is_3D=False,
        suptitle_ref="",
    ):
        super().__init__()
        self.widget = widget
        self.main_widget = main_widget
        self.gif = gif
        self.plot_input = plot_input
        self.data_selection = data_selection
        self.is_3D = is_3D
        self.suptitle_ref = suptitle_ref
        self.queue = multiprocessing.Queue()
        # used to check if the is finished
        self.queue_handler = GifHandler(parent=self)
        self.queue_listener = QueueListener(self.queue, self.queue_handler)
        self.queue_listener.start()

    @Slot()
    def run(self):
        # Setting the thread that will start the run simulation
        self.p = ThreadKillable(
            target=save_gif,
            args=(
                self.queue,
                self.widget,
                self.main_widget,
                self.gif,
                self.plot_input,
                self.data_selection,
                self.is_3D,
                self.suptitle_ref,
            ),
        )
        self.p.daemon = True
        self.p.start()

    def kill_worker(self):
        """
        Kill the worker
        Parameters
        ----------
        self: SaveGifWorker
            the worker generating the gif
        Returns
        -------

        """
        if self.queue_listener._thread is not None:
            # Stopping the queue listener
            self.queue_listener.stop()
            self.queue_listener.queue.close()
            self.queue_handler.close()
        # Closing the process (running simu or saving output
        self.p.kill()
        self.p.join()
