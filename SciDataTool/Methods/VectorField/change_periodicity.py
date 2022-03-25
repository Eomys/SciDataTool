import numpy as np

from SciDataTool.Functions.Load.import_class import import_class


def change_periodicity(
    self, per_a_new, per_t_new, is_aper_a_new=None, is_aper_t_new=False
):
    """Change (anti-)periodicities of vectorfield given input periodicities before changing referential

    Parameters
    ----------
    self : VectorField
        A VectorField object
    per_a_new : int
        New number of space periodicities of the machine over 2*pi
    per_t_new : int
        New number of time periodicities of the machine over time period (p/felec by default if Nrev is None) in static or rotating referential
    is_aper_a_new : bool
        True if spatial anti-periodicity in requested for new vectorfield
    is_aper_t_new : bool
        True if time anti-periodicity in requested for new vectorfield

    Returns
    -------
    vf_new : VectorField
        Vectorfield converted with new periodicities
    """

    DataLinspace = import_class("SciDataTool.Classes", "DataLinspace")

    # Get axes list in original VectorField
    # Assumes axes are the following: time, angle, z and z is DataPattern
    axes_list = self.get_axes()

    # Get replicating number for time axis
    per_t, is_aper_t = axes_list[0].get_periodicity()
    per_t = int(per_t / 2) if is_aper_t else per_t
    Nrep_t = int(per_t / per_t_new)
    Nt = Nrep_t * axes_list[0].get_length(
        is_oneperiod=Nrep_t > 1 or (Nrep_t == 1 and not is_aper_t_new),
        is_antiperiod=Nrep_t == 1 and is_aper_t_new,
    )

    # Get replicating number for angle axis
    per_a, is_aper_a = axes_list[1].get_periodicity()
    if is_aper_a_new is None:
        is_aper_a_new = is_aper_a
    per_a = int(per_a / 2) if is_aper_a else per_a
    Nrep_a = int(per_a / per_a_new)
    Na = Nrep_a * axes_list[1].get_length(
        is_oneperiod=Nrep_a > 1 or (Nrep_a == 1 and not is_aper_a_new),
        is_antiperiod=Nrep_a == 1 and is_aper_a_new,
    )

    if Nrep_t == 1 and Nrep_a == 1:
        # Return VectorField as it is
        return self.copy()

    # Init periodicity changed VectorField
    vf_new = type(self)(name=self.name, symbol=self.symbol, components=dict())

    # Keep time anti-periodicity if it exists
    if Nrep_t == 1 and is_aper_t_new:
        time_arg = "time[smallestperiod]"
    else:
        time_arg = "time[oneperiod]"

    # Keep spatial anti-periodicity if it exists
    if Nrep_a == 1 and is_aper_a_new:
        angle_arg = "angle[smallestperiod]"
    else:
        angle_arg = "angle[oneperiod]"

    # Get argument list for call to get_rphiz_along on one time and space period
    arg_list = [time_arg, angle_arg, "z[smallestpattern]"]

    # Get axes values on requested axes
    result = self.get_rphiz_along(*arg_list, is_squeeze=False)
    axes_list_new = list()
    for axis in axes_list:
        axis_new = axis.copy()
        # Change time periodicity
        if Nrep_t > 1 and axis.name == "time":
            axis_new.symmetries = {"period": per_t_new}
            time_full = result["time"]
            if isinstance(axis_new, DataLinspace):
                if axis.include_endpoint:
                    t_final = time_full[-1] + time_full[1] - time_full[0]
                else:
                    t_final = axis.final
                axis_new.number = Nt
                axis_new.final = Nrep_t * t_final
                axis_new.include_endpoint = False
            else:
                t_final = time_full[-1] + time_full[1] - time_full[0]
                for k in range(1, Nrep_t):
                    time_full = np.append(time_full, result["time"] + k * t_final)
                axis_new.values = time_full
        # Change angle periodicity
        if Nrep_a > 1 and axis.name == "angle":
            axis_new.symmetries = {"period": per_a_new}
            angle_full = result["angle"]
            if isinstance(axis_new, DataLinspace):
                if axis.include_endpoint:
                    a_final = angle_full[-1] + angle_full[1] - angle_full[0]
                else:
                    a_final = axis.final
                axis_new.number = Na
                axis_new.final = Nrep_a * a_final
                axis_new.include_endpoint = False
            else:
                a_final = angle_full[-1] + angle_full[1] - angle_full[0]
                for k in range(1, Nrep_a):
                    angle_full = np.append(angle_full, result["angle"] + k * a_final)
                axis_new.values = angle_full

        axes_list_new.append(axis_new)

    # Replicate values by the number of repetitions
    for comp, data in self.components.items():

        # Duplicate values
        if Nrep_t > 1 and Nrep_a > 1:
            val_new = np.tile(result[comp], (Nrep_t, Nrep_a, 1))
        elif Nrep_t > 1:
            val_new = np.tile(result[comp], (Nrep_t, 1, 1))
        elif Nrep_a > 1:
            val_new = np.tile(result[comp], (1, Nrep_a, 1))

        # Create new data object with updated periodicities
        data_new = type(data)(
            name=data.name,
            symbol=data.symbol,
            unit=data.unit,
            axes=axes_list_new,
            values=val_new,
            normalizations=data.normalizations.copy(),
            is_real=data.is_real,
        )

        # Store reduced periodicity data in VectorField
        vf_new.components[comp] = data_new

    return vf_new
