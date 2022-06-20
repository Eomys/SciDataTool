from copy import copy
import numpy as np
import imageio
import matplotlib.pyplot as plt
from SciDataTool.Functions.Plot.init_fig import init_fig, copy_fig


def plot_2D_Data_Animated(
    self,
    animated_axis,
    *arg_list,
    nb_frames=50,
    fps=10,
    axis_data=None,
    radius=None,
    is_norm=False,
    unit="SI",
    component_list=None,
    data_list=[],
    legend_list=[],
    color_list=None,
    linestyles=None,
    linewidth_list=[1.5],
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
    thresh=0.02,
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
    is_plot_only=False,
):
    """Plots a field as a function of time

    Parameters
    ----------
    self : VectorField
        an VectorField object
    Data_str : str
        name of the Data Object to plot (e.g. "mag.Br")
    animated_axis : str
        The field will be animated along this axis
    *arg_list : list of str
        arguments to specify which axes to plot
    nb_frames : int
        number of frames used to build the gif
    fps: int
        frames displayed per second
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
    scale : float
        arrow length factor in quiver. Be careful, if scale = None then there will be a normalization on the arrows on each frame
    width : float
        arrow width factor in quiver
    is_plot_only : bool
        True to remove axes, title and legend
    """

    # Special case of quiver plot
    if type_plot == "quiver":
        # list of png to make the gif
        images = list()

        # definition of the step along animated axis
        result = self.get_rphiz_along(animated_axis)
        animated_axis_name = animated_axis.split("[")[0]
        animated_values = result[animated_axis_name]
        value_max = np.nanmax(animated_values)
        value_min = np.nanmin(animated_values)
        variation_step = (value_max - value_min) / nb_frames

        # Getting the name of the gif
        save_path_gif = save_path.replace(".png", ".gif")
        fig.suptitle(None)
        # Copy_fig make a deep copy so that the machine plot is conserved
        deepcopy_fig = copy_fig(fig)

        # Params settings
        save_path = None
        is_show_fig = False

        # for value in animated_values:
        while value_min < value_max - variation_step:

            # Select a frequency and make it rotate by playing on the phase
            if "freqs" in arg_list[0]:
                arg_list0 = arg_list
                step = (value_min / variation_step) / nb_frames
                phase = 2 * np.pi * step

            # or directly select an instant/element in the animated axis
            else:
                if animated_axis_name in arg_list:
                    arg_listx = list(arg_list)
                    ind_ax = arg_listx.index(animated_axis_name)
                    arg_listx.pop(ind_ax)
                    arg_list0 = (animated_axis_name + "=" + str(value_min),) + tuple(
                        arg_listx
                    )
                    phase = 0
                else:
                    arg_list0 = (animated_axis_name + "=" + str(value_min),) + arg_list
                    phase = 0

            # Call to plot_2D_Data of VectorField class, which manage the quiver case
            self.plot_2D_Data(
                *arg_list0,
                axis_data=axis_data,
                radius=radius,
                is_norm=is_norm,
                unit=unit,
                component_list=component_list,
                data_list=data_list,
                legend_list=legend_list,
                color_list=color_list,
                linestyles=linestyles,
                linewidth_list=linewidth_list,
                save_path=save_path,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                is_logscale_x=is_logscale_x,
                is_logscale_y=is_logscale_y,
                is_disp_title=False,
                is_grid=is_grid,
                is_auto_ticks=is_auto_ticks,
                is_auto_range=is_auto_range,
                fig=fig,
                ax=ax,
                barwidth=barwidth,
                type_plot=type_plot,
                fund_harm_dict=fund_harm_dict,
                is_show_fig=is_show_fig,
                win_title=win_title,
                thresh=thresh,
                font_name=font_name,
                font_size_title=font_size_title,
                font_size_label=font_size_label,
                font_size_legend=font_size_legend,
                scale=scale,
                width=width,
                phase=phase,
                scale_units=scale_units,
                is_show_legend=is_show_legend,
                is_outside_legend=is_outside_legend,
                is_frame_legend=is_frame_legend,
            )

            if is_plot_only:
                ax.set_axis_off()
                ax.set_title("")
                ax.get_legend().remove()

            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            images.append(image)

            # Fig and ax reset to default for background
            fig, ax, _, _ = init_fig()
            deepcopy_ax = deepcopy_fig.axes[0]
            for patch in deepcopy_ax.patches:
                patch_cpy = copy(patch)
                patch_cpy.axes = None
                patch_cpy.figure = None
                patch_cpy.set_transform(ax.transData)
                ax.add_patch(patch_cpy)
            ax.set_xlim(deepcopy_ax.get_xlim())
            ax.set_ylim(deepcopy_ax.get_ylim())
            ax.set_xlabel(deepcopy_ax.get_xlabel())
            ax.set_ylabel(deepcopy_ax.get_ylabel())
            ax.set_title(deepcopy_ax.get_title())
            fig.suptitle(None)
            # While condition incrementation
            value_min += variation_step

        # Creating the gif
        plt.close(fig)
        imageio.mimsave(save_path_gif, images, format="GIF-PIL", fps=fps)

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

            self.components[comp].plot_2D_Data_Animated(
                animated_axis,
                *arg_list,
                nb_frames=nb_frames,
                fps=fps,
                axis_data=axis_data,
                is_norm=is_norm,
                unit=unit,
                data_list=[dat.components[comp] for dat in data_list],
                legend_list=legend_list,
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
            )
