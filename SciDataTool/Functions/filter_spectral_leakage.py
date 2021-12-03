import numpy as np
import numpy.linalg as np_lin

from SciDataTool.Functions.set_routines import unique_tol


def filter_spectral_leakage(
    spectrum,
    freqs,
    freqs_th,
    Nt,
    dt,
    is_freq_pos=True,
    Wmatf=np.array([]),
    If=np.array([]),
):
    """Filter spectral leakage from the input spectrum and theoretical frequencies accordingly to the method developed in
    Rainer et al., "Weak Coupling Between Electromagnetic and Structural Models for Electrical Machines",
    IEEE TRANSACTIONS ON MAGNETICS, VOL. 46, NO. 8, AUGUST 2010.

    Parameters
    ----------
    spectrum : ndarray
        Frequency spectrum to filter (1D, 2D or 3D). In case of 2D/3D, angle axis can be wavenumber axis
    freqs_th : ndarray
        theoretical frequencies
    Nt : int
        Number of time steps
    dt: float
        Time step value
    is_freq_pos: bool
        True to return spectrum truncated to positive frequencies
    Wmatf : ndarray
        Filtering matrix
    If: ndarray
        Index of FFT harmonics components used to calculate Wmatf

    Returns
    -------
    spectrum_filt : ndarray
        Filtered spectrum
    freqs_th : ndarray
        theoretical frequencies
    Wmatf : ndarray
        Filtering matrix
    """

    # Expand theoretical frequencies to negative values
    freqs_th = unique_tol(np.concatenate((freqs_th, -freqs_th), axis=0))
    Nfreq = freqs_th.size

    if Wmatf.size == 0 or If.size == 0:

        # Check frequency resolution
        df_fft = np.min(np.abs(np.diff(freqs)))
        df_th = np.min(np.abs(np.diff(freqs_th)))
        if df_th < df_fft:
            print(
                "FFT frequency resolution lower than theoretical frequency resolution, spectral leakage filtering maybe inaccurate"
            )

        # Keep only theoretical frequencies in the calculated range
        I1 = np.abs(freqs_th) <= np.max(freqs)
        freqs_th = freqs_th[I1]

        # Find closest index of each frequency in the grid
        If = np.argmin(np.abs(freqs[:, None] - freqs_th[None, :]), axis=0)

        # Filtering will be performed, match theoretical frequencies with closest
        # frequency in FFT frequency vector
        If0 = np.unique(If)
        if If0.size != If.size:
            If_new = np.zeros(freqs_th.size, dtype=int)
            for ii, jj in enumerate(If):
                kk = jj
                if kk + 1 < freqs.size:
                    # Going forward
                    while kk in If_new:
                        kk += 1
                else:
                    # Going backwards
                    while kk in If_new:
                        kk -= 1
                If_new[ii] = kk
            if np.unique(If_new).size < If.size:
                print(
                    "Wrong match between FFT and theoretical frequencies, spectral leakage filtering maybe inaccurate"
                )
            If = np.sort(If_new)

        # Calculate filtering matrix: spectrum of door window
        xfreqs2, xfreqs1 = np.meshgrid(freqs_th, freqs[If])
        Wmatf = my_doorwin(xfreqs1 - xfreqs2, Nt, dt, tol0=1e-4)
    else:
        Nfreq = Wmatf.shape[0]

    # Check that spectrum is either 1D or 3D
    if spectrum.ndim > 2:
        Nangle = spectrum.shape[1]
        Nslice = spectrum.shape[2]
        if Nslice > 1:
            # Reshape into 2D matrix
            spectrum = np.reshape(spectrum, (Nfreq, Nangle * Nslice))
        is_3D = True
    else:
        # Add 3rd dimension and squeeze after filtering
        is_3D = False

    # Filter spectrum
    spectrum_filt = np_lin.solve(Wmatf, spectrum[If, ...])

    # import matplotlib.pyplot as plt

    # If_max = np.where(freqs > freqs_th.max())[0][0]
    # If_ref = np.arange(If_min, If_max, 1, dtype=int)
    # spec_val = np.abs(np.sqrt(np.sum(spectrum[If_ref, :] ** 2, axis=-1)))
    # spec_val0 = np.abs(np.sqrt(np.sum(spectrum[If, :] ** 2, axis=-1)))
    # # spec_val1 = np.abs(np.sqrt(np.sum(spectrum[If1, :] ** 2, axis=-1)))
    # spec_val_filt = np.abs(np.sqrt(np.sum(spectrum_filt ** 2, axis=-1)))
    # plt.figure()
    # plt.plot(freqs[If_ref], spec_val)
    # plt.plot(freqs[If], spec_val0)
    # # plt.plot(freqs[If1], spec_val1)
    # plt.plot(freqs[If], spec_val_filt)
    # plt.show()

    if is_3D:
        if Nslice > 1:
            # Reshape to initial 3D shape
            spectrum_filt = np.reshape(spectrum_filt, (Nfreq, Nangle, Nslice))
        else:
            # Expand to 3D if requested
            spectrum_filt = spectrum_filt[:, :, None]

    if is_freq_pos:
        # Keep only positive frequencies
        Ip = freqs_th >= 0
        freqs_th = freqs_th[Ip]
        spectrum_filt = spectrum_filt[Ip, ...]

        # Multiply all components by two except zero frequency component
        spectrum_filt *= 2
        I0 = freqs_th == 0
        spectrum_filt[I0, ...] = 0.5 * spectrum_filt[I0, ...]

    return spectrum_filt, freqs_th, Wmatf, If


def my_doorwin(f, Nt, dt, tol0=1e-4):
    """ "Return the Fourier transform of a door window as developed in to the method developed in
    Rainer et al., "Weak Coupling Between Electromagnetic and Structural Models for Electrical Machines",
    IEEE TRANSACTIONS ON MAGNETICS, VOL. 46, NO. 8, AUGUST 2010.

    Parameters
    ----------
    f : ndarray
        frequency array [Hz]
    Nt : int
        Number of time steps
    dt: float
        Time step value
    tol0: float
        absolute tolerance under which frequency is assumed to be 0

    Returns
    -------
    W : ndarray
        Door window Fourier transform

    """

    # Tolerance under which input frequency is considered as 0
    I0 = np.abs(f) > tol0

    W = np.ones([f.shape[0], f.shape[1]], dtype=complex)

    W[I0] = (
        (1 - np.exp(-1j * 2 * np.pi * dt * f[I0] * Nt))
        / (1 - np.exp(-1j * 2 * np.pi * dt * f[I0]))
        / Nt
    )

    return W
