def plot_3D_Data(
    self,
    *arg_list,
    axis_data=None,
    is_norm=False,
    unit="SI",
    component_list=None,
    save_path=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    z_range=None,
    is_auto_ticks=True,
    is_auto_range=False,
    is_2D_view=True,
    is_same_size=False,
    N_stem=100,
    fig=None,
    ax=None,
    is_show_fig=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_logscale_z=False,
    thresh=None,
    is_switch_axes=False,
    colormap="RdBu_r",
    win_title=None,
    font_name="arial",
    font_size_title=12,
    font_size_label=10,
    font_size_legend=8,
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
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
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
    z_min : float
        minimum value for the z-axis
    z_max : float
        maximum value for the z-axis
    is_auto_ticks : bool
        in fft, adjust ticks to freqs (deactivate if too close)
    is_auto_range : bool
        in fft, display up to 1% of max
    is_2D_view : bool
        True to plot Data in xy plane and put z as colormap
    is_same_size : bool
        True to have all color blocks with same size in 2D view
    N_stem : int
        number of harmonics to plot (only for stem plots)
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    is_show_fig : bool
        True to show figure after plot
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_logscale_z : bool
        boolean indicating if the z-axis must be set in logarithmic scale
    thresh : float
        threshold for automatic fft ticks
    is_switch_axes : bool
        to switch x and y axes
    """

    # Call the plot on each component
    if component_list is None:  # default: extract all components
        component_list = self.components.keys()
    for i, comp in enumerate(component_list):

        if save_path is not None and len(component_list) > 1:
            save_path_comp = (
                save_path.split(".")[0] + "_" + comp + "." + save_path.split(".")[1]
            )
        else:
            save_path_comp = save_path

        self.components[comp].plot_3D_Data(
            arg_list,
            axis_data=axis_data,
            is_norm=is_norm,
            unit=unit,
            save_path=save_path_comp,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            z_min=z_min,
            z_max=z_max,
            colormap=colormap,
            is_auto_ticks=is_auto_ticks,
            is_auto_range=is_auto_range,
            is_2D_view=is_2D_view,
            is_same_size=is_same_size,
            N_stem=N_stem,
            fig=fig,
            ax=ax,
            is_show_fig=is_show_fig,
            is_logscale_x=is_logscale_x,
            is_logscale_y=is_logscale_y,
            is_logscale_z=is_logscale_z,
            thresh=thresh,
            is_switch_axes=is_switch_axes,
            win_title=win_title,
            font_name=font_name,
            font_size_title=font_size_title,
            font_size_label=font_size_label,
            font_size_legend=font_size_legend,
        )
