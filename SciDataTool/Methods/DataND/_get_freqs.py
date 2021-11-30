from numpy import meshgrid, array

from SciDataTool.Functions import AxisError


def _get_freqs(self):
    """Returns the frequency vector or array, if available.
    Parameters
    ----------
    self: Data
        a Data object
    Returns
    -------
    freqs : frequency vector or array
    """

    axis_names = [axis.name for axis in self.axes]
    axis_norm = [list(axis.normalizations.keys()) for axis in self.axes]

    index = None
    operation = None
    index_speed = None
    index_order = None

    if "freqs" in axis_names:
        index = axis_names.index("freqs")
    elif "frequency" in axis_names:
        index = axis_names.index("frequency")
    elif "time" in axis_names:
        index = axis_names.index("frequency")
        operation = "time_to_freqs"
    elif "speed" in axis_names and "order" in axis_names:
        index_speed = axis_names.index("speed")
        index_order = axis_names.index("order")
        is_norm = False
    else:
        for i, norm in enumerate(axis_norm):
            if "speed" in norm:
                index_speed = i
                is_norm = True
        if index_speed is not None and "order" in axis_names:
            index_order = axis_names.index("order")
        else:
            raise AxisError("Cannot compute frequencies from available axes")

    if index is not None:
        freqs = self.get_axes()[index].get_values(operation=operation)
    else:  # f = speed * 60 / order
        if is_norm:
            normalization = "speed"
        else:
            normalization = None
        speed = self.get_axes()[index_speed].get_values(normalization=normalization)
        order_strings = self.get_axes()[index_order].get_values().tolist()
        orders = array([int(s.split(" ")[0].replace("H", "")) for s in order_strings])
        os, so = meshgrid(orders, speed)
        freqs = so * 60 / os

    return freqs
