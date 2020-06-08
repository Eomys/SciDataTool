# -*- coding: utf-8 -*-
class FTError(Exception):
    """Raised when there is an error within the Fourier Transform methods (Data Object)
    """

    pass


class AxisError(FTError):
    """Raised when the axis requested is not available (Data Object)
    """

    pass


class UnitError(FTError):
    """Raised when the unit requested is not available or does not match the existing one (Data Object)
    """

    pass


class NormError(FTError):
    """Raised when the unit requested is not available or does not match the existing one (Data Object)
    """

    pass


axes_dict = {
    "angle": ["wavenumber", "ifft"],
    "time": ["freqs", "ifft"],
    "xyz": ["rphiz", "pol2cart"],
}

rev_axes_dict = {
    "wavenumber": ["angle", "fft"],
    "freqs": ["time", "fft"],
    "rphiz": ["xyz", "cart2pol"],
}