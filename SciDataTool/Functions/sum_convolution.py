import numpy as np

from SciDataTool.Functions.set_routines import unique_tol


def get_conv_indices(freqs1, freqs2, f_min, f_max, tol_freq):
    """Compute frequency array and return indices to perform DataFreq convolution

    Parameters
    ----------
    freqs1 : ndarray
        frequency array of first DataFreq
    freqs2 : ndarray
        frequency array of second DataFreq
    f_min: Float
        Minimum frequency of convolved spectrum [Hz]
    f_max: Float
        Maximum frequency of convolved spectrum [Hz]
    tol_freq: Float
        Absolute tolerance value to filter harmonic orders by their frequency value

    Returns
    -------
    freqs_un : ndarray
        frequency array of the convolved spectrum
    I0a: ndarray
        array of indices to extract only amplitudes which are kept for convolution (positive half of the spectrum)
    I0b: ndarray
        True = to get array of positive half of spectrum
        False = to get array of negative part of spectrum
    I1: ndarray
        array on which amplitudes are accumulated
    I2: ndarray
        index of constant component
    """

    # In case f_min is zero, consider also negative frequencies larger than tol_freq
    if f_min in [0, None]:
        f_min = -tol_freq

    # Get harmonic numbers in both spectrums
    Nh1 = freqs1.size
    Nh2 = freqs2.size

    # Compute the order array containing all combinations of input frequencies
    # Mirror n1 and n2 with their negative parts
    f1_0 = np.concatenate((freqs1, -freqs1), axis=0)
    f2_0 = np.concatenate((freqs2, -freqs2), axis=0)

    # Calculate meshgrid
    f1_1, f2_1 = np.meshgrid(f1_0, f2_0)

    # Calculate all frequency combinations and flatten grids
    freqs = f1_1.ravel("C") + f2_1.ravel("C")

    # Restrict convolution to f_min, f_max
    I0 = np.logical_and.reduce((freqs >= f_min, freqs <= f_max))

    # Keep only unique rows in order array

    freqs_un, I1 = unique_tol(
        freqs[I0],
        return_inverse=True,
        return_index=False,
        axis=0,
        is_abs_tol=True,
        tol=tol_freq,
    )

    # Find indices of positive frequencies to be kept
    I0a = np.where(I0)[0]

    if np.any(np.abs(freqs1) < tol_freq) and np.any(np.abs(freqs2) < tol_freq):
        # Convolution product cannot be optimized using conjugate property
        I0b = np.array([])
    else:
        # Find indices of components that will be conjugated
        I0b = I0a + 1 <= 2 * Nh1 * Nh2

        # Shift indices of the conjugated part to link them to their conjugate
        I0a[~I0b] = I0a[~I0b] + Nh1 - 2 * Nh1 * Nh2

    # Find f=0 component to divide by two after convolution
    I2 = np.where(freqs_un < tol_freq)[0]

    return freqs_un, I0a, I0b, I1, I2


def get_conv_amplitudes(amp1, amp2, I0a, I0b, I1, I2):
    """Compute amplitudes resulting from the convolution of input values

    Parameters
    ----------
    amp1: ndarray
        amplitude of first spectrum
    amp2: ndarray
        amplitude of second spectrum
    I0a: ndarray
        array of positive half of spectrum
    I0b: ndarray
        array of negative part of spectrum
    I1: ndarray
        array on which amplitudes are accumulated
    I2: ndarray
        index of constant component

    Returns
    -------
    amp: ndarray
        array of harmonics amplitude
    """

    # Duplicate and conjugate complex magnitudes to account for negative frequencies (1st half)
    amp1_1 = np.concatenate((amp1, np.conjugate(amp1)), axis=0)

    if I0b.size > 0:
        # Use conjugate property to reduce outer product size
        # Outer product of both complex amplitude vectors to calculte all harmonic combinations
        amp3 = np.outer(amp1_1, amp2).ravel("F")

        # Duplicate and conjugate complex magnitudes to account for negative frequencies (2nd half)
        amp_full = (
            np.concatenate((amp3[I0a[I0b]], np.conjugate(amp3[I0a[~I0b]])), axis=0) / 2
        )

    else:
        # Duplicate and conjugate complex magnitudes to account for negative frequencies
        amp2_2 = np.concatenate((amp2, np.conjugate(amp2)), axis=0)

        # Outer product of both complex amplitude vectors to calculte all harmonic combinations
        amp_full = np.outer(amp1_1, amp2_2).ravel("F")[I0a] / 2

    # Sum all contributions which have the same index
    if amp_full.dtype == complex:
        amp = np.bincount(I1, weights=amp_full.real) + 1j * np.bincount(
            I1, weights=amp_full.imag
        )
    else:
        amp = np.bincount(I1, weights=amp_full)

    # Divide by two constant component
    if I2.size > 0:
        amp[I2] /= 2

    return amp


def get_sum_indices(freqs1, freqs2, tol_freq):
    """Compute frequency array and return indices to perform DataFreq sum

    Parameters
    ----------
    freqs1 : ndarray
        frequency array of first DataFreq
    freqs2 : ndarray
        frequency array of second DataFreq
    tol_freq: Float
        Absolute tolerance value to filter harmonic orders by their frequency value

    Returns
    -------
    freqs_un : ndarray
        frequency array of summed DataFreq
    I0b: ndarray
        array on which amplitudes are accumulated
    """

    # Compute the frequency array containing all combinations
    freqs = np.concatenate((freqs1, freqs2), axis=0)

    # Get unique orders
    freqs_un, I0b = unique_tol(
        freqs,
        return_inverse=True,
        return_index=False,
        axis=0,
        is_abs_tol=True,
        tol=tol_freq,
    )

    return freqs_un, I0b


def get_sum_amplitudes(amp1, amp2, I0b):
    """Calculate summed amplitudes of both input amplitudes arrays

    Parameters
    ----------
    amp1 : ndarray
        First amplitude array
    amp2 : ndarray
        Second amplitude array
    I0b: ndarray
        array on which amplitudes are accumulated

    Returns
    -------
    amp: ndarray
        array of harmonics amplitude
    """

    # Concatenate both amplitude arrays
    amp_full = np.concatenate((amp1, amp2), axis=0)

    # Sum all contributions which have the same orders and wavenumber
    if amp_full.dtype == complex:
        amp = np.bincount(I0b, weights=amp_full.real) + 1j * np.bincount(
            I0b, weights=amp_full.imag
        )
    else:
        amp = np.bincount(I0b, weights=amp_full)

    return amp
