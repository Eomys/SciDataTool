# -*- coding: utf-8 -*-
from numpy import prod, mean, hanning, linspace, argmin, abs, where, isclose
from numpy.fft import fft, rfftn, ifftn, fftn, fftshift, rfft2
from scipy.fftpack import ifft, ifftshift
from numpy import (
    pi,
    zeros,
    cos,
    exp,
    log,
    meshgrid,
    array,
    abs as np_abs,
    angle as np_angle,
)
from numpy import linalg, transpose, dot
from scipy.signal import stft, spectrogram
import matplotlib.pyplot as plt


def comp_fft_freqs(time, is_time, is_positive):
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
        if is_positive:
            freqs = [i for i in range(int(N_tot / 2) + 1)]
        else:
            freqs = [i - int(N_tot / 2) for i in range(int(N_tot))]
        if is_time:
            freqs = [i / freqscale for i in freqs]
    return freqs


def comp_fft_time(freqs, is_angle):
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
        time = [0]
    else:
        N_tot = len(freqs)  # Number of samples
        fsampt = freqs[-1] * 2.0
        timestep = 1.0 / fsampt
        if is_angle:
            timestep *= 2.0 * pi
        time = [0 + i * timestep for i in range(N_tot)]
    return time


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
            10,
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
    else:
        f0 = 1000
        f_oct = [f0]
        i = 1
        while f_oct[-1] <= freqmax:
            f_oct.append(f0 * 2.0 ** (i / noct))
            i = i + 1
        f_oct = f_oct[:-2]
        i = -1
        while f_oct[0] > freqmin:
            f_oct.insert(0, f0 * 2.0 ** (i / noct))
            i = i - 1
        f_oct = f_oct[1:]
    return f_oct


def comp_fft(values, axes=None):
    """Computes the Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Complex Fourier Transform
    """
    values_shape = values.shape
    values_FT = fftn(values)
    values_FT[tuple([0 for N in values_shape])] *= 0.5
    values_FT = 2.0 * fftshift(values_FT) / float(prod([N for N in values_shape]))
    return values_FT


def comp_ifft(values):
    """Computes the inverse Fourier Transform
    Parameters
    ----------
    values: ndarray
        complex Fourier transform
    Returns
    -------
    ndarray of the field
    """

    values_shape = values.shape
    values[tuple([N // 2 for N in values_shape])] *= 2
    values = ifftshift(values * float(prod([N for N in values_shape])) / 2)
    values = ifftn(values)
    return values.real


def comp_rfft(values):
    """Computes the Fourier Transform restricted to positive freqs
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Complex Fourier Transform restricted to positive freqs
    """
    values_shape = values.shape
    values_FT = rfft2(values)
    values_FT = values_FT / float(prod(values_shape))
    return values_FT


def comp_magnitude(values):
    """Computes the magnitude of the Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Magnitude of the Fourier Transform
    """
    return np_abs(comp_fft(values))


#    return np_abs(comp_stft_average(values))
def comp_phase(values):
    """Computes the phase of the Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Phase of the Fourier Transform
    """
    return np_angle(comp_fft(values))


def comp_stft_average(values):
    """Computes the average of the Short-Time Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Average of the Short-Time Fourier Transform
    """
    # To do
    nperseg = 3200
    noverlap = int(nperseg * 0.75)
    f, t, Zxx = stft(
        values, fs=48000, window="hann", nperseg=nperseg, noverlap=noverlap
    )
    window_size = nperseg / len(values)
    values = mean(Zxx, axis=1) / (0.5)
    #    values = 2.0 * mean(Zxx, axis=1)
    print(values.shape)
    return f, np_abs(values)


def comp_fft_average(values):
    """Computes the average of the Short-Time Fourier Transform
    Parameters
    ----------
    values: ndarray
        ndarray of the field
    Returns
    -------
    Average of the Short-Time Fourier Transform
    """
    # To do
    nperseg = 3200
    noverlap = int(nperseg * 0.75)
    step = nperseg - noverlap
    N_tot = len(values)
    nwindows = int(N_tot / (2.0 * step))
    values_fft = zeros(nperseg, dtype="complex128")
    for i in range(nwindows):
        values_fft += comp_fft(values[i * step : nperseg + i * step] * hanning(nperseg))
    values = values_fft[int(nperseg / 2) :] / nwindows
    f = linspace(0, int(N_tot / 2), int(nperseg / 2))
    return f, np_abs(values)


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
