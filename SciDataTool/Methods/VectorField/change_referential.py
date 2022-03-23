import numpy as np


def change_referential(
    self, rotation_speed, is_waveform, atol=1e-9, sym_t_new=dict(), atol_freq=1e-6
):
    """Change referential of vectorfield given input rotation speed (algebric to include rotation direction)

    Parameters
    ----------
    self : VectorField
        A VectorField object
    rotation_speed : float
        rotation speed [rpm]
    is_waveform: bool
        True to perform referential change in waveform domain (time/space) otherwise perform it in spectral domain (freqs/wavenumber)
    atol: float
        Absolute tolerance under which amplitudes are assumed to be 0
    sym_t_new: dict
        Dict of symmetries in new referential
    atol_freq: float
        Absolute tolerance under which frequencies are assumed to be equal

    Returns
    -------
    vf_new : VectorField
        Vectorfield converted in new referential
    """

    # Init referential changed VectorField
    vf_new = type(self)(name=self.name, symbol=self.symbol, components=dict())

    # Loop on components to convert them to new referential
    axes_list_change = list()
    arg_list = list()
    freqs_new = np.array([])
    I1 = np.array([])
    Irf_un = np.array([])
    Imask = np.array([])
    ta_in = tuple()
    ta_out = tuple()
    for comp, data in self.components.items():

        # Change referential
        (
            data_new,
            axes_list_change,
            arg_list,
            freqs_new,
            I1,
            Irf_un,
            ta_in,
            ta_out,
        ) = data.change_referential(
            rotation_speed,
            is_waveform,
            atol=0,
            axes_list_change=axes_list_change,
            arg_list=arg_list,
            freqs_new=freqs_new,
            I1=I1,
            Irf_un=Irf_un,
            sym_t_new=sym_t_new,
            ta_in=ta_in,
            ta_out=ta_out,
            atol_freq=atol_freq,
        )

        # Filter harmonics that are below input absolute tolerance
        if atol > 0 and not is_waveform:

            # Copy axis not to change axis in axes_list_change
            data_new.axes = [axis.copy() for axis in data_new.axes]

            # Filter harmonics that are below input absolute tolerance
            if Imask.size == 0:
                val = np.abs(data_new.values)
                val_max = np.max(val)
                while val.ndim > 1:
                    val = np.sum(val, axis=-1)
                Imask = val > val_max * atol
            data_new.axes[0].values = data_new.axes[0].values[Imask]
            data_new.values = data_new.values[Imask, ...]

        # Store referential changed data in VectorField
        vf_new.components[comp] = data_new

    return vf_new
