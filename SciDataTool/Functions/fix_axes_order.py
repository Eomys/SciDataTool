from numpy import array
from SciDataTool.Functions.Plot import fft_dict, ifft_dict


def fix_axes_order(axes_list, args):
    """Put args in same order as axes_list"""
    indices = []
    for arg in args:
        for i, axis in enumerate(axes_list):
            if axis in arg:
                indices.append(i)
                break
            elif axis in fft_dict and fft_dict[axis] in arg:
                indices.append(i)
                break
            elif axis in ifft_dict and ifft_dict[axis] in arg:
                indices.append(i)
                break
    sort_indices = array(indices).argsort()
    return [args[i] for i in sort_indices]
