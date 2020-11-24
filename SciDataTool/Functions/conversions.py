# -*- coding: utf-8 -*-
from SciDataTool.Functions import UnitError
from SciDataTool.Functions.fft_functions import comp_fft_freqs, comp_fft_time
from numpy import (
    pi,
    log10,
    sqrt,
    square,
    column_stack,
    exp,
    real,
    imag,
    cos,
    sin,
    ndarray,
    abs as np_abs,
    angle as np_angle,
)

# List of the unit symbols, their normalizing value and their dimensions "MLTTempAngleCurrent"
unit_symbols = [
    ("dimless", 1.0, (0, 0, 0, 0, 0, 0)),  # dimensionless
    ("degC", 1.0, (0, 0, 0, 1, 0, 0)),  # degree Celsius
    ("rad", 1.0, (0, 0, 0, 0, 1, 0)),  # radians
    ("°", pi / 180, (0, 0, 0, 0, 1, 0)),  # degree (angle)
    ("rpm", 2 * pi / 60, (0, 0, -1, 0, 1, 0)),  # rotation per minute
    ("min", 60.0, (0, 0, 1, 0, 0, 0)),  # minute
    ("Ohm", 1.0, (1, 2, -3, 0, 0, -2)),  # Ohm
    ("At", 1.0, (0, 0, 0, 0, 0, 1)),  # Ampere-tour
    ("Wb", 1.0, (1, 2, -2, 0, 0, -1)),  # Weber
    ("Mx", 1.0e-8, (1, 2, -2, 0, 0, -1)),  # Maxwell
    ("Hz", 1.0, (0, 0, -1, 0, 0, 0)),  # Herz
    ("Pa", 1.0, (1, -1, -2, 0, 0, 0)),  # Pascal
    ("g", 1.0e-3, (0, 1, 0, 0, 0, 0)),  # gram
    ("s", 1.0, (0, 0, 1, 0, 0, 0)),  # second
    ("h", 3600.0, (0, 0, 1, 0, 0, 0)),  # hour
    #    ("K",       1.0, (0,0,0,1,0,0)),   # Kelvin
    ("A", 1.0, (0, 0, 0, 0, 0, 1)),  # Ampere
    ("J", 1.0, (1, 2, -2, 0, 0, 0)),  # Joule
    ("W", 1.0, (1, 2, -3, 0, 0, 0)),  # Watt
    ("N", 1.0, (1, 1, -2, 0, 0, 0)),  # Newton
    ("C", 1.0, (0, 0, 1, 0, 0, 1)),  # Coulomb
    ("T", 1.0, (1, 0, -2, 0, 0, -1)),  # Tesla
    ("G", 1.0e-4, (1, 0, -2, 0, 0, -1)),  # Gauss
    ("V", 1.0, (1, 2, -3, 0, 0, -1)),  # Volt
    ("F", 1.0, (-1, -2, 4, 0, 0, 2)),  # Farrad
    ("H", 1.0, (1, -2, -2, 0, 0, -2)),  # Henry
    ("m", 1.0, (1, 0, 0, 0, 0, 0)),  # meter
]
# Dictionnary of the prefixes and their values
unit_prefixes = {
    "Y": 1e24,
    "Z": 1e21,
    "E": 1e18,
    "P": 1e15,
    "T": 1e12,
    "G": 1e9,
    "M": 1e6,
    "k": 1e3,
    "h": 1e2,
    "da": 1e1,
    "": 1.0,
    "d": 1e-1,
    "c": 1e-2,
    "m": 1e-3,
    "µ": 1e-6,  # ('MICRO SIGN' U+00B5)
    "u": 1e-6,
    "μ": 1e-6,  # ('GREEK SMALL LETTER MU' U+03BC)
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
    "a": 1e-18,
    "z": 1e-21,
    "y": 1e-24,
}


def get_dim_prefix(unit_str):
    if unit_str == "":
        unit_str = "dimless"
    p = 1  # power of the unit
    dim = None
    for key in unit_symbols:
        if key[0] in unit_str:
            if unit_str.rsplit(key[0], 1)[1].isdigit():
                p = int(unit_str.rsplit(key[0], 1)[1])
            dim = [p * d for d in key[2]]
            prefix_str = unit_str.rsplit(key[0], 1)[0]
            if prefix_str in unit_prefixes.keys():
                prefix = (unit_prefixes.get(prefix_str) * key[1]) ** p
            else:
                raise UnitError("ERROR: Prefix " + prefix_str + " unknown")
            break
    if not dim:
        raise UnitError("ERROR: Unit " + unit_str + " unknown")
    return (dim, prefix)


def convert(values, unit1, unit2):
    """Converts values from unit1 to unit2
    Parameters
    ----------
    values: ndarray
        Values of the field to convert
    unit1: str
        start unit
    unit2: str
        final unit
    Returns
    -------
    ndarray of the converted field
    """
    unit1_save = unit1
    unit2_save = unit2
    # Format the strings
    unit1 = unit1.replace("*", "").replace(" ", "").replace("^", "")
    unit2 = unit2.replace("*", "").replace(" ", "").replace("^", "")
    # Unit1 parsing
    if "/" in unit1:
        dim1_denom, prefix1_denom = get_dim_prefix(unit1.split("/")[1])
        unit1 = unit1.split("/")[0]
    else:
        dim1_denom = [0, 0, 0, 0, 0, 0]
        prefix1_denom = 1.0
    dim1_num, prefix1_num = get_dim_prefix(unit1)
    # Unit2 parsing
    if "/" in unit2:
        dim2_denom, prefix2_denom = get_dim_prefix(unit2.split("/")[1])
        unit2 = unit2.split("/")[0]
    else:
        dim2_denom = [0, 0, 0, 0, 0, 0]
        prefix2_denom = 1.0
    dim2_num, prefix2_num = get_dim_prefix(unit2)
    # Check compatibility
    dim1 = [i - j for i, j in zip(dim1_num, dim1_denom)]
    dim2 = [i - j for i, j in zip(dim2_num, dim2_denom)]
    if dim1 != dim2:
        raise UnitError(
            "ERROR: Units " + unit1_save + " and " + unit2_save + " do not match"
        )
    else:
        return values * (prefix1_num / prefix1_denom) / (prefix2_num / prefix2_denom)


def to_dB(values, unit, ref_value=1.0):
    """Converts values into dB normalized with ref_value

    Parameters
    ----------
    values: ndarray
        Values of the field to convert
    unit: str
        Unit
    ref_value: float
        Reference value
    Returns
    -------
    ndarray of the converted field
    """
    if isinstance(values, ndarray):
        values[values < ref_value] = ref_value
    else:
        if values < ref_value:
            values = ref_value
    try:
        convert(values, unit, "W")
        return 10.0 * log10(values / ref_value)
    except:
        return 20.0 * log10(values / ref_value)


def to_dBA(values, freqs, unit, ref_value=1.0):
    """Converts values into dBA (requires frequency vector)

    Parameters
    ----------
    values: array
        Values of the field to convert (must be 1D)
    freqs: array
        Frequency vector
    unit: str
        Unit
    ref_value: float
        Reference value
    Returns
    -------
    ndarray of the converted field
    """
    values = to_dB(values, unit, ref_value)
    return dB_to_dBA(values, freqs)


def dB_to_dBA(values, freqs):
    """Converts values from dB into dBA (requires frequency vector)

    Parameters
    ----------
    values: array
        Values of the field to convert (must be 1D)
    freqs: array
        Frequency vector
    Returns
    -------
    ndarray of the converted field
    """
    freq2 = square(freqs)
    RA = (
        12200.0 ** 2
        * freq2 ** 2
        / (
            (freq2 + 20.6 ** 2)
            * sqrt((freq2 + 107.7 ** 2) * (freq2 + 737.0 ** 2))
            * (freq2 + 12200.0 ** 2)
        )
    )
    Aweight = 2.0 + 20.0 * log10(RA)
    Aweight[RA == 0] = -100  # replacing -Inf by -100 dB
    Aweight[
        values <= 0
    ] = 0  # avoiding to increase dB in dBA at frequencies where noise is already null
    try:
        values += Aweight
        return values
    except:
        raise UnitError("ERROR: dBA conversion only available for 1D fft")


def xyz_to_rphiz(values):
    """Converts axis values from cartesian coordinates into cylindrical coordinates

    Parameters
    ----------
    values: array
        Values of the axis to convert (Nx3)
    Returns
    -------
    ndarray of the axis (Nx3)
    """

    x = values[:, 0]
    y = values[:, 1]
    z = values[:, 2]

    affixe = x + 1j * y
    r = np_abs(affixe)
    phi = (np_angle(affixe) + 2 * pi) % (2 * pi)

    return column_stack((r, phi, z))


def rphiz_to_xyz(values):
    """Converts axis values from cylindrical coordinates into cartesian coordinates

    Parameters
    ----------
    values: array
        Values of the axis to convert (Nx3)
    Returns
    -------
    ndarray of the axis (Nx3)
    """

    r = values[:, 0]
    phi = values[:, 1]
    z = values[:, 2]

    affixe = r * exp(1j * phi)
    x = real(affixe)
    y = imag(affixe)

    return column_stack((x, y, z))


def xyz_to_rphiz_field(values, phi):
    """Converts field values from cartesian coordinates into cylindrical coordinates

    Parameters
    ----------
    values: array
        Values of the field to convert (Nx3)
    phi: array
        Values of the angle axis (N)
    Returns
    -------
    ndarray of the field (Nx3)
    """

    field_x = values[:, 0]
    field_y = values[:, 1]
    field_z = values[:, 2]

    cos_phi = cos(phi)
    sin_phi = sin(phi)

    field_r = cos_phi * field_x + sin_phi * field_y
    field_phi = -sin_phi * field_x + cos_phi * field_y

    return column_stack((field_r, field_phi, field_z))


def rphiz_to_xyz_field(values, phi):
    """Converts field values from cylindrical coordinates into cartesian coordinates

    Parameters
    ----------
    values: array
        Values of the field to convert (Nx3)
    phi: array
        Values of the angle axis (N)
    Returns
    -------
    ndarray of the field (Nx3)
    """

    field_r = values[:, 0]
    field_phi = values[:, 1]
    field_z = values[:, 2]

    cos_phi = cos(phi)
    sin_phi = sin(phi)

    field_x = cos_phi * field_r - sin_phi * field_phi
    field_y = sin_phi * field_r + cos_phi * field_phi

    return column_stack((field_x, field_y, field_z))


def time_to_freqs(values):
    is_time = True
    is_positive = False
    return comp_fft_freqs(values, is_time, is_positive)


def freqs_to_time(values):
    is_angle = False
    return comp_fft_time(values, is_angle)


def angle_to_wavenumber(values):
    is_time = False
    is_positive = False
    return comp_fft_freqs(values, is_time, is_positive)


def wavenumber_to_angle(values):
    is_angle = True
    return comp_fft_time(values, is_angle)


def xy_to_rphi(x, y):
    affixe = x + 1j * y
    r = np_abs(affixe)
    phi = (np_angle(affixe) + 2 * pi) % (2 * pi)

    return (r, phi)


def rphi_to_xy(r, phi):
    affixe = r * exp(1j * phi)
    x = real(affixe)
    y = imag(affixe)

    return (x, y)


def cart2pol(field_x, field_y, phi):
    cos_phi = cos(phi)
    sin_phi = sin(phi)

    field_r = cos_phi * field_x + sin_phi * field_y
    field_phi = -sin_phi * field_x + cos_phi * field_y

    return (field_r, field_phi)


def pol2cart(field_r, field_phi, phi):
    cos_phi = cos(phi)
    sin_phi = sin(phi)

    field_x = cos_phi * field_r - sin_phi * field_phi
    field_y = sin_phi * field_r + cos_phi * field_phi

    return (field_x, field_y)
