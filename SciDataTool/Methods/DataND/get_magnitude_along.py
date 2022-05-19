from SciDataTool.Functions import AxisError, NormError, UnitError
from SciDataTool.Functions.conversions import convert, to_dB, to_dBA, to_noct
from SciDataTool.Functions.fix_axes_order import fix_axes_order
from numpy import apply_along_axis, add, take


def get_magnitude_along(
    self,
    *args,
    unit="SI",
    is_norm=False,
    axis_data=[],
    is_squeeze=True,
    is_sum=True,
    corr_unit=None
):
    """Returns the ndarray of the magnitude of the FT, using conversions and symmetries if needed.
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
    list of 1Darray of axes values, ndarray of magnitude values
    """
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args

    # Fix axes order
    args = fix_axes_order([axis.name for axis in self.get_axes()], args)

    # For dB/dBA conversions, first extraction with freqs axis
    if "dB" in unit and unit != self.unit and is_sum:
        new_args = list(args).copy()
        freq_name = None
        index_freq = None
        index_speed = None
        index_order = None
        args_freqs = ["freqs", "frequency", "time"]
        for i, axis in enumerate(self.axes):  # Find frequency axis
            if axis.name in args_freqs:
                freq_name = axis.name
        if freq_name is not None:
            for i, arg in enumerate(args):
                if freq_name in arg:
                    if "sum" in arg or "rss" in arg:
                        new_args[i] = freq_name
                        index_freq = i
            if index_freq is None:  # No sum on freqs axis -> can extract directly
                return self.get_magnitude_along(
                    *args,
                    axis_data=axis_data,
                    unit=unit,
                    is_squeeze=is_squeeze,
                    is_sum=False,
                )
            else:
                data = self.get_data_along(
                    *new_args, axis_data=axis_data, unit=unit
                )  # Extract first along freqs axis
                return data.get_magnitude_along(
                    *[args[index_freq]],
                    axis_data=axis_data,
                    unit=unit,
                    is_squeeze=is_squeeze,
                    is_sum=False,
                    corr_unit=self.unit,
                )  # Then sum on freqs axis
        else:  # Try speed/order
            is_match = 0
            for i, axis in enumerate(self.axes):  # Find frequency axis
                if axis.name == "speed":
                    is_match += 1
                    arg_speed = "speed"
                elif axis.name == "order":
                    is_match += 1
                elif "speed" in axis.normalizations:
                    is_match += 1
                    arg_speed = axis.name + "->speed"
            if is_match == 2:
                for i, arg in enumerate(args):
                    if "speed" in arg:
                        if arg.split("{")[0] != arg_speed:
                            new_args[i] = arg_speed
                            index_speed = i
                    elif "order" in arg:
                        if arg.split("{")[0] != "order":
                            new_args[i] = "order"
                            index_order = i
            elif is_match == 1:
                for i, arg in enumerate(args):
                    if "speed" in arg:
                        if arg.split("{")[0] != arg_speed:
                            new_args[i] = arg_speed
                            index_speed = i
            elif unit == "dB" or "A-weight" in self.normalizations:
                self.get_magnitude_along(
                    *args,
                    axis_data=axis_data,
                    unit=unit,
                    is_squeeze=is_squeeze,
                    is_sum=False,
                )
            else:
                raise AxisError(
                    "Cannot convert to " + unit + " without a frequency axis"
                )
            if (
                index_speed is None and index_order is None
            ):  # No sum on freqs axis -> can extract directly
                return self.get_magnitude_along(
                    *args,
                    axis_data=axis_data,
                    unit=unit,
                    is_squeeze=is_squeeze,
                    is_sum=False,
                )
            elif index_speed is None:  # Sum on order axis
                if "[" in args[-1]:
                    new_args[-1] = args[-1].split("[")[0]
                data = self.get_data_along(
                    *new_args, axis_data=axis_data, unit=unit
                )  # Extract first along order axis
                return data.get_magnitude_along(
                    *[arg_speed, args[index_order]] + args[2:],
                    axis_data=axis_data,
                    unit=unit,
                    is_squeeze=is_squeeze,
                    is_sum=False,
                    corr_unit=self.unit,
                )  # Then sum on order axis
            elif index_order is None:  # Sum on speed axis
                data = self.get_data_along(
                    *new_args, axis_data=axis_data, unit=unit
                )  # Extract first along speed axis
                return data.get_magnitude_along(
                    *args,
                    axis_data=axis_data,
                    unit=unit,
                    is_squeeze=is_squeeze,
                    is_sum=False,
                    corr_unit=self.unit,
                )  # Then sum on speed axis
            else:  # Sum on speed and order axes
                data = self.get_data_along(
                    *new_args, axis_data=axis_data, unit=unit
                )  # Extract first along speed and order axes
                return data.get_magnitude_along(
                    *[args[index_speed], args[index_order]],
                    axis_data=axis_data,
                    unit=unit,
                    is_squeeze=is_squeeze,
                    is_sum=False,
                    corr_unit=self.unit,
                )  # Then sum on speed and order axes

    else:

        return_dict = self.get_along(
            *args,
            axis_data=axis_data,
            is_squeeze=is_squeeze,
            is_magnitude=True,
            corr_unit=corr_unit,
        )
        values = return_dict[self.symbol]

        # 1/nth octave band
        for axis in return_dict["axes_list"]:
            if axis.name == "freqs" or axis.corr_name == "freqs":
                index = axis.index
                if axis.noct is not None:
                    (values, foct) = apply_along_axis(
                        to_noct, index, values, return_dict["freqs"], noct=axis.noct
                    )
                    return_dict[axis.name] = foct
        # Convert into right unit (apart because of dBA conversion)
        if unit == self.unit or unit == "SI":
            if is_norm:
                try:
                    values = self.normalizations["ref"].normalize(values)
                except:
                    raise NormError("Reference value not specified for normalization")
        elif unit == "dB":
            ref_value = 1.0
            if "ref" in self.normalizations:
                ref_value *= self.normalizations["ref"].ref
            values = to_dB(values, self.unit, ref_value)
        elif unit == "dBA":
            ref_value = 1.0
            if "ref" in self.normalizations:
                ref_value *= self.normalizations["ref"].ref
            if "A-weight" in self.normalizations:
                values = to_dB(values, self.unit, ref_value)
                # Extract requested indices from A-weight
                axes_list = return_dict["axes_list"]
                index_list = []
                for ii, axis in enumerate(axes_list):
                    if (
                        axis.indices is not None
                        and len(axis.indices) > 1
                        and len(axis.indices) < len(axis.values)
                    ):
                        index_list.append(ii)
                A_weight = self.normalizations["A-weight"].vector
                for index in index_list:
                    A_weight = take(
                        A_weight,
                        axes_list[index].indices,
                        axis=index,
                    )
                # Flatten to apply A-weighting
                A_weight = A_weight.ravel("C")
                shape = values.shape
                values = values.reshape(
                    A_weight.shape
                    + shape[len(self.normalizations["A-weight"].vector.shape) :]
                )
                values = apply_along_axis(add, 0, values, A_weight)
                values = values.reshape(shape)
            elif "freqs" in return_dict.keys():
                for axis in return_dict["axes_list"]:
                    if axis.name == "freqs" or axis.corr_name == "freqs":
                        index = axis.index
                else:
                    if return_dict["axes_list"][
                        index
                    ].corr_values is not None and return_dict["axes_list"][
                        index
                    ].unit not in [
                        "SI",
                        return_dict["axes_list"][index].corr_unit,
                    ]:
                        freqs = return_dict["axes_list"][index].corr_values
                    else:
                        freqs = return_dict["freqs"]
                values = apply_along_axis(
                    to_dBA, index, values, freqs, self.unit, ref_value
                )
            elif "frequency" in return_dict.keys():
                for axis in return_dict["axes_list"]:
                    if axis.name == "frequency" or axis.corr_name == "frequency":
                        index = axis.index
                else:
                    if return_dict["axes_list"][
                        index
                    ].corr_values is not None and return_dict["axes_list"][
                        index
                    ].unit not in [
                        "SI",
                        return_dict["axes_list"][index].corr_unit,
                    ]:
                        freqs = return_dict["axes_list"][index].corr_values
                    else:
                        freqs = return_dict["frequency"]
                values = apply_along_axis(
                    to_dBA, index, values, freqs, self.unit, ref_value
                )
            elif "order" in return_dict:
                freqs = self._get_freqs()
                freqs = freqs.ravel("C")
                shape = values.shape
                values = values.reshape(freqs.shape + shape[2:])
                values = apply_along_axis(
                    to_dBA, 0, values, freqs, self.unit, ref_value
                )
                values = values.reshape(shape)
            else:
                raise UnitError(
                    "dBA conversion only available for fft with frequencies"
                )

        elif unit in self.normalizations:
            values = self.normalizations.get(unit).normalize(values)
        else:
            values = convert(values, self.unit, unit)
        return_dict[self.symbol] = values
        return return_dict
