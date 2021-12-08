from numpy import any as np_any

from SciDataTool.Functions.sum_convolution import get_sum_indices, get_sum_amplitudes


def sum(
    self,
    other,
    tol_freq=1e-4,
    name=None,
    symbol=None,
    unit=None,
    normalizations=None,
):
    """Merge two DataFreq objects

    Parameters
    ----------
    self : DataFreq
        A DataFreq object
    other : DataFreq
        Another DataFreq object
    tol_freq: float
        Absolute tolerance value to filter harmonic orders by their frequency value
    name: str
        name
    symbol: str
        symbol
    unit: str
        unit
    normalizations: {Normalization}
        Dict of normalization objects

    Returns
    -------
    result : Spectrum
        DataFreq object resulting from summing both DataFreq objects
    """

    if not isinstance(other, type(self)):
        raise Exception("other is not a DataFreq object")

    if len(self.axes) > 1:
        raise Exception("self contains more than one axis")

    if len(other.axes) > 1:
        raise Exception("other contains more than one axis")

    if self.axes[0].name != "freqs":
        raise Exception("self axis is not frequency axis")
    else:
        freqs1 = self.axes[0].get_values()
        if np_any(freqs1) < 0:
            raise Exception("self contains negative frequency values")

    if other.axes[0].name != "freqs":
        raise Exception("other axis is not frequency axis")
    else:
        freqs2 = other.axes[0].get_values()
        if np_any(freqs2) < 0:
            raise Exception("other contains negative frequency values")

    # Fill metadata
    if name is None:
        name = self.name
    if symbol is None:
        symbol = self.symbol
    if unit is None:
        unit = self.unit
    if normalizations is None:
        normalizations = self.normalizations

    # Compute spectrum orders resulting from convolution
    freqs_un, I0b = get_sum_indices(freqs1, freqs2, tol_freq)

    # Compute spectrum amplitudes resulting from convolution
    amp = get_sum_amplitudes(self.values, other.values, I0b)

    # Create Frequency axis
    Freqs = self.axes[0].copy()
    Freqs.values = freqs_un

    # Create DataFreq resulting from convolution
    result = type(self)(
        name=name,
        unit=unit,
        symbol=symbol,
        axes=[Freqs],
        values=amp,
        normalizations=normalizations,
    )

    return result
