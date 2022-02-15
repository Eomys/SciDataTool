from numpy import pi, sqrt, inf  # for eval
from SciDataTool.Functions import AxisError
from SciDataTool.Classes.RequestedAxis import RequestedAxis


def read_input_strings(args, axis_data):
    """Reads the string input into the "get_along" methods to define the axes
    Parameters
    ----------
    args: list
        list of string describing the requested axes
    axis_data: ndarray
        user-input values for the axes
    Returns
    -------
    list of axes data (axes_list)
    """
    axes_list = []
    for axis_str in args:
        unit = "SI"
        values = None
        indices = None
        input_data = None
        # Detect unit
        if "{" in axis_str:
            elems = axis_str.split("{")
            unit = elems[1].strip("}")
            axis_str = elems[0]
        # Detect normalization
        if "->" in axis_str:
            elems = axis_str.split("->")
            if "=" in elems[1]:
                unit = elems[1].split("=")[0]
            elif "[" in elems[1]:
                unit = elems[1].split("[")[0]
            elif ">" in elems[1]:
                unit = elems[1].split("[")[0]
            elif "<" in elems[1]:
                unit = elems[1].split("[")[0]
            else:
                unit = elems[1]
            name = elems[0]
            axis_str = axis_str.replace("->" + unit, "")
        # Detect max
        if "max" in axis_str:
            elems = axis_str.split("=max")
            name = elems[0]
            extension = "max"
        # Detect min
        elif "min" in axis_str:
            elems = axis_str.split("=min")
            name = elems[0]
            extension = "min"
        # Detect rms sum
        elif "rss" in axis_str:
            elems = axis_str.split("=rss")
            name = elems[0]
            extension = "rss"
        # Detect sum
        elif "sum" in axis_str:
            elems = axis_str.split("=sum")
            name = elems[0]
            extension = "sum"
        # Detect rms mean
        elif "rms" in axis_str:
            elems = axis_str.split("=rms")
            name = elems[0]
            extension = "rms"
        # Detect mean
        elif "mean" in axis_str:
            elems = axis_str.split("=mean")
            name = elems[0]
            extension = "mean"
        # Detect integrate
        elif "integrate_local" in axis_str:
            elems = axis_str.split("=integrate_local")
            name = elems[0]
            extension = "integrate_local"
        elif "integrate" in axis_str:
            elems = axis_str.split("=integrate")
            name = elems[0]
            extension = "integrate"
        # Detect antiderivate
        elif "antiderivate" in axis_str:
            elems = axis_str.split("=antiderivate")
            name = elems[0]
            extension = "antiderivate"
        # Detect derivate
        elif "derivate" in axis_str:
            elems = axis_str.split("=derivate")
            name = elems[0]
            extension = "derivate"
        # Detect periods
        elif "oneperiod" in axis_str:
            elems = axis_str.split("[")
            name = elems[0]
            extension = "oneperiod"
        elif "antiperiod" in axis_str:
            elems = axis_str.split("[")
            name = elems[0]
            extension = "antiperiod"
        elif "smallestperiod" in axis_str:
            elems = axis_str.split("[")
            name = elems[0]
            extension = "smallestperiod"
        # Detect pattern
        elif "pattern" in axis_str:
            elems = axis_str.split("[")
            name = elems[0]
            extension = "pattern"
        # Detect axis_data input
        elif "axis_data" in axis_str:
            elems = axis_str.split("=axis_data")
            name = elems[0]
            extension = "axis_data"
            try:
                input_data = axis_data[name]
            except Exception:
                raise AxisError("No axis_data provided")
        # Detect above
        elif ">" in axis_str:
            elems = axis_str.split(">")
            init_str = elems[1]
            interval_init = eval(init_str)
            interval_final = inf
            name = elems[0]
            extension = "interval"
            input_data = [interval_init, interval_final]
        # Detect below
        elif "<" in axis_str:
            elems = axis_str.split("<")
            init_str = elems[1]
            interval_init = -inf
            interval_final = eval(init_str)
            name = elems[0]
            extension = "interval"
            input_data = [interval_init, interval_final]
        # Detect interval
        elif "=[" in axis_str:
            elems = axis_str.split("=[")
            elems2 = elems[1].split(",")
            if len(elems2) > 2:
                extension = "list"
                name = elems[0]
                input_data = [eval(elem.strip("]")) for elem in elems2]
            else:
                init_str = elems2[0]
                interval_init = eval(init_str)
                final_str = elems2[1].strip("]")
                interval_final = eval(final_str)
                name = elems[0]
                extension = "interval"
                input_data = [interval_init, interval_final]
        # Detect single value
        elif "=" in axis_str:
            elems = axis_str.split("=")
            name = elems[0]
            extension = "single"
            input_data = [eval(elems[1])]
        # Detect index input...
        elif "[" in axis_str:
            elems = axis_str.split("[")
            ind_str = elems[1].strip("]")
            name = elems[0]
            # Range of indices
            if ":" in ind_str:
                elems2 = ind_str.split(":")
                extension = "interval"
                indices = [i for i in range(int(elems2[0]), int(elems2[1]))]
            # List of indices
            elif "," in ind_str:
                extension = "list"
                indices = [int(x) for x in ind_str.split(",")]
            # List of all indices
            elif len(ind_str) == 0:
                extension = "list"
                indices = [":"]
            # N largest
            elif "largest" in ind_str:
                extension = "list"
                indices = [ind_str.split("largest")[0]]
            # Single index
            else:
                extension = "single"
                indices = [int(ind_str)]
        # Whole axis
        else:
            name = axis_str
            extension = "whole"
        # Detect 1/nth octave band
        if "oct" in unit:
            noct = int(unit.split("oct")[0].split("/")[1])
            unit = "SI"
        else:
            noct = None
        # RequestedAxis object creation
        axis = RequestedAxis(
            name=name,
            unit=unit,
            extension=extension,
            values=values,
            indices=indices,
            input_data=input_data,
            noct=noct,
        )
        axes_list.append(axis)
    return axes_list
