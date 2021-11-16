class FTError(Exception):
    """Raised when there is an error within the Fourier Transform methods (Data Object)"""

    pass


class AxisError(FTError):
    """Raised when the axis requested is not available (Data Object)"""

    pass


class UnitError(FTError):
    """Raised when the unit requested is not available or does not match the existing one (Data Object)"""

    pass


class NormError(FTError):
    """Raised when the normalization cannot be applied (Data Object)"""

    pass


axes_dict = {
    "angle": ["wavenumber", "ifft", "rad"],
    "time": ["freqs", "ifft", "s"],
    "xyz": ["rphiz", "pol2cart", "m"],
}

rev_axes_dict = {
    "wavenumber": ["angle", "fft", "dimless"],
    "freqs": ["time", "fft", "Hz"],
    "rphiz": ["xyz", "cart2pol", "m"],
}
