from SciDataTool import Data1D
from SciDataTool.Functions import axes_dict, rev_axes_dict
from SciDataTool.Functions.conversions import get_unit_derivate, get_unit_integrate


def get_data_along(self, *args, unit="SI", is_norm=False, axis_data=[]):
    """Returns the sliced or interpolated version of the data, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    axis_data: list
        list of ndarray corresponding to user-input data
    Returns
    -------
    a DataND object
    """

    results = self.get_along(
        *args, is_squeeze=False, unit=unit, is_norm=is_norm, axis_data=axis_data
    )
    values = results.pop(self.symbol)
    del results["axes_dict_other"]
    axes_list = results.pop("axes_list")
    Axes = []

    axes_name_new = list(results.keys())
    if "time" in axes_name_new:
        Data_type = "DataTime"
    elif "freqs" in axes_name_new:
        Data_type = "DataFreq"
    else:
        Data_type = "DataND"

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes." + Data_type, fromlist=[Data_type])
    DataClass = getattr(module, Data_type)

    for axis_name in axes_name_new:
        if not isinstance(results[axis_name], str):
            for i, axis in enumerate(self.axes):
                if axis.name == axis_name:
                    index = i
                    name = axis.name
                    is_components = axis.is_components
                    axis_values = results[axis_name]
                    unit = axis.unit
                elif axis_name in axes_dict:
                    if axes_dict[axis_name][0] == axis.name:
                        index = i
                        name = axis_name
                        is_components = axis.is_components
                        axis_values = results[axis_name]
                        unit = axes_dict[axis_name][2]
                elif axis_name in rev_axes_dict:
                    if rev_axes_dict[axis_name][0] == axis.name:
                        index = i
                        name = axis_name
                        is_components = axis.is_components
                        axis_values = results[axis_name]
                        unit = rev_axes_dict[axis_name][2]
            # Update symmetries
            if "smallestperiod" in args[index] or args[index] in [
                "freqs",
                "wavenumber",
            ]:
                symmetries = self.axes[index].symmetries
            else:
                symmetries = dict()
            Axes.append(
                Data1D(
                    name=name,
                    unit=unit,
                    values=axis_values,
                    is_components=is_components,
                    normalizations=self.axes[index].normalizations,
                    symmetries=symmetries,
                ).to_linspace()
            )
    # Update unit if derivation or integration
    unit = self.unit
    for axis in axes_list:
        if axis.extension in ["antiderivate", "integrate"]:
            unit = get_unit_integrate(self.unit, axis.corr_unit)
        elif axis.extension == "derivate":
            unit = get_unit_derivate(self.unit, axis.corr_unit)

    return DataClass(
        name=self.name,
        unit=unit,
        symbol=self.symbol,
        axes=Axes,
        values=values,
        normalizations=self.normalizations,
        is_real=self.is_real,
    )
