unit_dict = {
    "time": "s",
    "angle": "°",
    "freqs": "Hz",
    "wavenumber": "",
    "phase": "",
    "z": "m",
    "radius": "m",
    "distance": "m",
    "loadcases": "",
    "eccentricity": "%",
    "frequency": "Hz",
    "revolution": "",
    "order": "",
    "cr_band": "Bark",
    "speed": "rpm",
    "Rotation speed": "rpm",
    "modes": "",
}

axis_norm_dict = {
    "time": ["angle_rotor"],
    "angle": ["tooth_id", "distance"],
    "freqs": ["elec_order", "mech_order"],
    "wavenumber": ["space_order"],
    "z": ["x L"],
}

norm_name_dict = {
    "elec_order": "Electrical order",
    "mech_order": "Mechanical order",
    "space_order": "Space order",
    "distance": "Distance",
    "angle_rotor": "Rotor mechanical angle",
    "tooth_id": "Stator tooth number",
    "x L": "x L",
}

norm_dict = {
    "elec_order": "Electrical order []",
    "mech_order": "Mechanical order []",
    "space_order": "Space order []",
    "distance": "Distance [m]",
    "angle_rotor": "Rotor mechanical angle [°]",
    "tooth_id": "Stator tooth number []",
    "speed": "Speed [rpm]",
    "Hz": "Frequency [Hz]",
    "Bark": "Critical band rate [Bark]",
    "time": "Time [s]",
}

axes_dict = {
    "freqs": "frequency",
    "cr_band": "critical band rate",
    "z": "axial direction",
    "loadcases": "load cases",
}

fft_dict = {
    "time": "freqs",
    "angle": "wavenumber",
}

ifft_dict = {
    "freqs": "time",
    "wavenumber": "angle",
}

# Colors and linestyles
COLORS = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
    "b",
    "g",
    "m",
    "yellow",
    "black",
    "lawngreen",
    "dodgerblue",
    "darkviolet",
    "deeppink",
]

LINESTYLES = [
    "solid",
    "dotted",
    "dashed",
    "dashdot",
    (0, (1, 10)),
    (0, (5, 10)),
    (0, (3, 5, 1, 5)),
    (0, (3, 10, 1, 10)),
    (0, (3, 5, 1, 5, 1, 5)),
    (0, (3, 1, 1, 1, 1, 1)),
]

## Paramater for Schematics plot
P_FONT_SIZE = 12  # Point Font size
SC_FONT_SIZE = 12  # Schematics Font size
TEXT_BOX = dict(  # Parameter of the text box
    boxstyle="round",
    ec=(0.0, 0.0, 0.0),
    fc=(1.0, 1.0, 1.0),
)
# Arrow parameters
ARROW_WIDTH = 2
ARROW_COLOR = "black"
# Schematics lines
SC_LINE_COLOR = "black"
SC_LINE_STYLE = "dotted"
SC_LINE_WIDTH = 1
# Main lines
MAIN_LINE_COLOR = "0.5"  # Gray
MAIN_LINE_STYLE = "dotted"
MAIN_LINE_WIDTH = 1
