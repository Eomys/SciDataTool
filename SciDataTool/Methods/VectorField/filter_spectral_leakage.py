import numpy as np


def filter_spectral_leakage(self, freqs_th):
    """Filter spectral leakage from a SciDataTool VectorField object

    Parameters
    ----------
    self : VectorField
        a VectorField object to be filtered
    freqs_th : ndarray
        theoretical frequencies

    Returns
    -------
    vf_filt : VectorField
        Filtered vectorfield

    """

    # Init filtered VectorField
    vf_filt = type(self)(name=self.name, symbol=self.symbol, components=dict())

    axes_list = list()
    arg_list = list()
    Wmatf = np.array([])
    If = np.array([])
    for comp, data in self.components.items():
        # Filter components by components
        (
            data_filt,
            axes_list,
            arg_list,
            Wmatf,
            If,
            freqs_th,
        ) = data.filter_spectral_leakage(
            freqs_th, axes_list, arg_list, Wmatf, If, is_return_calc_data=True
        )
        # Store filtered data in VectorField
        vf_filt.components[comp] = data_filt

    return vf_filt
