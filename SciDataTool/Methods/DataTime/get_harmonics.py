# -*- coding: utf-8 -*-
from SciDataTool.Functions import AxisError, NormError, UnitError
from SciDataTool.Functions.fft_functions import comp_fft
from SciDataTool.Functions.symmetries import rebuild_symmetries
from SciDataTool.Functions.conversions import convert, to_dB, to_dBA
from SciDataTool.Functions.parser import read_input_strings
from SciDataTool.Functions.interpolations import get_common_base, get_interpolation
from numpy import (
    squeeze,
    take,
    apply_along_axis,
    argsort,
    negative,
    meshgrid,
    abs as np_abs,
)
from os import sys


def get_harmonics(self, N_harm, *args, unit="SI", is_norm=False, is_flat=False):
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
    # Read the axes input in args
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args
    axes_list = read_input_strings(args, [])
    # Extract the requested axes (symmetries + unit)
    for i, axis_requested in enumerate(axes_list):
        if axis_requested[3] == "values":
            # Get original values of the axis
            axis_requested.append(
                self.get_FT_axis(axis_requested[0] + axis_requested[1])
            )
            # Interpolate axis with input data
            if str(axis_requested[4]) == "whole":
                axis_requested[4] = axis_requested[5]
                axis_requested[5] = "whole"
            else:
                axis_requested[4] = get_common_base(
                    axis_requested[5], axis_requested[4]
                )
        # Change fft name for the slices of the field
        if axis_requested[0] == "freqs":
            axis_requested[0] = "time"
        elif axis_requested[0] == "wavenumber":
            axis_requested[0] = "angle"
    # Check if the requested axis is defined in the Data object
    for axis_requested in axes_list:
        axis_name = axis_requested[0]
        is_match = False
        for index, axis in enumerate(self.axes):
            if axis.name == axis_name:
                is_match = True
                break
        if not is_match:
            sys.stderr.write(
                "WARNING: Requested axis ["
                + axis_name
                + "] is not available and will be ignored"
            )
            axes_list.remove(axis_requested)
    # Rebuild symmetries of field if axis is extracted
    values = self.values
    for index, axis in enumerate(self.axes):
        for axis_requested in axes_list:
            if axis.name in self.symmetries.keys() and axis.name == axis_requested[0]:
                values = rebuild_symmetries(
                    values, index, self.symmetries.get(axis.name)
                )
                break
    # Extract the slices of the field (single values)
    for index, axis in enumerate(self.axes):
        is_match = False
        for axis_requested in axes_list:
            if axis.name == axis_requested[0]:
                is_match = True
                if axis_requested[3] == "indices" and axis_requested[2] == "single":
                    values = take(values, axis_requested[4], axis=index)
                    break
        if not is_match:  # Axis was not specified -> take slice at the first value
            values = take(values, [0], axis=index)
    # Eliminate dimensions=1
    values = squeeze(values)
    # Interpolate over axis values (single values)
    for index, axis in enumerate(self.axes):
        for axis_requested in axes_list:
            if (
                axis.name == axis_requested[0]
                and axis_requested[3] == "values"
                and axis_requested[2] == "single"
            ):
                values = apply_along_axis(
                    get_interpolation,
                    index,
                    values,
                    axis_requested[5],
                    axis_requested[4],
                )
                break
    # Eliminate dimensions=1
    values = squeeze(values)
    # Perform Fourier Transform
    values = np_abs(comp_fft(values))
    # Extract slices again (intervals)
    index = 0
    for axis_requested in axes_list:
        for axis in self.axes:
            if axis.name == axis_requested[0]:
                if axis_requested[2] == "indices" and axis_requested[2] == "interval":
                    values = take(values, axis_requested[4], axis=index)
                index += 1
                break
    # Interpolate over axis values again (intervals)
    index = 0
    for axis_requested in axes_list:
        for axis in self.axes:
            if (
                axis.name == axis_requested[0]
                and axis_requested[3] == "values"
                and axis_requested[2] == "interval"
            ):
                values = apply_along_axis(
                    get_interpolation,
                    index,
                    values,
                    axis_requested[5],
                    axis_requested[4],
                )
                index += 1
                break
    # Test if data is 1D or 2D
    if len(values.shape) > 2:
        raise AxisError("ERROR: only 1D or 2D implemented")
    else:
        # Convert into right unit
        if unit == self.unit or unit == "SI":
            if is_norm:
                try:
                    values = values / self.normalizations.get("ref")
                except:
                    raise NormError(
                        "ERROR: Reference value not specified for normalization"
                    )
        elif unit == "dB":
            ref_value = 1.0
            if "ref" in self.normalizations.keys():
                ref_value *= self.normalizations.get("ref")
            values = to_dB(values, self.unit, ref_value)
        elif unit == "dBA":
            ref_value = 1.0
            is_match = False
            if "ref" in self.normalizations.keys():
                ref_value *= self.normalizations.get("ref")
            for axis_requested in axes_list:
                if axis_requested[0] == "time":
                    is_match = True
                    values = to_dBA(values, axis_requested[4], self.unit, ref_value)
            if not is_match:
                raise UnitError(
                    "ERROR: dBA conversion only available for fft with frequencies"
                )
        elif unit in self.normalizations:
            values = values / self.normalizations.get(unit)
        else:
            values = convert(values, self.unit, unit)
        # 1D case
        if len(values.shape) == 1:
            for axis_requested in axes_list:
                if axis_requested[2] == "interval":
                    axis_values = axis_requested[4]
            indices = argsort(negative(values))
            indices = indices[:N_harm]
            axis_values = axis_values[indices]
            return [axis_values, values]
        # 2D case
        else:
            for axis_requested in axes_list:
                if axis_requested[0] == "angle":
                    r = axis_requested[4]
                elif axis_requested[0] == "time":
                    f = axis_requested[4]
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
            return [f, r, values]
