# -*- coding: utf-8 -*-
from SciDataTool.Functions import NormError
from SciDataTool.Functions.fft_functions import comp_magnitude, comp_nthoctave_axis
from SciDataTool.Functions.symmetries import rebuild_symmetries
from SciDataTool.Functions.conversions import convert, to_dB, to_dBA
from numpy import array, take, squeeze, argwhere, log10, sum as np_sum


def get_nthoctave(self, noct, freqmin, freqmax, unit="SI", is_norm=False):
    """Returns the spectrum in the 1/n octave band.
    Parameters
    ----------
    self: Data
        a Data object
    noct: int
        kind of octave band (1/3, etc)
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
    # Extract the frequency axis
    freqs = self.get_FT_axis("freqs")
    # Compute the 1/n octave axis
    f_oct = comp_nthoctave_axis(noct, freqmin, freqmax)
    # Rebuild symmetries for "time"
    values = self.values
    for index, axis in enumerate(self.axes):
        if axis.name == "time" and axis.name in self.symmetries.keys():
            values = rebuild_symmetries(values, index, self.symmetries.get(axis.name))
    # Extract the slices of the field
    for index, axis in enumerate(self.axes):
        if axis.name != "time":
            values = take(values, [0], axis=index)
    # Eliminate dimensions=1
    values = squeeze(values)
    # Perform Fourier Transform
    values = comp_magnitude(values)
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
        if "ref" in self.normalizations.keys():
            ref_value *= self.normalizations.get("ref")
        values = to_dBA(values, freqs, self.unit, ref_value)
    elif unit in self.normalizations:
        values = values / self.normalizations.get(unit)
    else:
        values = convert(values, self.unit, unit)
    # Compute sum over each interval
    freqbds = [f / (2 ** (1.0 / (2.0 * noct))) for f in f_oct]
    freqbds.append(freqbds[-1])
    values_oct = []
    for i in range(len(freqbds) - 1):
        f1 = freqbds[i]
        f2 = freqbds[i + 1]
        indices = argwhere((freqs >= f1) & (freqs <= f2))
        if len(indices) == 0:
            values_oct.append(0)
        else:
            values2 = take(values, indices)
            if np_sum(values2) == 0:
                values_oct.append(0)
            else:
                values_oct.append(10 * log10(np_sum(10 ** (0.1 * values2))))
    values = array(values_oct)
    return [f_oct, values]
