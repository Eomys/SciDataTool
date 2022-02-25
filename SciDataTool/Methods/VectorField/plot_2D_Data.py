from numpy import column_stack, array, exp, real, squeeze, array2string
from SciDataTool.Functions.Plot.plot_2D import plot_2D
from SciDataTool.Functions.conversions import (
    rphiz_to_xyz,
    xyz_to_rphiz,
    rphiz_to_xyz_field,
)
from SciDataTool.GUI.WVectorSelector.WVectorSelector import REV_COMP_DICT
from SciDataTool.Functions.Load.import_class import import_class


def plot_2D_Data(
    self,
    *arg_list,
    axis_data=None,
    radius=None,
    is_norm=False,
    unit="SI",
    component_list=None,
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
    is_auto_range=False,
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
    scale_units="x",
    scale=None,
    width=0.005,
    phase=0,
    is_show_legend=True,
    is_outside_legend=False,
    is_frame_legend=True,
):
    """Plots a field as a function of time

    Parameters
    ----------
    self : Output
        an Output object
    Data_str : str
        name of the Data Object to plot (e.g. "mag.Br")
    *arg_list : list of str
        arguments to specify which axes to plot
    radius : float
        radius used for quiver plot
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
    data_list : list
        list of Data objects to compare
    component_list : list
        list of component names to plot in separate figures
    legend_list : list
        list of legends to use for each Data object (including reference one) instead of data.name
    color_list : list
        list of colors to use for each Data object
    save_path : str
        full path of the png file where the figure is saved if save_path is not None
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
    thresh : float
        threshold for automatic fft ticks
    scale_units : str
        arrow lenght scale factor reference {'width', 'height', 'dots', 'pouces', 'x', 'y', 'xy'}
    scale : float
        arrow length factor
    width : float
        arrow width factor
    is_outside_legend : bool
        True to display legend outside the graph
    is_frame_legend : bool
        True to display legend in a frame
    """

    # Dynamic import to avoid import loop
    DataPattern = import_class("SciDataTool.Classes", "DataPattern")

    # Special case of quiver plot
    if type_plot == "quiver":

        if component_list is None:
            title = "Total " + self.name
            result = self.get_xyz_along(
                arg_list,
                axis_data=axis_data,
                unit=unit,
                is_norm=is_norm,
            )

            if "x" in result and "y" in result:
                Xdatas = column_stack((result["x"], result["y"]))
            else:
                if radius is None:
                    radius = 1
                phi = result["angle"]
                rphi = column_stack((array([radius] * len(phi)), phi))
                Xdatas = rphiz_to_xyz(rphi)

            Ydatas = column_stack(
                (squeeze(result["comp_x"]), squeeze(result["comp_y"]))
            )
        else:
            title = REV_COMP_DICT[component_list[0]] + " " + self.name
            if component_list[0] in ["comp_x", "comp_y"]:
                vecfield = self.to_xyz()
                result = vecfield.components[component_list[0]].get_along(
                    arg_list,
                    axis_data=axis_data,
                    unit=unit,
                    is_norm=is_norm,
                )
                if "x" in result and "y" in result:
                    Xdatas = column_stack((result["x"], result["y"]))
                else:
                    if radius is None:
                        radius = 1
                    phi = result["angle"]
                    rphi = column_stack((array([radius] * len(phi)), phi))
                    Xdatas = rphiz_to_xyz(rphi)
                Y_comp = result[vecfield.components[component_list[0]].symbol]
                if component_list[0] == "comp_x":
                    Y_comp[Xdatas[:, 0] < 0] = -Y_comp[Xdatas[:, 0] < 0]
                    Ydatas = column_stack((Y_comp, 0 * Y_comp, 0 * Y_comp))
                else:
                    Y_comp[Xdatas[:, 1] < 0] = -Y_comp[Xdatas[:, 1] < 0]
                    Ydatas = column_stack((0 * Y_comp, Y_comp, 0 * Y_comp))
            else:
                vecfield = self.to_rphiz()
                result = vecfield.components[component_list[0]].get_along(
                    arg_list,
                    axis_data=axis_data,
                    unit=unit,
                    is_norm=is_norm,
                )
                Y_comp = result[vecfield.components[component_list[0]].symbol]

                if "x" in result and "y" in result:
                    Xdatas = column_stack((result["x"], result["y"]))
                    rphiz = xyz_to_rphiz(Xdatas)

                    if component_list[0] == "radial":
                        Y_3d = column_stack((Y_comp, 0 * Y_comp, 0 * Y_comp))
                    else:
                        Y_3d = column_stack((0 * Y_comp, Y_comp, 0 * Y_comp))

                    Ydatas = rphiz_to_xyz_field(Y_3d, rphiz[:, 1])

                else:
                    if radius is None:
                        radius = 1
                    phi = result["angle"]
                    rphi = column_stack((array([radius] * len(phi)), phi))
                    Xdatas = rphiz_to_xyz(rphi)
                    if component_list[0] == "radial":
                        Y_3d = column_stack((Y_comp, 0 * Y_comp, 0 * Y_comp))
                    else:
                        Y_3d = column_stack((0 * Y_comp, Y_comp, 0 * Y_comp))

                    Ydatas = rphiz_to_xyz_field(Y_3d, phi)

        Ydatas = real(Ydatas * exp(1j * phase))

        title2 = " for "
        if "time" in result:
            title2 += (
                "time="
                + array2string(
                    result["time"], formatter={"float_kind": "{:.3g}".format}
                )
                .replace(" ", ", ")
                .replace("[", "")
                .replace("]", "")
                + "[s]"
            )
        elif "freqs" in result:
            title2 += (
                "freqs="
                + array2string(
                    result["freqs"], formatter={"float_kind": "{:.5g}".format}
                )
                .replace(" ", ", ")
                .replace("[", "")
                .replace("]", "")
                + "[Hz]"
            )

        title3 = ""
        axes_dict_other = result["axes_dict_other"]
        for axis_name in axes_dict_other:
            is_display = True
            for axis in self.get_axes():
                if axis.name == axis_name:
                    if isinstance(axis, DataPattern) and len(axis.unique_indices) == 1:
                        is_display = False
            if is_display:
                if isinstance(axes_dict_other[axis_name][0], str):
                    title3 += axis_name + "=" + axes_dict_other[axis_name][0]
                else:
                    title3 += (
                        axis_name
                        + "="
                        + array2string(
                            axes_dict_other[axis_name][0],
                            formatter={"float_kind": "{:.3g}".format},
                        )
                        .replace(" ", ", ")
                        .replace("[", "")
                        .replace("]", "")
                        + " ["
                        + axes_dict_other[axis_name][1]
                        + "], "
                    )
        if title2 == " for " and title3 == "":
            title2 = ""
        title = title + title2 + title3

        # Normalize Ydatas
        # Ydatas = Ydatas / (np_max(Ydatas) * 0.001 * radius)
        plot_2D(
            [Xdatas],
            [Ydatas],
            color_list=color_list,
            linestyle_list=linestyles,
            linewidth_list=linewidth_list,
            title=title,
            legend_list=[self.name],
            xlabel="[m]",
            ylabel="[m]",
            fig=fig,
            ax=ax,
            type_plot="quiver",
            save_path=save_path,
            is_show_fig=is_show_fig,
            win_title=win_title,
            font_name=font_name,
            font_size_title=font_size_title,
            font_size_label=font_size_label,
            font_size_legend=font_size_legend,
            is_show_legend=is_show_legend,
            is_grid=False,
            scale_units=scale_units,
            scale=scale,
            width=width,
            is_outside_legend=is_outside_legend,
            is_frame_legend=is_frame_legend,
        )

    else:

        # Call the plot on each component
        if component_list is None:  # default: extract all components
            component_list = self.components.keys()
        for i, comp in enumerate(component_list):
            # (fig, axes, patch_leg, label_leg) = init_fig(None, shape="rectangle")

            if save_path is not None and len(component_list) > 1:
                save_path_comp = (
                    save_path.split(".")[0] + "_" + comp + "." + save_path.split(".")[1]
                )
            else:
                save_path_comp = save_path

            self.components[comp].plot_2D_Data(
                arg_list,
                axis_data=axis_data,
                is_norm=is_norm,
                unit=unit,
                data_list=[dat.components[comp] for dat in data_list],
                legend_list=legend_list,
                linestyles=linestyles,
                color_list=color_list,
                save_path=save_path_comp,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                is_logscale_x=is_logscale_x,
                is_logscale_y=is_logscale_y,
                is_disp_title=is_disp_title,
                is_grid=is_grid,
                is_auto_ticks=is_auto_ticks,
                is_auto_range=is_auto_range,
                fig=fig,
                ax=ax,
                barwidth=barwidth,
                type_plot=type_plot,
                fund_harm_dict=fund_harm_dict,
                is_show_fig=is_show_fig,
                thresh=thresh,
                font_name=font_name,
                font_size_title=font_size_title,
                font_size_label=font_size_label,
                font_size_legend=font_size_legend,
                is_show_legend=is_show_legend,
                is_outside_legend=is_outside_legend,
                is_frame_legend=is_frame_legend,
            )
