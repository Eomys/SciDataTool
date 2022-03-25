import numpy as np

from SciDataTool.Functions.change_referential import (
    change_referential_spectrum,
    change_referential_waveform,
)
from SciDataTool.Functions.Load.import_class import import_class


def change_referential(
    self,
    rotation_speed,
    is_waveform,
    atol=1e-9,
    axes_list_change=list(),
    arg_list=list(),
    freqs_new=np.array([]),
    I1=np.array([]),
    Irf_un=np.array([]),
    sym_t_new=dict(),
    ta_in=tuple(),
    ta_out=tuple(),
    atol_freq=1e-6,
):
    """Change referential of a SciDataTool DataND object

    Parameters
    ----------
    self : DataND
        a DataND object
    rotation_speed : float
        rotation speed [rpm]
    is_waveform: bool
        True to perform referential change in waveform domain (time/space) otherwise perform it in spectral domain (freqs/wavenumber)
    atol: float
        Absolute tolerance under which amplitudes are assumed to be 0
    axes_list_change : [Data]
        Axes list to be stored in referential changed DataFreq
    arg_list: list
        List of strings to call get_along
    freqs_new : ndarray
        frequencies vector in the new rotating referential
    I1 : ndarray
        Array of component indices in new spectrum
    Irf_un: ndarray
        Array of indices of unique frequency/wavenumber couples
    ta_in: tuple
        Tuple of input time/angle meshgrids
    ta_out: tuple
        Tuple of output time/angle meshgrids
    atol_freq: float
        Absolute tolerance under which frequencies are assumed to be equal

    Returns
    -------
    data_new : DataND
        a DataND object in new referential
    axes_list_change : [Data]
        Axes list to be stored in changed DataND
    arg_list: list
        List of strings to call get_along
    freqs_new : ndarray
        frequencies vector in the new rotating referential
    I1 : ndarray
        Array of component indices in new spectrum
    Irf_un: ndarray
        Array of indices of unique frequency/wavenumber couples
    ta_in: tuple
        Tuple of input time/angle meshgrids
    ta_out: tuple
        Tuple of output time/angle meshgrids

    """

    Data1D = import_class("SciDataTool.Classes", "Data1D")
    DataLinspace = import_class("SciDataTool.Classes", "DataLinspace")
    DataPattern = import_class("SciDataTool.Classes", "DataPattern")

    if is_waveform:
        DataClass = import_class("SciDataTool.Classes", "DataTime")
    else:
        DataClass = import_class("SciDataTool.Classes", "DataFreq")

    # Get axes list
    axes_list = self.get_axes()
    axes_name = [axis.name for axis in axes_list]

    if len(arg_list) == 0:
        # Get fft along frequency axis (keep other axes)
        arg_list = list()
        for axis in axes_list:
            if axis.name == "time":
                if is_waveform:
                    arg_list.append("time[oneperiod]")
                else:
                    arg_list.append("freqs")
            elif axis.name == "angle":
                if is_waveform:
                    arg_list.append("angle[oneperiod]")
                else:
                    arg_list.append("wavenumber")
            elif axis.name == "z" and isinstance(axis, DataPattern):
                arg_list.append("z[smallestpattern]")
            else:
                arg_list.append(axis.name)

    # Referential changed is requested in waveform domain if time is in arg_list
    is_waveform = "time[oneperiod]" in arg_list

    if not is_waveform and hasattr(self, "is_real"):
        # Force non real data to get all spectrum
        is_real = self.is_real
        self.is_real = False
    else:
        is_real = True

    # Extract data from vectorfield on one period
    result = self.get_along(*arg_list, is_squeeze=False)
    values = result[self.symbol]

    if is_waveform:
        # Get axes values
        time0 = result["time"]
        angle0 = result["angle"]

        # Check requested time anti-periodicity
        is_aper_t = "antiperiod" in sym_t_new

        # Get angle periodicity on one period
        per_a, is_aper_a = axes_list[1].get_periodicity()
        per_a = int(per_a / 2) if is_aper_a else per_a

        val_new, time_new, angle_new, ta_in, ta_out = change_referential_waveform(
            values,
            time0,
            angle0,
            rotation_speed,
            is_aper_a,
            is_aper_t,
            ta_in,
            ta_out,
        )
    else:
        freqs = result["freqs"]
        wavenumber = result["wavenumber"]

        val_new, freqs_new, I1, Irf_un = change_referential_spectrum(
            freqs,
            wavenumber,
            rotation_speed,
            values,
            atol=atol,
            freqs_new=freqs_new,
            I1=I1,
            Irf_un=Irf_un,
            is_double_f0=is_real and "freqs" in axes_name,
            atol_freq=atol_freq,
        )

        if is_real:
            # Adapt spectrum amplitude
            if "time" in axes_name:
                # Input data is DataTime, FFT has just been performed in four quadrants
                # so all amplitudes are multiplied by 2 after restriction to positive frequencies
                coeff = 2
            else:
                # Input data is DataFreq, since data is a real spectrum no need to multiply again
                # all harmonics by two
                coeff = 1

            # Restrict spectrum to positive frequencies only and multiply amplitudes by coeff
            Ifreq_pos = freqs_new >= 0
            freqs_store = freqs_new[Ifreq_pos]
            val_new = val_new[Ifreq_pos] * coeff
            val_new[0] = val_new[0] / coeff
        else:
            freqs_store = freqs_new

    if len(axes_list_change) == 0:
        axes_list_change = list()
        for axis in axes_list:

            if axis.name == "time" and is_waveform:
                axis_new = axis.copy()
                axis_new.symmetries = sym_t_new
                axis_new.number = time_new.size
                if isinstance(axis_new, DataLinspace):
                    axis_new.final = time_new[-1]
                    axis_new.include_endpoint = True
                else:
                    axis_new.values = time0

            elif axis.name == "angle" and is_waveform:
                axis_new = axis.copy()
                if is_aper_a:
                    axis_new.symmetries = {"antiperiod": int(2 * per_a)}
                else:
                    axis_new.symmetries = {"period": per_a}
                axis_new.number = angle_new.size
                if isinstance(axis_new, DataLinspace):
                    axis_new.final = angle_new[-1]
                    axis_new.include_endpoint = True
                else:
                    axis_new.values = angle_new

            elif axis.name == "freqs" or (axis.name == "time" and not is_waveform):
                axis_new = Data1D(
                    name="freqs",
                    unit="Hz",
                    values=freqs_store,
                    normalizations=axis.normalizations.copy(),
                    symmetries=dict(),  # Don't keep time symmetries, FFT inverse requests axis_data
                )

            elif axis.name == "wavenumber" or (
                axis.name == "angle" and not is_waveform
            ):
                axis_new = Data1D(
                    name="wavenumber",
                    unit="dimless",
                    values=wavenumber,
                    normalizations=axis.normalizations.copy(),
                    symmetries=axis.symmetries.copy(),
                )

            else:
                axis_new = axis.copy()

            axes_list_change.append(axis_new)

    data_new = DataClass(
        name=self.name,
        symbol=self.symbol,
        unit=self.unit,
        axes=axes_list_change,
        values=val_new,
        normalizations=self.normalizations.copy(),
        is_real=is_real,
    )

    if not is_waveform and hasattr(self, "is_real"):
        # Reset data
        self.is_real = is_real

    return data_new, axes_list_change, arg_list, freqs_new, I1, Irf_un, ta_in, ta_out
