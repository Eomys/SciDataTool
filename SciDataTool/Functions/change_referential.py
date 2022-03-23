import numpy as np
import scipy.interpolate as scp_int

from SciDataTool.Functions.set_routines import unique_tol


def change_referential_spectrum(
    freqs,
    wavenumbers_circ,
    rotation_speed,
    spectrum,
    atol=1e-9,
    freqs_new=np.array([]),
    I1=np.array([]),
    Irf_un=np.array([]),
    is_double_f0=False,
    atol_freq=1e-6,
):
    """Compute a new 2D spectrum depending on a rotating referential defined by a speed.

    Parameters
    ----------
    freqs : ndarray
        frequencies vector
    wavenumbers_circ : ndarray
        circumferential wavenumbers vector
    rotation_speed : float
        rotation speed
    spectrum : ndarray
        2D/3D spectrum with freqs/wavenumbers_circ as two first axes
    atol: float
        Absolute tolerance under which amplitudes are assumed to be 0
    freqs_new : ndarray
        frequencies vector in the new rotating referential
    I1 : ndarray
        Array of component indices in new spectrum
    Irf_un: ndarray
        Array of indices of unique frequency/wavenumber couples
    is_double_f0: bool
        True to multiply spectrum components which have zero frequency and non-zero wavenumber
    atol_freq: float
        Absolute tolerance under which frequencies are assumed to be equal

    Returns
    -------
    spectrum_new : ndarray
        spectrum in the new rotating referential
    freqs_new : ndarray
        frequencies vector in the new rotating referential
    I1 : ndarray
        Array of component indices in new spectrum
    Irf_un: ndarray
        Array of indices of unique frequency/wavenumber couples

    """
    Nf = freqs.size
    Nr = wavenumbers_circ.size
    # Get number of slices depending on input spectrum shape
    if spectrum.ndim > 2:
        Nslice = spectrum.shape[2]
        is_squeeze = False
    else:
        Nslice = 1
        is_squeeze = True
        spectrum = spectrum[:, :, None]

    if freqs_new.size == 0:
        # Calculate new frequency values by shifting frequencies
        Xwavenb, Xfreqs = np.meshgrid(wavenumbers_circ, freqs)
        Xfreqs_new = Xfreqs + Xwavenb * rotation_speed / 60

        # Get unique frequencies
        freqs_new, If0 = unique_tol(
            Xfreqs_new.ravel("C"),
            return_inverse=True,
            axis=0,
            tol=atol_freq,
            is_abs_tol=True,
        )

        # Get frequency/wavenumber_circ position in new matrix [Nf_new, Nr]
        Ir0 = np.tile(np.arange(Nr, dtype=int), Nf)
        Irf = np.concatenate((If0[:, None], Ir0[:, None]), axis=1)

        # Get unique couples of frequency/wavenumber to sum on same harmonics
        Irf_un, I1 = np.unique(Irf, return_inverse=True, axis=0)

    # Number of frequencies in new referential
    Nf_new = freqs_new.size

    if is_double_f0:
        # Multiply by two spectrum components which have f=0, r!=0
        jf0 = np.abs(freqs) < 1e-4
        jr = wavenumbers_circ != 0
        spectrum[jf0, jr, :] = 2 * spectrum[jf0, jr, :]

    # Calculate spectrum amplitude in new referential by summing all contributions
    # which have the same orders and wavenumber for each slice
    spectrum_new = np.zeros((Nf_new, Nr, Nslice), dtype=spectrum.dtype)
    for k in range(Nslice):
        # Reshape values for kth slice columnwise
        amp_k = spectrum[:, :, k].ravel("C")
        # Sum all contributions which have the same orders and wavenumber as given by I1
        if spectrum.dtype == complex:
            # bincount fails on complex numbers, real and imaginary parts must be treated separately
            amp_new_k = np.bincount(I1, weights=amp_k.real) + 1j * np.bincount(
                I1, weights=amp_k.imag
            )
        else:
            amp_new_k = np.bincount(I1, weights=amp_k)
        # Store amplitudes at new frequency/wavenumber positions
        spectrum_new[Irf_un[:, 0], Irf_un[:, 1], k] = amp_new_k

    if is_double_f0:
        # Divide by two spectrum components which have f=0, r!=0
        spectrum[jf0, jr, :] = spectrum[jf0, jr, :] / 2

    if atol > 0:
        # Filter harmonics that are below input absolute tolerance
        Imask = (
            np.sum(np.sum(np.abs(spectrum_new), axis=2), axis=1)
            > np.max(np.abs(spectrum_new)) * atol
        )
        spectrum_new = spectrum_new[Imask, ...]
        freqs_new = freqs_new[Imask]

    if is_squeeze:
        # Squeeze spectrum back to 2D
        spectrum_new = spectrum_new[:, :, 0]

    return spectrum_new, freqs_new, I1, Irf_un


def change_referential_waveform(
    val0,
    time0,
    angle0,
    rotation_speed,
    is_aper_a=False,
    is_aper_t=False,
    ta_in=tuple(),
    ta_out=tuple(),
):
    """Change referential of input 3D array defined on time, angle and z given input rotation speed
    (algebric to include rotation direction)

    Parameters
    ----------
    val0 : ndarray
        Field values in new referential
    time0 : ndarray
        time vector [s]
    angle0 : float
        angle vector [rad]
    rotation_speed : float
        rotation speed [rpm]
    per_a: int
        angle periodicity number (one period)
    is_aper_a: bool
        True if there is a spatial anti-periodicity
    is_aper_t: bool
        True if there is a time anti-periodicity
    ta_in: tuple
        Tuple of input time/angle meshgrids
    ta_out: tuple
        Tuple of output time/angle meshgrids

    Returns
    -------
    val_new : ndarray
        Field values in new referential
    time_new : ndarray
        time vector in new referential [s]
    angle_new : ndarray
        angle vector in new referential [rad]
    ta_in: tuple
        Tuple of input time/angle meshgrids
    ta_out: tuple
        Tuple of output time/angle meshgrids
    """

    # Init size
    Nt = time0.size
    Na = angle0.size
    if val0.ndim > 2:
        Nslice = val0.shape[2]
        is_squeeze = False
    else:
        Nslice = 1
        val0 = val0[:, :, None]
        is_squeeze = True
    shape0 = [Nt, Na, Nslice]

    if len(ta_in) == 0 or len(ta_out) == 0:
        # Add final value to time and space vectors
        tf = time0[-1] + time0[1] - time0[0]
        time1 = np.append(time0, tf)
        alphaf = angle0[-1] + angle0[1] - angle0[0]
        angle1 = np.append(angle0, alphaf)
        ta_in = (time1, angle1)

        # Build 2D meshgrids and flatten them columnwise
        Xangle0, Xtime0 = np.meshgrid(angle0, time0)
        Xtime0, Xangle0 = Xtime0.ravel("C"), Xangle0.ravel("C")

        # Shift angle according to rotation speed
        Xangle_new = (Xangle0 + 2 * np.pi * rotation_speed / 60 * Xtime0) % alphaf
        ta_out = (Xtime0, Xangle_new)

    # 2D interpolate for new angle array
    val_new = np.zeros(shape0)
    valk = np.zeros((Nt + 1, Na + 1))
    for k in range(Nslice):
        # Make current slice periodic along time and space
        valk[0:Nt, 0:Na] = val0[:, :, k]
        valk[-1, :-1] = val0[0, :, k]
        valk[:-1, -1] = val0[:, 0, k]
        valk[-1, -1] = val0[0, 0, k]

        # Perform 2D interpolation
        val_new[:, :, k] = scp_int.RegularGridInterpolator(
            ta_in, valk, method="linear"
        )(ta_out).reshape((Nt, Na))

    if is_aper_t:
        # Remove half part of 1st dimension
        val_new = val_new[: int(Nt / 2), :, :]
        time_new = time0[: int(Nt / 2)]
    else:
        time_new = time0

    if is_aper_a:
        # Remove half part of 2nd dimension
        val_new = val_new[:, : int(Na / 2), :]
        angle_new = angle0[: int(Na / 2)]
    else:
        angle_new = angle0

    if is_squeeze:
        # Remove 3rd dimension
        val_new = val_new[:, :, 0]

    return val_new, time_new, angle_new, ta_in, ta_out
