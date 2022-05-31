from SciDataTool.Functions.parser import read_input_strings
from SciDataTool.Functions.fft_functions import comp_fftn, comp_ifftn
from SciDataTool.Functions.fix_axes_order import fix_axes_order


def get_along(
    self,
    *args,
    unit="SI",
    is_norm=False,
    axis_data=[],
    is_squeeze=True,
    is_magnitude=False,
    corr_unit=None,
):
    """Returns the ndarray of the field, using conversions and symmetries if needed.
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
    Returns
    -------
    list of 1Darray of axes values, ndarray of field values
    """
    # Read the axes input in args
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args

    # Fix axes order
    args = fix_axes_order([axis.name for axis in self.get_axes()], args)

    axes_list = read_input_strings(args, axis_data)
    # Extract the requested axes (symmetries + unit)
    axes_list, transforms = self._comp_axes(axes_list)
    # Get the field
    values = self._get_field(axes_list)
    # If DataFreq + 1 ifft axis + 1 fft axis: perform ifft on all axes then fft
    save_transforms = None
    save_names = None
    if "ifft" in transforms and "fft" in transforms:
        save_transforms = [axis.transform for axis in axes_list]
        save_names = [axis.name for axis in axes_list]
        for axis in axes_list:
            if axis.name == "freqs":
                axis.transform = "ifft"
                axis.name = "time"
            elif axis.name == "wavenumber":
                axis.transform = "ifft"
                axis.name = "angle"
    # Inverse fft
    if "ifft" in transforms:
        values = comp_ifftn(
            values, axes_list, is_real=self.is_real, axes_list=self.axes
        )
    # Prepare fft in ifft/fft case
    if save_transforms is not None:
        for i, transform in enumerate(save_transforms):
            axes_list[i].name = save_names[i]
            if transform == "fft_axis":
                axes_list[i].transform = "fft"
                save_transforms[i] = "fft"
            else:
                axes_list[i].transform = transform
    # Slices along time/space axes
    values, axes_dict_other = self._extract_slices(values, axes_list)
    # fft
    if "fft" in transforms:
        values = comp_fftn(values, axes_list, is_real=self.is_real)
    # Slices along fft axes
    values = self._extract_slices_fft(values, axes_list)
    # Rebuild symmetries
    values = self._rebuild_symmetries(values, axes_list)
    # Interpolate over axis values
    values = self._interpolate(values, axes_list)
    # Apply operations such as sum, integration, derivations etc.
    values = self._apply_operations(
        values, axes_list, is_magnitude, unit=self.unit, corr_unit=corr_unit
    )
    # Conversions
    values = self._convert(values, unit, is_norm, is_squeeze, axes_list)
    # Return axes and values
    return_dict = {}
    for axis_requested in axes_list:
        if axis_requested.extension in [
            "max",
            "min",
            "sum",
            "rss",
            "mean",
            "rms",
            "integrate",
        ]:
            return_dict[axis_requested.name] = axis_requested.extension
        else:
            return_dict[axis_requested.name] = axis_requested.values
    return_dict[self.symbol] = values
    return_dict["axes_list"] = axes_list
    return_dict["axes_dict_other"] = axes_dict_other
    return return_dict
