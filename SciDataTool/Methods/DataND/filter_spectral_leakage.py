import numpy as np

from SciDataTool.Functions.filter_spectral_leakage import (
    filter_spectral_leakage as filter_spectral_leakage_fct,
)


def filter_spectral_leakage(
    self,
    freqs_th,
    axes_list_filt=list(),
    arg_list=list(),
    Wmatf=np.array([]),
    If=np.array([]),
    is_return_calc_data=False,
):
    """Filter spectral leakage from a SciDataTool DataND object

    Parameters
    ----------
    self : DataND
        a DataND object
    freqs_th : ndarray
        theoretical frequencies
    axes_list_filt : [Data]
        Axes list to be stored in filtered DataFreq
    arg_list : list
        List of axes arguments to call SciDataTool get_along()
    Wmatf : ndarray
        Filtering matrix
    If: ndarray
        Index of FFT harmonics components used to calculate Wmatf
    is_return_all_args: bool
        True to return all data that can be used to speed calculation for further use

    Returns
    -------
    data_filt : DataND
        a DataND object
    axes_list_filt : [Data]
        Axes list to be stored in filtered DataFreq
    arg_list : list
        List of axes arguments to call SciDataTool get_along()
    Wmatf : ndarray
        Filtering matrix
    If: ndarray
        Index of FFT harmonics components used to calculate Wmatf
    """

    module = __import__("SciDataTool.Classes.DataFreq", fromlist=["DataFreq"])
    DataFreq = getattr(module, "DataFreq")

    module = __import__("SciDataTool.Classes.DataPattern", fromlist=["DataPattern"])
    DataPattern = getattr(module, "DataPattern")

    module = __import__("SciDataTool.Classes.Data1D", fromlist=["Data1D"])
    Data1D = getattr(module, "Data1D")

    if len(axes_list_filt) == 0 or len(arg_list) == 0:
        # Get fft along frequency axis (keep other axes)
        arg_list = list()  # Reinstantiate a different list
        axes_list = self.get_axes()
        for axis in axes_list:
            if axis.name == "time":
                arg_list.append("freqs")
            elif axis.name == "angle":
                arg_list.append("wavenumber")
            elif axis.name == "z" and isinstance(axis, DataPattern):
                arg_list.append("z[smallestpattern]")
            else:
                arg_list.append(axis.name)

    is_real = self.is_real
    self.is_real = False  # To have negative frequencies
    result = self.get_along(*arg_list)
    freqs = result["freqs"]
    spectrum = result[self.symbol]

    if Wmatf.size == 0:
        # Get time step
        Time = self.get_axes("time")
        if len(Time) > 0:
            time = Time[0].get_values()
        else:
            result_time = self.get_along("time")
            time = result_time["time"]
        dt = time[1] - time[0]
        Nt = time.size
    else:
        Nt, dt = None, None

    if is_real and np.where(freqs < 0)[0].size == 0:
        # Mirror values to negative frequencies
        If0 = freqs != 0
        spectrum[If0, ...] *= 0.5
        If0[-1] = bool(np.mod(freqs.size, 2) == 0)
        freqs = np.concatenate((-np.flip(freqs), freqs[If0]))
        spectrum = np.concatenate(
            (
                np.flip(np.conj(spectrum)),
                spectrum[If0, ...],
            ),
            axis=0,
        )

    # Restrict filtering to negative wavenumber only
    if is_real and "wavenumber" in result:
        wavenumber = result["wavenumber"]
        Irn = wavenumber <= 0
        spectrum = spectrum[:, Irn, ...]

    spectrum_filt, freqs_th, Wmatf, If = filter_spectral_leakage_fct(
        spectrum, freqs, freqs_th, Nt, dt, is_freq_pos=False, Wmatf=Wmatf, If=If
    )

    if is_real:
        # Multiply all components by two except zero frequency component
        spectrum_filt *= 2
        I0 = freqs_th == 0
        spectrum_filt[I0, ...] = 0.5 * spectrum_filt[I0, ...]

        # Keep only positive frequencies
        Ifp = freqs_th >= 0
        freqs_th = freqs_th[Ifp]

        # Mirror spectrum
        if "wavenumber" in result:
            # Mirror negative frequencies to negative wavenumbers
            Ifn = ~Ifp
            if freqs_th[0] == 0:
                Ifn[I0] = True
            spectrum_filt = np.concatenate(
                (
                    spectrum_filt[Ifp, ...],
                    np.flip(np.conj(spectrum_filt[Ifn, 1:-1, ...])),
                ),
                axis=1,
            )
        else:
            spectrum_filt = spectrum_filt[Ifp, ...]

    if len(axes_list_filt) == 0:
        axes_list_filt = list()  # Reinstantiate a different list
        axes_list_filt.append(
            Data1D(
                name="freqs",
                unit="Hz",
                values=freqs_th,
                normalizations=axes_list[0].normalizations,
                symmetries=dict(),
            )
        )

        if "wavenumber" in result:
            axes_list_filt.append(
                Data1D(
                    name="wavenumber",
                    unit="dimless",
                    values=result["wavenumber"],
                    normalizations=axes_list[1].normalizations,
                    symmetries=axes_list[1].symmetries,
                )
            )

        # Copy other axes
        if "angle" in [axis.name for axis in self.axes]:
            n = 2
        else:
            n = 1
        for axis in axes_list[n:]:
            axes_list_filt.append(axis.copy())

    data_filt = DataFreq(
        name=self.name,
        symbol=self.symbol,
        unit=self.unit,
        axes=axes_list_filt,
        values=spectrum_filt,
        normalizations=self.normalizations,
        is_real=True,
    )

    self.is_real = is_real

    if is_return_calc_data:
        return data_filt, axes_list_filt, arg_list, Wmatf, If

    else:
        return data_filt
