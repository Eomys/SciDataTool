from SciDataTool.Functions.Plot import unit_dict

import csv
import numpy as np
from os.path import join

CHAR_LIST = ["$", "{", "}"]


def export_along(
    self,
    *args,
    is_2D=True,
    unit="SI",
    save_path=None,
    file_name=None,
    file_format="csv",
    is_multiple_files=False,
    plot_options={}
):
    """Exports the sliced or interpolated version of the data, using conversions and symmetries if needed, in a file.
    Parameters
    ----------
    self: Data
        a Data object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    axis_data: list
        list of ndarray corresponding to user-input data
    file_format: str
        export format ("csv", ...)
    Returns
    -------
    a DataND object
    """

    # If args not specified, write only oneperiod/pattern
    if args == tuple():
        # Dynamic import to avoid loop
        module = __import__("SciDataTool.Classes.DataPattern", fromlist=["DataPattern"])
        DataPattern = getattr(module, "DataPattern")
        arg_list = []
        for axis in self.get_axes():
            if isinstance(axis, DataPattern):
                arg_list.append(axis.name + "[pattern]")
            else:
                arg_list.append(axis.name + "[oneperiod]")
        args = tuple(arg_list)

    # Get requested data
    if is_2D:
        Xdata, Ydatas, title, xlabel, ylabel, legends = self.plot_2D_Data(
            *args, **plot_options, unit=unit, is_export=True
        )
        axes_list_new = []
        if "for " in title:
            slices = title.split("for ")[1]
        else:
            slices = ""
    else:
        if "is_norm" in plot_options:
            is_norm = plot_options["is_norm"]
        else:
            is_norm = False
        if "axis_data" in plot_options:
            axis_data = plot_options["axis_data"]
        else:
            axis_data = None
        is_fft = False
        for arg in args:
            if "freqs" in arg or "wavenumber" in arg:
                is_fft = True
        if is_fft:
            results = self.get_magnitude_along(
                *args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
        else:
            results = self.get_along(
                *args, unit=unit, is_norm=is_norm, axis_data=axis_data
            )
        axes_list = results["axes_list"]

        # Remove slice axes
        axes_list_new = []
        slices = ""
        for axis in axes_list:
            if axis.unit == "SI":
                axis.unit = unit_dict[axis.name]
            if len(results[axis.name]) == 1:
                slices += axis.name + "=" + str(results[axis.name][0])
            elif isinstance(results[axis.name], str):
                slices += axis.name + "=" + results[axis.name]
            else:
                axes_list_new.append(axis)
        for axis in results["axes_dict_other"]:
            if slices != "":
                slices = slices + ", "
            slices += axis + "=" + str(results["axes_dict_other"][axis][0])
        if slices != "":
            slices = "sliced at " + slices

    # Default file_name
    if file_name is None:
        file_name = self.symbol + "_Data"

    if file_format == "csv":
        # Write csv files
        # Format: first axis in column, second in row, third in file
        if is_2D or len(axes_list_new) < 3:
            nfiles = 1
        elif len(axes_list_new) == 3 and is_multiple_files:
            nfiles = len(axes_list_new[2].values)
        elif len(axes_list_new) == 3:
            raise Exception(
                "cannot export more than 2 dimensions in single csv file. Activate is_multiple_files to write in multiple csv files."
            )
        else:
            raise Exception("cannot export more than 3 dimensions in csv file")

        for i in range(nfiles):
            if nfiles > 1:
                file_name_i = (
                    file_name
                    + "_"
                    + axes_list_new[2].name
                    + str(axes_list_new[2].values[i])
                )
                if slices == "":
                    slices = "sliced at "
                slices_i = (
                    slices
                    + axes_list_new[2].name
                    + "="
                    + str(axes_list_new[2].values[i])
                )
            else:
                file_name_i = file_name
                slices_i = slices
            with open(
                join(save_path, file_name_i + "." + file_format), "w+", newline=""
            ) as my_csv:
                csvWriter = csv.writer(my_csv, delimiter=",")
                # First line: meta-data
                if unit == "SI":
                    unit = self.unit
                if "dB" in unit:
                    unit += (
                        " re. " + str(self.normalizations["ref"].ref) + " " + self.unit
                    )

                meta_data = [self.symbol, self.name, "[" + unit + "]", slices_i]
                csvWriter.writerow(meta_data)

                if is_2D:
                    # Second line: axes + second axis values
                    if len(Ydatas) > 1:
                        A2_cell = xlabel + "/" + legends[-1].split("=")[0]
                        second_line = format_matrix(
                            np.insert(
                                np.array(legends).astype("<U64"),
                                0,
                                A2_cell,
                            ),
                            CHAR_LIST,
                        )
                    else:
                        A2_cell = xlabel
                        second_line = [A2_cell]
                    csvWriter.writerow(second_line)

                    # Rest of file: first axis + matrix
                    if len(Ydatas) == 1:
                        field = np.array(Ydatas[0])
                    else:
                        field = np.array(Ydatas)
                    if field.shape[0] != len(Xdata[0]):
                        field = field.T
                    matrix = format_matrix(
                        np.column_stack((np.array(Xdata[0]).T, field)).astype("str"),
                        CHAR_LIST,
                    )
                    csvWriter.writerows(matrix)

                else:
                    # Second line: axes + second axis values
                    if len(axes_list_new) == 1:
                        A2_cell = (
                            axes_list_new[0].name + "[" + axes_list_new[0].unit + "]"
                        )
                        second_line = [A2_cell]
                    else:
                        A2_cell = (
                            axes_list_new[0].name
                            + "["
                            + axes_list_new[0].unit
                            + "]"
                            + "/"
                            + axes_list_new[1].name
                            + "["
                            + axes_list_new[1].unit
                            + "]"
                        )
                        second_line = format_matrix(
                            np.insert(
                                results[axes_list_new[1].name].astype("<U64"),
                                0,
                                A2_cell,
                            ),
                            CHAR_LIST,
                        )
                    csvWriter.writerow(second_line)

                    # Rest of file: first axis + matrix
                    if len(results[self.symbol].shape) == 1:
                        # Transpose if 1D array
                        field = results[self.symbol].T
                    elif nfiles > 1:
                        # Slice third axis
                        field = np.take(results[self.symbol], i, axis=2)
                    else:
                        field = results[self.symbol]
                    matrix = format_matrix(
                        np.column_stack(
                            (results[axes_list_new[0].name].T, field)
                        ).astype("str"),
                        CHAR_LIST,
                    )
                    csvWriter.writerows(matrix)

    else:
        raise Exception("export format not supported")


def format_matrix(a, char_list):
    for char in char_list:
        a = np.char.replace(a, char, "")
    return a
