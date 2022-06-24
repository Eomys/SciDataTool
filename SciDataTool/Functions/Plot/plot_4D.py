# -*- coding: utf-8 -*-

from numpy import log10, abs as np_abs, nanmax as np_max, NaN, zeros_like
import matplotlib.pyplot as plt

from SciDataTool.Functions.Plot.init_fig import init_fig
import numpy as np


def plot_4D(
    Xdata,
    Ydata,
    Zdata,
    Sdata=None,
    is_same_size=False,
    colormap="jet",
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    title="",
    xlabel="",
    ylabel="",
    zlabel="",
    xticks=None,
    yticks=None,
    xticklabels=None,
    yticklabels=None,
    annotations=None,
    annotation_threshold=0.01,
    fig=None,
    ax=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_logscale_z=False,
    is_disp_title=True,
    type_plot="scatter",
    save_path=None,
    is_show_fig=None,
    is_switch_axes=False,
    win_title=None,
    font_name="arial",
    font_size_title=12,
    font_size_label=10,
    font_size_legend=8,
    is_grid=False,
    grid_xlw=None,
    grid_ylw=None,
    marker_color="k",
    is_hide_annotation=False,
):
    """Plots a 4D graph

    Parameters
    ----------
    Xdata : ndarray
        array of x-axis values
    Ydata : ndarray
        array of y-axis values
    Zdata : ndarray
        array of z-axis values
    Sdata : ndarray
        array of 4th axis values
    is_same_size : bool
        in scatter plot, all squares are the same size
    colormap : colormap object
        colormap prescribed by user
    x_min : float
        minimum value for the x-axis (no automated scaling in 3D)
    x_max : float
        maximum value for the x-axis (no automated scaling in 3D)
    y_min : float
        minimum value for the y-axis (no automated scaling in 3D)
    y_max : float
        maximum value for the y-axis (no automated scaling in 3D)
    z_min : float
        minimum value for the z-axis (no automated scaling in 3D)
    z_max : float
        maximum value for the z-axis (no automated scaling in 3D)
    title : str
        title of the graph
    xlabel : str
        label for the x-axis
    ylabel : str
        label for the y-axis
    zlabel : str
        label for the z-axis
    xticks : list
        list of ticks to use for the x-axis
    yticks: list
        list of ticks to use for the y-axis
    xticklabels : list
        list of tick labels to use for the x-axis
    yticklabels : list
        list of tick labels to use for the x-axis
    annotations : list
        list of annotations to apply to data
    annotation_threshold : float
        threshold to plot annotation (percentage of the maximum value)
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_logscale_z : bool
        boolean indicating if the z-axis must be set in logarithmic scale
    is_disp_title : bool
        boolean indicating if the title must be displayed
    type : str
        type of 3D graph : "stem", "surf", "pcolor" or "scatter"
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    is_show_fig : bool
        True to show figure after plot
    is_switch_axes : bool
        to switch x and y axes
    is_grid : bool
        to plot grid
    grid_xlw : float
        grid linewidth along x
    grid_ylw : float
        grid linewidth along y
    """

    # Set figure/subplot
    if is_show_fig is None:
        is_show_fig = True if fig is None else False

    # Set if figure is 3D
    if "scatter" not in type_plot:
        is_3d = True
    else:
        is_3d = False

    # Set figure if needed
    if fig is None and ax is None:
        (fig, ax, _, _) = init_fig(fig=None, shape="rectangle", is_3d=is_3d)

    # Check logscale on z axis
    if is_logscale_z:
        Zdata = 10 * log10(np_abs(Zdata))
        clb_format = "%0.0f"
    else:
        clb_format = "%.4g"

    # Calculate z limits
    if z_max is None:
        z_max = np_max(Zdata)
    if z_min is None:
        if is_logscale_z:
            z_min = 0
        else:
            z_min = z_max / 1e4

    Zdata[Zdata < z_min] = NaN

    if is_same_size:
        Sdata = zeros_like(Zdata)
        Sdata[Zdata > z_max / 1e4] = 30
    elif Sdata is None:
        Sdata = 300 * Zdata / z_max

    # Switch axes
    if is_switch_axes:
        Xdata, Ydata = Ydata, Xdata
        if len(Xdata.shape) > 1:
            Xdata = Xdata.T
        if len(Ydata.shape) > 1:
            Ydata = Ydata.T
        if len(Zdata.shape) > 1:
            Zdata = Zdata.T
        x_min, y_min = y_min, x_min
        x_max, y_max = y_max, x_max
        xlabel, ylabel = ylabel, xlabel
        xticks, yticks = yticks, xticks
        xticklabels, yticklabels = yticklabels, xticklabels
        is_logscale_x, is_logscale_y = is_logscale_y, is_logscale_x

    # Plot
    if type_plot == "scatter":
        c = ax.scatter(
            Xdata,
            Ydata,
            c=Zdata,
            s=Sdata,
            marker="s",
            cmap=colormap,
            vmin=z_min,
            vmax=z_max,
            picker=True,
            pickradius=5,
        )
        clb = fig.colorbar(c, ax=ax, format=clb_format)
        clb.ax.set_title(zlabel, fontsize=font_size_legend, fontname=font_name)
        clb.ax.tick_params(labelsize=font_size_legend)
        for l in clb.ax.yaxis.get_ticklabels():
            l.set_family(font_name)
        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
            plt.xticks(rotation=90, ha="center", va="top")
        if xticklabels is not None:
            ax.set_xticklabels(xticklabels, rotation=90)
        if yticks is not None:
            ax.yaxis.set_ticks(yticks)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels)
        if annotations is not None:
            for i, txt in enumerate(annotations):
                if Zdata[i] > annotation_threshold and txt is not None:
                    ax.annotate(
                        txt,
                        (Xdata[i], Ydata[i]),
                        rotation=45,
                        family=font_name,
                        visible=not is_hide_annotation,
                    )

    elif type_plot == "scatterX":
        c = ax.scatter(
            Xdata,
            Ydata,
            s=50 * Zdata,
            color=marker_color,
            marker="x",
            picker=True,
            pickradius=5,
        )
        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
            plt.xticks(rotation=90, ha="center", va="top")
        if xticklabels is not None:
            ax.set_xticklabels(xticklabels, rotation=90)
        if yticks is not None:
            ax.yaxis.set_ticks(yticks)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    if is_logscale_x:
        ax.xscale("log")

    if is_logscale_y:
        ax.yscale("log")

    if is_disp_title:
        ax.set_title(title)

    if is_3d:
        for item in (
            [ax.xaxis.label, ax.yaxis.label, ax.zaxis.label]
            + ax.get_xticklabels()
            + ax.get_yticklabels()
            + ax.get_zticklabels()
        ):
            item.set_fontsize(font_size_label)
    else:
        for item in (
            [ax.xaxis.label, ax.yaxis.label]
            + ax.get_xticklabels()
            + ax.get_yticklabels()
        ):
            item.set_fontsize(font_size_label)
            item.set_fontname(font_name)
    ax.title.set_fontsize(font_size_title)
    ax.title.set_fontname(font_name)

    if is_grid:
        if grid_xlw is not None:
            ax.xaxis.grid(lw=grid_xlw)
        else:
            ax.xaxis.grid()
        if grid_ylw is not None:
            ax.yaxis.grid(lw=grid_ylw)
        else:
            ax.yaxis.grid()
        # ax.xaxis.grid(False) #To remove grid along x
        # Plot grid below data
        ax.set_axisbelow(True)

    if save_path is not None:
        save_path = save_path.replace("\\", "/")
        fig.savefig(save_path)
        plt.close()

    if is_show_fig:
        fig.show()

    if win_title:
        manager = plt.get_current_fig_manager()
        if manager is not None:
            manager.set_window_title(win_title)
