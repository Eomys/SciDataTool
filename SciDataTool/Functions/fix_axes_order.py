from numpy import array
from SciDataTool.Functions.Plot import fft_dict, ifft_dict


def fix_axes_order(axes_list, args):
    """Put args in same order as axes_list"""
    indices = []
    for j, arg in enumerate(args):
        for i, axis in enumerate(axes_list):
            if (
                axis in arg
                or axis in fft_dict
                and fft_dict[axis] in arg
                or axis in ifft_dict
                and ifft_dict[axis] in arg
            ):
                indices.append(i)
                break
    if len(indices) < len(args):
        # axis was not in data -> keep same order
        return args
    else:
        sort_indices = array(indices).argsort()
        return [args[i] for i in sort_indices]
