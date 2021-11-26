from SciDataTool.Functions.interpolations import (
    get_interpolation,
    get_interpolation_step,
)


def _interpolate(self, values, axes_list):
    """Returns the values of the field interpolated over the axes values.
    Parameters
    ----------
    self: Data
        a Data object
    values: ndarray
        array of the field
    axes_list: list
        a list of RequestedAxis objects
    Returns
    -------
    values: ndarray
        values of the field
    """

    # Interpolate over axis values
    for axis_requested in axes_list:
        if axis_requested.input_data is not None:
            if axis_requested.is_step:
                # values = apply_along_axis(
                #     get_interpolation_step,
                #     axis_requested.index,
                #     values,
                #     axis_requested.values,
                #     axis_requested.input_data,
                # )
                values = get_interpolation_step(
                    values,
                    axis_requested.values,
                    axis_requested.input_data,
                    axis_requested.index,
                )
            else:
                values = get_interpolation(
                    values,
                    axis_requested.values,
                    axis_requested.input_data,
                    axis_requested.index,
                )
            # Store new axis data into axis_requested.values
            axis_requested.values = axis_requested.input_data
    return values
