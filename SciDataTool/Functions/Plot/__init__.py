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
    "Critical band rate": "Bark",
    "speed": "rpm",
    "Rotation speed": "rpm",
    "modes": "",
    "designs": "",
}

axis_norm_dict = {
    "time": ["angle_rotor", "speed"],
    "angle": ["tooth_id", "distance"],
    "freqs": ["elec_order", "mech_order"],
    "wavenumber": ["space_order"],
    "z": ["x L"],
    "Critical band rate": ["Hz"],
}

norm_name_dict = {
    "elec_order": "Electrical order",
    "mech_order": "Mechanical order",
    "space_order": "Space order",
    "distance": "Distance",
    "angle_rotor": "Rotor mechanical angle",
    "tooth_id": "Stator tooth number",
    "x L": "x L",
    "Hz": "Hz",
    "speed": "speed",
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
    "speed": "Rotation speed [rpm]",
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

REV_COMP_DICT = {
    "radial": "radial",
    "tangential": "circumferential",
    "axial": "axial",
    "comp_x": "x-axis component",
    "comp_y": "y-axis component",
    "comp_z": "z-axis component",
}

PARAM_3D = [
    "is_2D_view",
    "is_contour",
    "is_same_size",
    "N_stem",
    "colormap",
    "annotation_delim",
    "marker_color",
    "z_range",
]

PARAM_2D = [
    "color_list",
    "data_list",
    "legend_list",
    "fund_harm_dict",
    "is_show_legend",
]