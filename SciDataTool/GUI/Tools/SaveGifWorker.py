from PySide2.QtCore import QObject, Signal, Slot
from SciDataTool.GUI.Tools.ThreadKillable import ThreadKillable
import multiprocessing
from SciDataTool.GUI.Tools.GifHandler import GifHandler
from logging.handlers import QueueListener


def save_gif(queue, widget, plot_input):

    animated_axis = plot_input.pop(0)

    widget.param_dict["save_path"] = widget.gif
    if "component_list" in widget.param_dict:
        widget.param_dict.pop("component_list")

    widget.data.plot_2D_Data_Animated(animated_axis, *plot_input, **widget.param_dict)
    queue.put("gif generated")


class SaveGifWorker(QObject):
    """Worker that saves a gif plot"""

    gif_available = Signal()

    def __init__(self, widget=None, plot_input=list()):
        super().__init__()
        self.widget = widget
        self.plot_input = plot_input
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
                self.plot_input,
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
