from SciDataTool.Functions.Plot.plot_2D import plot_2D
from SciDataTool.Functions.Plot import (
    unit_dict,
    norm_dict,
    axes_dict,
    fft_dict,
    COLORS,
)
from SciDataTool.Functions.Load.import_class import import_class
from SciDataTool.Functions.fix_axes_order import fix_axes_order
from SciDataTool.Functions.parser import read_input_strings
from SciDataTool.Classes.Norm_indices import Norm_indices
from numpy import (
    squeeze,
    split,
    array,
    where,
    unique,
    nanmax as np_max,
    array2string,
    insert,
    nanmin as np_min,
    linspace,
    argmin,
    argmax,
    take,
    log10,
    nan,
)


def plot_2D_Data(
    self,
    *arg_list,
    axis_data=None,
    is_norm=False,
    unit="SI",
    overall_axes=[],
    data_list=[],
    legend_list=[],
    color_list=None,
    linestyles=None,
    linewidth_list=[2],
    save_path=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_disp_title=True,
    is_grid=True,
    is_auto_ticks=True,
    is_auto_range=True,
    xlabel=None,
    ylabel=None,
    title=None,
    fig=None,
    ax=None,
    barwidth=100,
    type_plot=None,
    fund_harm_dict=None,
    is_show_fig=None,
    win_title=None,
    thresh=None,
    font_name="arial",
    font_size_title=12,
    font_size_label=10,
    font_size_legend=8,
    is_show_legend=True,
    is_outside_legend=False,
    is_frame_legend=True,
    is_indlabels=False,
    annotations=None,
):
    """Plots a field as a function of time

    Parameters
    ----------
    data : Data
        a Data object
    *arg_list : list of str
        arguments to specify which axes to plot
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
    data_list : list
        list of Data objects to compare
    legend_list : list
        list of legends to use for each Data object (including reference one) instead of data.name
    color_list : list
        list of colors to use for each Data object
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    x_min : float
        minimum value for the x-axis
    x_max : float
        maximum value for the x-axis
    y_min : float
        minimum value for the y-axis
    y_max : float
        maximum value for the y-axis
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_disp_title : bool
        boolean indicating if the title must be displayed
    is_grid : bool
        boolean indicating if the grid must be displayed
    is_auto_ticks : bool
        in fft, adjust ticks to freqs (deactivate if too close)
    is_auto_range : bool
        in fft, display up to 1% of max
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    barwidth : float
        barwidth scaling factor, only if type_plot = "bargraph"
    type_plot : str
        type of 2D graph : "curve", "bargraph", "barchart" or "quiver"
    fund_harm_dict : dict
        Dict containing axis name as key and frequency/order/wavenumber of fundamental harmonic as value to display fundamental harmonic in red in the fft
    is_show_fig : bool
        True to show figure after plot
    win_title : str
        Title of the plot window
    thresh : float
        threshold for automatic fft ticks
    is_outside_legend : bool
        True to display legend outside the graph
    is_frame_legend : bool
        True to display legend in a frame
    """

    # Dynamic import to avoid import loop
    DataPattern = import_class("SciDataTool.Classes", "DataPattern")

    # Extract arg_list it the function called from another script with *arg_list
    if len(arg_list) == 1 and type(arg_list[0]) == tuple:
        arg_list = arg_list[0]

    axes_names = [
        axis.name for axis in read_input_strings(arg_list, axis_data=axis_data)
    ]

    # Fix axes order
    arg_list_along = fix_axes_order([axis.name for axis in self.get_axes()], arg_list)

    # In case of 1D fft, keep only positive wavenumbers
    for i, arg in enumerate(arg_list_along):
        if "wavenumber" in arg and "=" not in arg and "[" not in arg:
            liste = list(arg_list_along)
            liste[i] = arg.replace("wavenumber", "wavenumber>0")
            arg_list_along = tuple(liste)

    if color_list == [] or color_list is None:
        color_list = COLORS

    new_color_list = color_list.copy()

    # Set unit
    if unit == "SI":
        unit = self.unit

    # Detect if is fft, build ylabel
    if "dB" in unit and "ref" in self.normalizations:
        unit_str = (
            "["
            + unit
            + " re. "
            + str(self.normalizations["ref"].ref)
            + " $"
            + self.unit
            + "$]"
        )
    else:
        unit_str = r"$[" + unit + "]$"
    is_fft = False
    if (
        any("wavenumber" in s for s in arg_list) or any("freqs" in s for s in arg_list)
    ) and type_plot != "curve":
        is_fft = True
        if self.symbol == "Magnitude":
            if ylabel is None:
                ylabel = "Magnitude " + unit_str
        else:
            if ylabel is None:
                ylabel = r"$|\widehat{" + self.symbol + "}|$ " + unit_str
    else:
        if is_norm:
            if ylabel is None:
                ylabel = (
                    r"$\frac{" + self.symbol + "}{" + self.symbol + "_0}\,$" + unit_str
                )
        else:
            if self.symbol == "Magnitude":
                if ylabel is None:
                    ylabel = "Magnitude " + unit_str
            else:
                if ylabel is None:
                    ylabel = r"$" + self.symbol + "\,$" + unit_str

    # Extract field and axes
    Xdatas = []
    Ydatas = []
    data_list2 = [self] + data_list
    for i, d in enumerate(data_list2):
        if is_fft or "dB" in unit:
            result = d.get_magnitude_along(
                *arg_list_along, axis_data=axis_data, unit=unit, is_norm=is_norm
            )
            if i == 0:
                axes_list = result.pop("axes_list")
                axes_dict_other = result.pop("axes_dict_other")
                result_0 = result
        else:
            result = d.get_along(
                *arg_list_along, axis_data=axis_data, unit=unit, is_norm=is_norm
            )
            if i == 0:
                axes_list = result.pop("axes_list")
                axes_dict_other = result.pop("axes_dict_other")
                result_0 = result
        Ydatas.append(result.pop(d.symbol))
        # in string case not overlay, Xdatas is a linspace
        if (
            axes_list[list(result.keys()).index(axes_names[0])].is_components
            and axes_list[list(result.keys()).index(axes_names[0])].extension != "list"
        ):
            xdata = linspace(
                0, len(result[axes_names[0]]) - 1, len(result[axes_names[0]])
            )
        else:
            xdata = result[axes_names[0]]
        Xdatas.append(xdata)

    # Build xlabel and title
    title1 = self.name[0].capitalize() + self.name[1:] + " "
    title2 = "for "
    for axis in axes_list:
        if axis.unit in norm_dict and axis.unit != "Hz":
            name = norm_dict[axis.unit].split(" [")[0]
        elif axis.name in axes_dict:
            name = axes_dict[axis.name]
        else:
            name = axis.name
        if (
            axis.extension
            in [
                "whole",
                "interval",
                "oneperiod",
                "antiperiod",
                "smallestperiod",
                "axis_data",
                "list",
            ]
            and len(axis.values) > 1
            or (len(axis.values) == 1 and len(axes_list) == 1)
        ):
            if axis.unit == "SI":
                if axis.name in unit_dict:
                    axis_unit = unit_dict[axis.name]
                else:
                    axis_unit = axis.unit
                if xlabel is None:
                    xlabel = name[0].capitalize() + name[1:] + " [" + axis_unit + "]"
                main_axis_name = name
            elif axis.unit in norm_dict:
                if xlabel is None:
                    xlabel = norm_dict[axis.unit]
                if axis.unit == "Hz":
                    main_axis_name = "frequency"
                else:
                    main_axis_name = axis.unit
            else:
                axis_unit = axis.unit
                if xlabel is None:
                    xlabel = name[0].capitalize() + name[1:] + " [" + axis_unit + "]"
                main_axis_name = name
            if (
                axis.name == "angle"
                and axis.unit == "°"
                and round(np_max(axis.values) / 6) % 5 == 0
            ):
                xticks = [i * round(np_max(axis.values) / 6) for i in range(7)]
            else:
                xticks = None
            if (
                axes_list[list(result.keys()).index(axes_names[0])].is_components
                and not self.get_axes()[0].is_overlay
            ):
                xticklabels = result[axes_names[0]]
                xticks = Xdatas[0]
            else:
                xticklabels = None
                xticks = None
        else:
            if axis.corr_unit == "SI":
                if axis.name in unit_dict:
                    axis_unit = unit_dict[axis.name]
                else:
                    axis_unit = axis.unit
            elif axis.corr_unit in norm_dict and axis.corr_unit != "Hz":
                axis_unit = norm_dict[axis.corr_unit]
            else:
                axis_unit = axis.unit

            if isinstance(result_0[axis.name], str):
                title2 += name + "=" + result_0[axis.name]
            else:
                if isinstance(result_0[axis.name][0], str):
                    axis_str = result_0[axis.name][0]
                else:
                    if result_0[axis.name][0] > 10:
                        fmt = "{:.5g}"
                    else:
                        fmt = "{:.3g}"
                    axis_str = array2string(
                        result_0[axis.name], formatter={"float_kind": fmt.format}
                    ).replace(" ", ", ")

                if len(result_0[axis.name]) == 1:
                    axis_str = axis_str.strip("[]")

                index = None
                if axis.is_pattern and len(axis.values) == 1:
                    for axis_obj in self.get_axes():
                        if axis_obj.name == axis.name:
                            index = axis.indices[0]

                title2 += name + "=" + axis_str.rstrip(", ") + " [" + axis_unit + "]"
                if index is not None:
                    title2 += " (slice " + str(index + 1) + "), "
                else:
                    title2 += ", "

    # Title part 3 containing axes that are here but not involved in requested axes
    title3 = ""
    for axis_name in axes_dict_other:
        is_display = True
        for axis in self.axes:
            if axis.name == axis_name:
                if isinstance(axis, DataPattern) and len(axis.unique_indices) == 1:
                    is_display = False
        if is_display:
            if isinstance(axes_dict_other[axis_name][0], str):
                title3 += axis_name + "=" + axes_dict_other[axis_name][0]
            else:
                if axes_dict_other[axis_name][0] > 10:
                    fmt = "{:.5g}"
                else:
                    fmt = "{:.3g}"
                title3 += (
                    axis_name
                    + "="
                    + array2string(
                        axes_dict_other[axis_name][0],
                        formatter={"float_kind": fmt.format},
                    ).replace(" ", ", ")
                    + " ["
                    + axes_dict_other[axis_name][1]
                    + "], "
                )

    if title2 == "for " and title3 == "":
        title2 = ""

    # Detect discontinuous axis (Norm_indices) to use bargraph
    for axis in axes_list:
        if axis.unit in self.axes[axis.index].normalizations:
            if isinstance(
                self.axes[axis.index].normalizations[axis.unit], Norm_indices
            ):
                type_plot = "bargraph"

    # Detect how many curves are overlaid, build legend and color lists
    if legend_list == [] and data_list != []:
        legend_list = [d.name for d in data_list2]
    elif legend_list == []:
        legend_list = ["" for d in data_list2]
    legends = []
    # Prepare colors
    linestyle_list = linestyles
    for i, d in enumerate(data_list2):
        is_overlay = False
        for axis in axes_list:
            if axis.extension == "list":
                is_overlay = True
                if linestyles is None:
                    linestyles = ["dashed"]
                n_curves = len(axis.values)
                if axis.unit == "SI":
                    if axis.name in unit_dict:
                        axis_unit = unit_dict[axis.name]
                    else:
                        axis_unit = axis.unit
                elif axis.unit in norm_dict:
                    axis_unit = norm_dict[axis.unit]
                else:
                    axis_unit = axis.unit
                if len(d.axes[axis.index].get_values()) > 1:
                    legends += [
                        (
                            legend_list[i]
                            + " "
                            + axis.name
                            + "="
                            + axis.values.tolist()[j]
                            + " "
                            + axis_unit
                            if isinstance(axis.values.tolist()[j], str)
                            else legend_list[i]
                            + " "
                            + axis.name
                            + "="
                            + "%.3g" % axis.values.tolist()[j]
                            + " "
                            + axis_unit
                        )
                        .replace("SI", "")
                        .replace(" []", "")
                        for j in range(n_curves)
                    ]
                else:
                    legends += [legend_list[i]]

        if not is_overlay:
            legends += [legend_list[i]]
            # Adjust colors in non overlay case with overlay axis
            if len(data_list2) > 1:
                for axis in self.get_axes():
                    if axis.is_overlay and len(color_list) > len(axis.values):
                        new_color_list[1:] = color_list[len(axis.values) :]

    # Split Ydatas if the plot overlays several curves
    if is_overlay:
        Ydata = []
        for d in Ydatas:
            if d.ndim != 1:
                axis_index = where(array(d.shape) == n_curves)[0]
                if axis_index.size > 1:
                    print("WARNING, several axes with same dimensions")
                Ydata += split(d, n_curves, axis=axis_index[-1])
            else:
                Ydata += [d]
        Ydatas = [squeeze(d) for d in Ydata]
        Xdata = []
        for i in range(len(data_list2)):
            Xdata += [Xdatas[i] for x in range(n_curves)]
        Xdatas = Xdata

    # Finish title
    if title is None:

        # Reformat in case of operation
        for ope in ["max", "min", "mean"]:
            if "=" + ope in title2:
                title2 = ""
                title1 = (
                    ope[0].capitalize() + ope[1:] + " " + title1[0].lower() + title1[1:]
                )

        # Concatenate all title parts
        if is_overlay:
            title = title1 + title3
        else:
            title = title1 + title2 + title3

        # Remove last coma due to title2 or title3
        title = title.rstrip(", ")

        # Remove dimless and quotes
        title = title.replace("SI", "").replace("[]", "").replace("'", "")

    xlabel = xlabel.replace("SI", "").replace(" []", "")  # Remove dimless units
    ylabel = ylabel.replace("SI", "").replace(" []", "")  # Remove dimless units

    # Overall computation
    if overall_axes != []:
        if self.unit == "W":
            op = "=sum"
        else:
            op = "=rss"
        arg_list_ovl = [0 for i in range(len(arg_list))]
        # Add sum to overall_axes
        for axis in overall_axes:
            is_match = False
            for i, arg in enumerate(arg_list):
                if axis in arg:
                    is_match = True
                    arg_list_ovl[i] = axis + op
            if not is_match:
                arg_list_ovl.append(axis + op)
        # Add other requested axes
        for i, arg in enumerate(arg_list):
            if arg_list_ovl[i] == 0:
                arg_list_ovl[i] = arg
        if is_fft or "dB" in unit:
            result = self.get_magnitude_along(
                *arg_list_ovl, unit=unit, axis_data=axis_data
            )
        else:
            result = self.get_along(*arg_list_ovl, unit=unit, axis_data=axis_data)
        Y_overall = result[self.symbol]
        # in string case not overlay, Xdatas is a linspace
        if (
            axes_list[list(result.keys()).index(axes_names[0])].is_components
            and axes_list[list(result.keys()).index(axes_names[0])].extension != "list"
        ):
            xdata = linspace(
                0, len(result[axes_names[0]]) - 1, len(result[axes_names[0]])
            )
        else:
            xdata = result[list(result)[0]]
        Ydatas.insert(0, Y_overall)
        Xdatas.insert(0, xdata)
        new_color_list = new_color_list.copy()
        new_color_list.insert(0, "#000000")
        legends.insert(0, "Overall")

    # Deactivate legend if only one item
    if type_plot == "point":
        legends = []

    if "dB" in unit:  # Replace <=0 by nans
        for ydata in Ydatas:
            ydata[ydata <= 0] = nan

    # Call generic plot function
    if is_fft:

        if thresh is None:
            if self.normalizations is not None and "ref" in self.normalizations:
                thresh = self.normalizations["ref"].ref
            else:
                thresh = 0.02

        freqs = Xdatas[0]
        if "dB" in unit:
            indices = [
                ind
                for ind, y in enumerate(Ydatas[0])
                if abs(y) > max(10 * log10(thresh) + abs(np_max(Ydatas[0])), 0)
            ]
        else:
            if Ydatas[0].size == 1:
                indices = [0]
            else:
                indices = [
                    ind
                    for ind, y in enumerate(Ydatas[0])
                    if abs(y) > abs(thresh * np_max(Ydatas[0]))
                ]
        xticks = unique(insert(freqs[indices], 0, 0))

        if is_auto_range:
            if len(xticks) > 1:
                if x_min is None:
                    x_min = xticks[0]
                else:
                    x_min = max(x_min, xticks[0])
                if x_max is None:
                    x_max = xticks[-1]
                else:
                    x_max = min(x_max, xticks[-1])
            else:
                if x_min is None:
                    x_min = np_min(freqs)
                else:
                    x_min = max(x_min, np_min(freqs))
                if x_max is None:
                    x_max = np_max(freqs)
                else:
                    x_max = min(x_max, np_max(freqs))

        else:
            if x_min is None:
                x_min = np_min(freqs)
            if x_max is None:
                x_max = np_max(freqs)

        x_min = x_min - x_max * 0.05
        x_max = x_max * 1.05

        if (
            len(xticks) == 0
            or (
                len(xticks) > 20
                and not axes_list[
                    list(result.keys()).index(axes_names[0])
                ].is_components
            )
            or not is_auto_ticks
        ):
            xticks = None

        # Force bargraph for fft if type_graph not specified
        if type_plot is None:
            type_plot = "bargraph"

        # Option to draw fundamental harmonic in red
        if not fund_harm_dict:
            fund_harm = None
        else:
            # Activate the option only if main axis is in dict and only one Data is plotted
            if main_axis_name in fund_harm_dict and len(Ydatas) == 1:
                fund_harm = fund_harm_dict[main_axis_name]
            else:
                # Deactivate the option
                fund_harm = None

        plot_2D(
            Xdatas,
            Ydatas,
            legend_list=legends,
            color_list=new_color_list,
            linestyle_list=linestyle_list,
            linewidth_list=linewidth_list,
            fig=fig,
            ax=ax,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            type_plot=type_plot,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            is_logscale_x=is_logscale_x,
            is_logscale_y=is_logscale_y,
            is_disp_title=is_disp_title,
            is_grid=is_grid,
            xticks=xticks,
            xticklabels=xticklabels,
            save_path=save_path,
            barwidth=barwidth,
            fund_harm=fund_harm,
            is_show_fig=is_show_fig,
            win_title=win_title,
            font_name=font_name,
            font_size_title=font_size_title,
            font_size_label=font_size_label,
            font_size_legend=font_size_legend,
            is_show_legend=is_show_legend,
            is_outside_legend=is_outside_legend,
            is_frame_legend=is_frame_legend,
            is_indlabels=is_indlabels,
        )

    else:

        # Force curve plot if type_plot not specified
        if type_plot is None:
            type_plot = "curve"
        annot = None
        # Hidden annotations
        if annotations is not None:
            try:
                annot = list()
                axis_along = self.get_axes(annotations[0])[0]
                axis_op = self.get_axes(annotations[1])[0]
                operation = annotations[2]
                arg_list_new = []
                if self.unit == "W":
                    op = "=sum"
                else:
                    op = "=rss"
                for axis in self.get_axes():
                    if axis.name not in [axis_along.name, axis_op.name]:
                        arg_list_new.append(axis.name + op)
                    else:
                        arg_list_new.append(axis.name)
                data2 = self.get_data_along(*arg_list_new, unit=unit)
                arg_list_new = []
                for arg in arg_list_along:
                    if axis_along.name in arg or axis_op.name in arg:
                        arg_list_new.append(arg.replace("=sum", ""))
                result = data2.get_magnitude_along(*arg_list_new)
                for ii in range(len(result[annotations[0]])):
                    if operation == "max":
                        index = argmax(take(result[self.symbol], ii, axis=0))
                        annot.append(
                            "main "
                            + annotations[1].rstrip("s")
                            + ": "
                            + axis_op.get_values()[index]
                        )
                if len(overall_axes) != 0:
                    annot.insert(0, "Overall")
            except Exception:
                pass

        plot_2D(
            Xdatas,
            Ydatas,
            legend_list=legends,
            color_list=new_color_list,
            fig=fig,
            ax=ax,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            type_plot=type_plot,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            is_logscale_x=is_logscale_x,
            is_logscale_y=is_logscale_y,
            is_disp_title=is_disp_title,
            is_grid=is_grid,
            xticks=xticks,
            xticklabels=xticklabels,
            barwidth=barwidth,
            linestyle_list=linestyle_list,
            linewidth_list=linewidth_list,
            save_path=save_path,
            is_show_fig=is_show_fig,
            win_title=win_title,
            font_name=font_name,
            font_size_title=font_size_title,
            font_size_label=font_size_label,
            font_size_legend=font_size_legend,
            is_show_legend=is_show_legend,
            is_outside_legend=is_outside_legend,
            is_frame_legend=is_frame_legend,
            is_indlabels=is_indlabels,
            annotations=annot,
        )
