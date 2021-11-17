from numpy import take


def _extract_slices_fft(self, values, axes_list):
    """Returns the values of the field (with symmetries and transformations).
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

    # Extract the slices of the field
    for index, axis in enumerate(self.axes):
        is_match = False
        for axis_requested in axes_list:
            if axis.name == axis_requested.corr_name:
                is_match = True
                if (
                    axis_requested.indices is not None
                    and axis_requested.transform == "fft"
                ):
                    values = take(values, axis_requested.indices, axis=index)
        if not is_match:  # Axis was not specified -> take slice at the first value
            values = take(values, [0], axis=index)
    return values
