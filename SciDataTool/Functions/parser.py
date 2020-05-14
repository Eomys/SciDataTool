# -*- coding: utf-8 -*-
from numpy import pi, sqrt  # for eval
from SciDataTool.Functions import AxisError


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
        axis_unit = "{SI}"
        # Detect unit
        if "{" in axis_str:
            elems = axis_str.split("{")
            axis_unit = "{" + elems[1]
            axis_str = elems[0]
        # Detect axis_data input
        if "axis_data" in axis_str:
            elems = axis_str.split("=axis_data")
            try:
                axes_list.append(
                    [
                        elems[0],
                        axis_unit,
                        "interval",
                        "values",
                        axis_data[int(elems[1]) - 1],
                    ]
                )
            except:
                try:
                    axes_list.append(
                        [elems[0], axis_unit, "interval", "values", axis_data[0]]
                    )
                except:
                    raise AxisError("ERROR: Absence of axis_data")
        # Detect interval
        elif "=[" in axis_str:
            elems = axis_str.split("=[")
            elems2 = elems[1].split(",")
            init_str = elems2[0]
            interval_init = eval(init_str)
            final_str = elems2[1].strip("]")
            interval_final = eval(final_str)
            axes_list.append(
                [
                    elems[0],
                    axis_unit,
                    "interval",
                    "values",
                    [interval_init, interval_final],
                ]
            )
        # Detect single value
        elif "=" in axis_str:
            elems = axis_str.split("=")
            axes_list.append(
                [elems[0], axis_unit, "single", "values", [eval(elems[1])]]
            )
        # Detect index input...
        elif "[" in axis_str:
            elems = axis_str.split("[")
            ind_str = elems[1].strip("]")
            # Range of indices
            if ":" in ind_str:
                elems2 = ind_str.split(":")
                indices = [i for i in range(int(elems2[0]), int(elems2[1]) + 1)]
                axes_list.append([elems[0], axis_unit, "interval", "indices", indices])
            # List of indices
            if "," in ind_str:
                indices = ind_str.split(",")
                axes_list.append([elems[0], axis_unit, "list", "indices", indices])
            # Single index
            else:
                indices = [int(ind_str)]
                axes_list.append([elems[0], axis_unit, "single", "indices", indices])
        # Whole axis
        else:
            axes_list.append([axis_str, axis_unit, "interval", "values", "whole"])
    return axes_list
