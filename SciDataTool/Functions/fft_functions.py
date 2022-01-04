from numpy import (
    array,
    pi,
    exp,
    ceil,
    isin,
    take,
    insert,
    delete,
    allclose,
    real,
    linspace,
    where,
    isclose,
    around,
)
from numpy.fft import (
    fftshift,
    ifftshift,
    rfftn,
    irfftn,
    fftn,
    ifftn,
)


from SciDataTool.Functions.nudft_functions import is_uniform, nudftn, inudftn


def comp_fft_freqs(time, is_time, is_real):
    """Computes the frequency/wavenumber vector from the time/space vector
    Parameters
    ----------
    time: array
        Time or space vector
    is_time: bool
        Boolean indicating if we input time or space
    Returns
    -------
    Frequency/wavenumber vector
    """
    N_tot = time.size  # Number of samples
    if N_tot == 1:
        freqs = [0]
    else:
        # zero-padding
        # N_tot = int(2**(log(N_tot)//log(2)+1))
        timestep = float(time[1] - time[0])  # Sample step
        fsampt = 1.0 / timestep  # Sample frequency
        freqscale = N_tot / fsampt
        freqs = [i - int(N_tot / 2) for i in range(int(N_tot))]
        if is_real and is_time:
            # freqs = rfftfreq(N_tot, 1/(N_tot*fsampt))
            freqs = [i for i in range(int(N_tot / 2) + 1)]
            # freqs.append(-freqs[0])
        if is_time:
            freqs = [i / freqscale for i in freqs]
    return freqs


def comp_fft_time(freqs, is_angle, is_real):
    """Computes the time/space vector from the frequency/wavenumber vector
    Parameters
    ----------
    freqs: array
        Frequency or wavenumber vector
    is_angle: bool
        Boolean indicating if we output angle or time
    Returns
    -------
    Time/space vector
    """
    if freqs.size == 1:
        time = array([0])
    else:
        if is_real and not is_angle:
            N_tot = 2 * (len(freqs) - 1)  # Number of samples
            fs = freqs[-1] / (N_tot)
        else:
            N_tot = len(freqs)  # Number of samples
            fs = freqs[-1] / (N_tot - 2)
        tf = 1 / (fs * 2)
        time = linspace(0, tf, N_tot, endpoint=False)
        # fsampt = freqs[-1] * 2.0
        # timestep = 1.0 / fsampt
        if is_angle:
            time *= 2.0 * pi
            # timestep *= 2.0 * pi
        # time = [0 + i * timestep for i in range(N_tot)]
    return time.tolist()


def comp_nthoctave_axis(noct, freqmin, freqmax):
    """Computes the frequency vector between freqmin and freqmax for the 1/n octave
    Parameters
    ----------
    noct: int
        kind of octave band (1/3, etc)
    freqmin: float
        minimum frequency
    freqmax: float
        maximum frequency
    Returns
    -------
    Frequency vector
    """
    if noct == 3:
        table = [
            12.5,
            16,
            20,
            25,
            31.5,
            40,
            50,
            63,
            80,
            100,
            125,
            160,
            200,
            250,
            315,
            400,
            500,
            630,
            800,
            1000,
            1250,
            1600,
            2000,
            2500,
            3150,
            4000,
            5000,
            6300,
            8000,
            10000,
            12500,
            16000,
            20000,
        ]
        f_oct = [f for f in table if (f >= freqmin and f <= freqmax)]
    elif noct == 1:
        table = [
            16,
            31.5,
            63,
            125,
            250,
            500,
            1000,
            2000,
            4000,
            8000,
            16000,
        ]
        f_oct = [f for f in table if (f >= freqmin and f <= freqmax)]
    else:
        f0 = 1000
        f_oct = [f0]
        i = 1
        while f_oct[-1] <= freqmax:
            f = f0 * 2.0 ** (i / noct)
            f_oct.append(0.5 * ceil(2.0 * f))
            i = i + 1
        f_oct = f_oct[:-1]
        i = -1
        while f_oct[0] > freqmin:
            f = f0 * 2.0 ** (i / noct)
            f_oct = [0.5 * ceil(2.0 * f)] + f_oct
            i = i - 1
        f_oct = f_oct[1:]
    return f_oct


# def _comp_fft(values, is_positive=False):
#     """Computes the Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the field
#     Returns
#     -------
#     Complex Fourier Transform
#     """
#     values_FT = fft(values)
#     if is_positive:
#         if iscomplex(values).any():
#             print("WARNING: keeping only positive harmonics from complex raw data")
#         values_FT[0] *= 0.5
#         values_FT = 2.0 * fftshift(values_FT) / len(values)
#         if len(values) % 2 == 0:
#             values_FT = append(values_FT, conjugate(values_FT[0]))
#     else:
#         values_FT = fftshift(values_FT) / len(values)
#     return values_FT


def comp_fftn(values, axes_list, is_real=True):
    """Computes the Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Complex Fourier Transform
    """

    axes = []
    axes_dict_non_uniform = dict()
    shape = []
    is_onereal = False
    is_twice = False
    axis_names = [axis.name for axis in axes_list]

    # Check if one or several axes is non-uniform
    is_non_uniform = False
    for axis in axes_list:
        if axis.transform == "fft":
            if axis.corr_values is not None and len(axis.corr_values) > 1:  # Timesteps
                if not is_uniform(axis.corr_values):
                    is_non_uniform = True
                    axes_dict_non_uniform[axis.index] = [
                        axis.corr_values,
                        axis.input_data,
                    ]
                    # Keep only interpolation data
                    axis.values = axis.input_data
                    axis.input_data = None
                    continue
            if axis.input_data is not None:
                if not isin(
                    around(axis.input_data, decimals=5), around(axis.values, decimals=5)
                ).all():
                    is_non_uniform = True
                    # Convert wavenumbers to frequencies if needed
                    frequencies = (
                        axis.input_data
                        if axis.name == "freqs"
                        else axis.input_data / (2 * pi)
                    )
                    axes_dict_non_uniform[axis.index] = [
                        axis.corr_values,
                        frequencies,
                    ]
                    # Keep only interpolation data
                    axis.values = axis.input_data
                    axis.input_data = None

    # Apply DFT on non-uniform axes
    if is_non_uniform:
        values = nudftn(values, axes_dict=axes_dict_non_uniform)

    # Find other fft axes
    for axis in axes_list:
        if axis.index not in axes_dict_non_uniform:
            if axis.transform == "fft":
                if is_real and axis.name == "freqs":
                    axes.append(axis.index)
                    shape.append(values.shape[axis.index])
                    is_onereal = True
                elif (
                    is_real
                    and axis.name == "wavenumber"
                    and "freqs" not in axis_names
                    and min(axis.values) >= 0
                ):
                    axes.append(axis.index)
                    shape.append(values.shape[axis.index])
                    is_twice = True
                else:
                    axes = [axis.index] + axes
                    shape = [values.shape[axis.index]] + shape
    if axes != []:
        size = array(shape).prod()
        if is_onereal:
            values_FT = rfftn(values, axes=axes)
            # Do not multiply constant component by 2 (f=0)
            if axes_list[axes[-1]].corr_values is not None:
                freqs = axes_list[axes[-1]].corr_values
            else:
                freqs = axes_list[axes[-1]].values
            if freqs[0] == 0:
                slice_0 = take(values_FT, 0, axis=axes[-1])
                slice_0 *= 0.5
                if is_twice:
                    slice_0 *= 0.5
                other_values = delete(values_FT, 0, axis=axes[-1])
                values_FT = insert(other_values, 0, slice_0, axis=axes[-1])
            values_FT2 = 2.0 * fftshift(values_FT, axes=axes[:-1]) / size
            if is_twice:
                values_FT2 *= 2.0
        elif is_twice:
            values_FT = fftn(values, axes=axes)
            slice_0 = take(values_FT, 0, axis=axes[-1])
            slice_0 *= 0.5
            other_values = delete(values_FT, 0, axis=axes[-1])
            values_FT = insert(other_values, 0, slice_0, axis=axes[-1])
            values_FT2 = 2.0 * fftshift(values_FT, axes=axes) / size
        else:
            values_FT = fftn(values, axes=axes)
            values_FT2 = fftshift(values_FT, axes=axes) / size
    else:
        values_FT2 = values
    return values_FT2


# def _comp_ifft(values, is_positive=False):
#     """Computes the Inverse Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the FT
#     Returns
#     -------
#     IFT
#     """

#     if is_positive:
#         values[0] *= 2
#         values = concatenate((flip(conjugate(values))[:-1], values))[:-1]
#         values = values / 2
#         values = ifftshift(values) * len(values)
#     else:
#         values = ifftshift(values) * len(values)
#     values_IFT = ifft(values)
#     return values_IFT


def comp_ifftn(values, axes_list, is_real=True):
    """Computes the Inverse Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the FT
    Returns
    -------
    IFT
    """

    axes = []
    shape = []
    is_onereal = False
    is_half = False
    axis_names = [axis.name for axis in axes_list]
    # Check if one or several axes is non-uniform
    axes_dict_non_uniform = {}

    for axis in axes_list:
        if axis.transform == "ifft":
            if axis.input_data is not None and len(axis.input_data) > 1:
                if not is_uniform(axis.input_data):
                    # Data is at least non uniform in "space"
                    axes_dict_non_uniform[axis.index] = [
                        axis.input_data,
                        axis.corr_values,
                    ]
                    # Keep only interpolation data
                    axis.values = axis.input_data
                    axis.input_data = None
                else:
                    # Compare frequencies of interest with fft frequencies
                    freqs = comp_fft_freqs(
                        axis.input_data, axis.name == "time", is_real
                    )
                    if len(axis.corr_values) > 1:
                        if (
                            not is_uniform(axis.corr_values)
                            or (
                                len(freqs) != len(axis.corr_values)
                                and not isin(freqs, axis.corr_values).all()
                            )
                            or len(freqs) == len(axis.corr_values)
                            and not allclose(
                                freqs,
                                axis.corr_values,
                                rtol=1e-5,
                                atol=1e-8,
                                equal_nan=False,
                            )
                        ):
                            # Data is at least non uniform in "frequency"
                            # Convert wavenumbers to frequencies if needed
                            frequencies = (
                                axis.corr_values
                                if axis.name == "time"
                                else axis.corr_values / (2 * pi)
                            )
                            axes_dict_non_uniform[axis.index] = [
                                axis.input_data,
                                frequencies,
                            ]
                            # Keep only interpolation data
                            axis.values = axis.input_data
                            axis.input_data = None

    # Compute non uniform inverse Fourier Transform for axes
    if axes_dict_non_uniform:
        values = inudftn(values, axes_dict=axes_dict_non_uniform)

    for axis in axes_list:
        # Exclude non uniform axes
        if axis.index in axes_dict_non_uniform:
            continue
        if axis.transform == "ifft":
            if is_real and axis.name == "time":
                axes.append(axis.index)
                shape.append(2 * (values.shape[axis.index] - 1))
                is_onereal = True
            elif is_real and axis.name == "angle" and "time" not in axis_names:
                axes.append(axis.index)
                shape.append(values.shape[axis.index])
                is_half = True
            else:
                axes = [axis.index] + axes
                shape = [values.shape[axis.index]] + shape
    if axes:  # Check if ifftn has to be called
        size = array(shape).prod()
        if is_onereal:
            values = values * size / 2
            if is_half:
                values *= 0.5
            values_shift = ifftshift(values, axes=axes[:-1])
            slice_0 = take(values_shift, 0, axis=axes[-1])
            slice_0 *= 2
            if is_half:
                slice_0 *= 2
            other_values = delete(values_shift, 0, axis=axes[-1])
            values = insert(other_values, 0, slice_0, axis=axes[-1])
            values_IFT = irfftn(values, axes=axes)
        elif is_half:
            values = values * size / 2
            values_shift = ifftshift(values, axes=axes[:-1])
            slice_0 = take(values_shift, 0, axis=axes[-1])
            slice_0 *= 2
            other_values = delete(values_shift, 0, axis=axes[-1])
            values = insert(other_values, 0, slice_0, axis=axes[-1])
            values_IFT = ifftn(values, axes=axes)
        else:
            values_shift = ifftshift(values, axes=axes) * size
            values_IFT = ifftn(values_shift, axes=axes)
    else:
        values_IFT = values
    if is_real:
        values_IFT = real(values_IFT)
    return values_IFT


# def comp_magnitude(values):
#     """Computes the magnitude of the Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the field
#     Returns
#     -------
#     Magnitude of the Fourier Transform
#     """
#     return np_abs(_comp_fft(values))


#    return np_abs(comp_stft_average(values))
# def comp_phase(values):
#     """Computes the phase of the Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the field
#     Returns
#     -------
#     Phase of the Fourier Transform
#     """
#     return np_angle(_comp_fft(values))


# def comp_stft_average(values):
#     """Computes the average of the Short-Time Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the field
#     Returns
#     -------
#     Average of the Short-Time Fourier Transform
#     """
#     # To do
#     nperseg = 3200
#     noverlap = int(nperseg * 0.75)
#     f, t, Zxx = stft(
#         values, fs=48000, window="hann", nperseg=nperseg, noverlap=noverlap
#     )
#     window_size = nperseg / len(values)
#     values = mean(Zxx, axis=1) / (0.5)
#     #    values = 2.0 * mean(Zxx, axis=1)
#     print(values.shape)
#     return f, np_abs(values)


# def comp_fft_average(values):
#     """Computes the average of the Short-Time Fourier Transform
#     Parameters
#     ----------
#     values: ndarray
#         ndarray of the field
#     Returns
#     -------
#     Average of the Short-Time Fourier Transform
#     """
#     # To do
#     nperseg = 3200
#     noverlap = int(nperseg * 0.75)
#     step = nperseg - noverlap
#     N_tot = len(values)
#     nwindows = int(N_tot / (2.0 * step))
#     values_fft = zeros(nperseg, dtype="complex128")
#     for i in range(nwindows):
#         values_fft += _comp_fft(
#             values[i * step : nperseg + i * step] * hanning(nperseg)
#         )
#     values = values_fft[int(nperseg / 2) :] / nwindows
#     f = linspace(0, int(N_tot / 2), int(nperseg / 2))
#     return f, np_abs(values)


def rect_window(f, M, dt):
    W = where(
        isclose(f, 0),
        (1 - exp(-1j * 2 * pi * dt * f * (M))) / (1 - exp(-1j * 2 * pi * dt * f)) / M,
        1,
    )
    return W


# M = 200
# tf = 1
# timec = linspace(0,tf*(1-1/M),M)
# dt = timec[1] - timec[0]
# A0 = 2
# freq0 = 10.0
# phi0=0
# y = A0*cos(2*pi*freq0*timec+phi0)
# freqs = comp_fft_freqs(timec, is_time=True, is_positive=False)
# y_FT = comp_fft(y)
# fig = plt.figure(constrained_layout=True, figsize=(20, 10))
# plt.plot(freqs,np_abs(y_FT))
# freqs_th = [-freq0, freq0]
# If = [0 for i in range(len(freqs_th))]
# for i in range(len(freqs_th)):
#     If[i] = int(argmin(abs([f-freqs_th[i] for f in freqs])))
# freqs = [freqs[i] for i in If]
# (xfreqs2, xfreqs1) = meshgrid(freqs_th,freqs)
# Wmat = rect_window(xfreqs1 - xfreqs2, M, dt)
# y_corr = linalg.solve(Wmat, y_FT[If])
# print(y_corr)
# plt.plot(freqs_th,np_abs(y_corr))
