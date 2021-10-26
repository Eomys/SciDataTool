from numpy import (
    argsort,
    negative,
    meshgrid,
)


def get_harmonics(
    self, N_harm, *args, unit="SI", is_norm=False, axis_data=None, is_flat=False
):
    """Returns the complex Fourier Transform of the field, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    N_harm: int
        Number of largest harmonics to be extracted
    args: list
        Axes names, ranges and units
    unit: str
        Unit demanded by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    is_flat: bool
        Boolean if the output data remains flattened (for 2D cases)
    Returns
    -------
    list of 1Darray of axes values, ndarray of magnitude of FT
    """
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args
    return_dict = self.get_magnitude_along(
        args, unit=unit, is_norm=is_norm, axis_data=axis_data
    )
    values = return_dict[self.symbol]

    # 2D case
    if "freqs" in return_dict and "wavenumber" in return_dict:
        r = return_dict["wavenumber"]
        f = return_dict["freqs"]
        # Flatten the data
        values_flat = values.flatten()
        R, F = meshgrid(r, f)
        f = F.flatten()
        r = R.flatten()
        # Get the N_harm largest peaks
        indices = argsort(negative(values_flat))
        indices = indices[:N_harm]
        values = values_flat[indices]
        f = f[indices]
        r = r[indices]
        if len(values.shape) == 2 and not is_flat:
            f.reshape((N_harm, N_harm))
            r.reshape((N_harm, N_harm))
            values.reshape((N_harm, N_harm))
        return_dict["freqs"] = f
        return_dict["wavenumber"] = r
        return_dict[self.symbol] = values

    # 1D cases
    elif "freqs" in return_dict:
        f = return_dict["freqs"]
        indices = argsort(negative(values))
        indices = indices[:N_harm]
        f = f[indices]
        values = values[indices]
        return_dict["freqs"] = f
        return_dict[self.symbol] = values
    elif "wavenumber" in return_dict:
        r = return_dict["wavenumber"]
        indices = argsort(negative(values))
        indices = indices[:N_harm]
        r = r[indices]
        values = values[indices]
        return_dict["wavenumber"] = r
        return_dict[self.symbol] = values

    return return_dict
