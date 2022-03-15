import logging


class GifHandler(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def emit(self, record):
        """Send signal gif_available to specify the end of the gif generation"""
        self.parent.gif_available.emit()
