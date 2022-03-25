from SciDataTool.Functions.Plot import ifft_dict, fft_dict


def is_axes_in_order(axes_selected, data):
    """Detect if axes given are in order compared to how they are store in a Data object
    Parameters
    ----------
    axes_selected: list
        List of axes selected as str
    data : Data
        Data object reference that store the axes
    Returns
    -------
    boolean stating if the axes are in order or not
    """
    not_in_order = False
    axes_name = [ax.name for ax in data.get_axes()]
    axes_selected_name = [ax.split("{")[0] for ax in axes_selected]

    if axes_selected_name[0] in axes_name and axes_selected_name[1] in axes_name:
        if axes_name.index(axes_selected_name[0]) > axes_name.index(
            axes_selected_name[1]
        ):
            not_in_order = True
            axes_selected = [axes_selected[1], axes_selected[0]]

    elif axes_selected_name[0] in ifft_dict and axes_selected_name[1] in ifft_dict:
        if axes_name.index(ifft_dict[axes_selected_name[0]]) > axes_name.index(
            ifft_dict[axes_selected_name[1]]
        ):

            not_in_order = True
            axes_selected = [axes_selected[1], axes_selected[0]]

    elif axes_selected_name[0] in fft_dict and axes_selected_name[1] in fft_dict:
        if axes_name.index(fft_dict[axes_selected_name[0]]) > axes_name.index(
            fft_dict[axes_selected_name[1]]
        ):

            not_in_order = True
            axes_selected = [axes_selected[1], axes_selected[0]]

    return not_in_order, axes_selected
