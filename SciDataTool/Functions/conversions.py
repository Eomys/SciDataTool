from SciDataTool.Functions import UnitError
from SciDataTool.Functions.fft_functions import (
    comp_fft_freqs,
    comp_fft_time,
    comp_nthoctave_axis,
)
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
    nan,
    isnan,
    abs as np_abs,
    sum as np_sum,
    angle as np_angle,
    where,
    argwhere,
    array,
    take,
    zeros,
    floor,
    ones,
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
                raise UnitError("Prefix " + prefix_str + " unknown")
            break
    if not dim:
        raise UnitError("Unit " + unit_str + " unknown")
    return (dim, prefix)


def get_unit_derivate(unit_str, axis_unit):
    unit_str = unit_str.replace("*", "").replace(" ", "").replace("^", "")
    if axis_unit == "Hz":
        axis_unit = "s"
    if axis_unit == "rad":
        axis_unit = "m"
    p = 0
    if "/" in unit_str:
        unit_num = unit_str.split("/")[0]
        unit_denom = unit_str.split("/")[1]
    else:
        unit_num = unit_str
        unit_denom = ""
    if axis_unit in unit_num:
        p = 1
        if unit_num.rsplit(axis_unit, 1)[1].isdigit():
            p = int(unit_num.rsplit(axis_unit, 1)[1])
        p_new = p - 1
        # Case axis_unit must be withdrawn
        if p_new == 0:
            unit_str = unit_str.replace(axis_unit, "")
        elif p_new == 1:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit)
        else:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit + str(p_new))
    elif axis_unit in unit_denom:
        p = 1
        if unit_denom.rsplit(axis_unit, 1)[1].isdigit():
            p = int(unit_denom.rsplit(axis_unit, 1)[1])
        p_new = p + 1
        # Case p was 1
        if p_new == 2:
            unit_str = unit_str.replace(axis_unit, axis_unit + "2")
        elif p_new == 1:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit)
        else:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit + str(p_new))
    else:
        # Case axis_unit was not in unit_str
        if unit_denom != "":
            unit_str += axis_unit
        else:
            unit_str += "/" + axis_unit
    return unit_str


def get_unit_integrate(unit_str, axis_unit):
    unit_str = unit_str.replace("*", "").replace(" ", "").replace("^", "")
    if axis_unit == "Hz":
        axis_unit = "s"
    if axis_unit == "rad":
        axis_unit = "m"
    p = 0
    if "/" in unit_str:
        unit_num = unit_str.split("/")[0]
        unit_denom = unit_str.split("/")[1]
    else:
        unit_num = unit_str
        unit_denom = ""
    if axis_unit in unit_num:
        p = 1
        if unit_num.rsplit(axis_unit, 1)[1].isdigit():
            p = int(unit_num.rsplit(axis_unit, 1)[1])
        p_new = p + 1
        # Case p was 1
        if p_new == 2:
            unit_str = unit_str.replace(axis_unit, axis_unit + "2")
        elif p_new == 1:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit)
        else:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit + str(p_new))
    elif axis_unit in unit_denom:
        p = 1
        if unit_denom.rsplit(axis_unit, 1)[1].isdigit():
            p = int(unit_denom.rsplit(axis_unit, 1)[1])
        p_new = p - 1
        # Case axis_unit must be withdrawn
        if p_new == 0:
            unit_denom = unit_denom.replace(axis_unit, "")
            if unit_denom == "":
                unit_str = unit_num
            else:
                unit_str = unit_str.replace(axis_unit, "")
        elif p_new == 1:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit)
        else:
            unit_str = unit_str.replace(axis_unit + str(p), axis_unit + str(p_new))
    else:
        # Case axis_unit was not in unit_str
        if unit_denom != "":
            unit_str = unit_num + axis_unit + "/" + unit_denom
        else:
            unit_str += axis_unit
    return unit_str


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
    # Critical band to frequency conversion (for acoustic loudness)
    # Traunmüller, H. (1990). "Analytical expressions for the tonotopic sensory scale".
    # The Journal of the Acoustical Society of America. 88: 97. doi:10.1121/1.399849
    if unit1 == "Bark" and unit2 == "Hz":
        return 1960 * (values + 0.53) / (26.28 - values)
    elif unit1 == "Hz" and unit2 == "Bark":
        return (26.81 * values / (1960 + values)) - 0.53
    elif unit1 == "dimless" and unit2 == "":
        return values
    elif unit1 == "" and unit2 == "dimless":
        return values
    # Generic conversion
    else:
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
                "Units " + unit1_save + " and " + unit2_save + " do not match"
            )
        else:
            return (
                values * (prefix1_num / prefix1_denom) / (prefix2_num / prefix2_denom)
            )


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
    if ref_value != 1:
        if isinstance(values, ndarray):
            values[values < ref_value] = ref_value
        else:
            if values < ref_value:
                values = ref_value
    mask = values != 0
    try:
        convert(values, unit, "W")
        values_dB = 10.0 * where(mask, log10(values / ref_value, where=mask), 0)
    except Exception:
        values_dB = 20.0 * where(mask, log10(values / ref_value, where=mask), 0)
    return values_dB


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


def dB_to_dBA(values, freqs, noct=None):
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
    if noct is not None:
        freqs_ref = [
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
        Aweight = [
            -63.4,
            -56.7,
            -50.5,
            -44.7,
            -39.4,
            -34.6,
            -30.2,
            -26.2,
            -22.5,
            -19.1,
            -16.1,
            -13.4,
            -10.9,
            -8.6,
            -6.6,
            -4.8,
            -3.2,
            -1.9,
            -0.8,
            0,
            0.6,
            1,
            1.2,
            1.3,
            1.2,
            1,
            0.5,
            -0.1,
            -1.1,
            -2.5,
            -4.3,
            -6.6,
            -9.3,
        ]
        mask = argwhere(freqs in freqs_ref)
        Aweight = take(Aweight, mask)
    else:
        freq2 = square(freqs)
        freq2[freq2 == 0] = nan
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
        Aweight[isnan(Aweight)] = -100  # replacing NaN by -100 dB
        values_dBA = values + Aweight
        return values_dBA


def to_noct(values, freqs, noct=3):
    """Converts values into 1/nth octave band (requires frequency vector)

    Parameters
    ----------
    values: array
        Values of the field to convert (must be 1D)
    freqs: array
        Frequency vector
    noct: int
        Requested octave band
    Returns
    -------
    ndarray of the converted field
    """
    # Compute the 1/n octave axis
    f_oct = comp_nthoctave_axis(noct, freqs[0], freqs[-1])
    # Compute sum over each interval
    freqbds = [f / (2 ** (1.0 / (2.0 * noct))) for f in f_oct]
    freqbds.append(freqbds[-1])
    # freqbds = [0] + f_oct
    values_oct = []
    N = zeros(len(freqbds) - 1)
    for i in range(len(freqbds) - 1):
        f1 = freqbds[i]
        f2 = freqbds[i + 1]
        indices = argwhere((freqs >= f1) & (freqs <= f2))
        N[i] = len(indices)
        if len(indices) == 0:
            values_oct.append(0)
        else:
            values2 = take(values, indices)
            if np_sum(values2) == 0:
                values_oct.append(0)
            else:
                values_oct.append(sqrt(np_sum(values2 ** 2)))
    values = array(values_oct)
    # Apply bin correction factor for when centre frequencies are not integer
    # multiples of the bandwicth (BW)
    df_fft = freqs[1] - freqs[0]
    BW = zeros(len(freqbds) - 1)
    for i in range(len(freqbds) - 1):
        BW[i] = freqbds[i + 1] - freqbds[i]
    for i in range(len(freqbds) - 1):
        if (N[i] != 0) and (floor(BW[i] / df_fft) <= N[i]):
            values[i] = values[i] * (BW[i] / (df_fft * N[i])) ** 0.5
    return [values, array(f_oct)]


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
    if len(values.shape) > 2:
        z = values[:, 2]

    affixe = r * exp(1j * phi)
    x = real(affixe)
    y = imag(affixe)

    if len(values.shape) > 2:
        return column_stack((x, y, z))
    else:
        return column_stack((x, y))


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


def time_to_freqs(values, is_real):
    is_time = True
    return comp_fft_freqs(values, is_time, is_real)


def freqs_to_time(values, is_real):
    is_angle = False
    return comp_fft_time(values, is_angle, is_real)


def angle_to_wavenumber(values, is_real):
    is_time = False
    return comp_fft_freqs(values, is_time, is_real)


def wavenumber_to_angle(values, is_real):
    is_angle = True
    return comp_fft_time(values, is_angle, is_real)


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

    dim_array = ones((1, field_x.ndim), int).ravel()
    dim_array[1] = -1

    # Reshape b with dim_array and perform elementwise multiplication with
    # broadcasting along the singleton dimensions for the final output
    cos_phi_reshaped = cos_phi.reshape(dim_array)
    sin_phi_reshaped = sin_phi.reshape(dim_array)

    field_r = field_x * cos_phi_reshaped + field_y * sin_phi_reshaped
    field_phi = -field_x * sin_phi_reshaped + field_y * cos_phi_reshaped

    return (field_r, field_phi)


def pol2cart(field_r, field_phi, phi):
    cos_phi = cos(phi)
    sin_phi = sin(phi)

    dim_array = ones((1, field_r.ndim), int).ravel()
    dim_array[1] = -1

    # Reshape b with dim_array and perform elementwise multiplication with
    # broadcasting along the singleton dimensions for the final output
    cos_phi_reshaped = cos_phi.reshape(dim_array)
    sin_phi_reshaped = sin_phi.reshape(dim_array)

    field_x = field_r * cos_phi_reshaped - field_phi * sin_phi_reshaped
    field_y = field_r * sin_phi_reshaped + field_phi * cos_phi_reshaped

    return (field_x, field_y)
