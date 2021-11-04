from numpy import array

from importlib import import_module

from SciDataTool.Classes.DataPattern import DataPattern

from SciDataTool.Functions.symmetries import rebuild_symmetries_axis
from SciDataTool.Functions import AxisError

operation_list = [
    "sum",
    "rss",
    "mean",
    "rms",
    "integrate",
    "integrate_local",
    "derivate",
    "antiderivate",
]


def get_axis(self, axis, is_real):
    """Computes the vector 'axis' in the unit required, using conversions and symmetries if needed.
    Parameters
    ----------
    self: RequestedAxis
        a RequestedAxis object
    axis: Axis
        an Axis object
    """

    if self.operation is not None:
        module = import_module("SciDataTool.Functions.conversions")
        func = getattr(module, self.operation)  # Conversion function
    if isinstance(axis, DataPattern):
        self.is_pattern = True
        self.rebuild_indices = axis.rebuild_indices
        self.is_step = axis.is_step
    is_components = getattr(axis, "is_components", False)
    if is_components:
        values = axis.get_values(unit=self.unit)
        if self.indices is not None:
            if self.indices[0] == ":":
                self.values = values
                self.indices = list(range(len(values)))
            else:
                self.values = values[self.indices]
                self.extension = "list"
        elif self.extension not in operation_list and self.extension != "list":
            self.values = values
            self.extension = "whole"
        else:
            self.values = values

    else:
        if self.extension == "pattern":
            if not self.is_pattern:
                raise AxisError("[pattern] cannot be called with non DataPattern axis")
            else:
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
                self.extension = "smallestperiod"
        elif self.extension == "smallestperiod":
            # if isinstance(axis, DataPattern):
            #     raise AxisError(
            #         "[smallestperiod] cannot be called with DataPattern axis"
            #     )
            # else:
            is_smallestperiod = True
            is_oneperiod = False
            is_antiperiod = False
        elif self.extension == "antiperiod":
            if isinstance(axis, DataPattern):
                raise AxisError("[antiperiod] cannot be called with DataPattern axis")
            else:
                is_smallestperiod = False
                is_oneperiod = False
                is_antiperiod = True
        elif self.extension == "oneperiod" or self.transform == "fft":
            if isinstance(axis, DataPattern):
                raise AxisError("[oneperiod] cannot be called with DataPattern axis")
            else:
                is_smallestperiod = False
                is_oneperiod = True
                is_antiperiod = False
        elif self.extension in operation_list:
            # Remove periodicities in case of DataPattern otherwise operations can be applied on periodic signals
            is_smallestperiod = not self.is_pattern
            is_oneperiod = False
            is_antiperiod = False
        # Ignore symmetries if fft axis
        elif self.name == "freqs" or self.name == "wavenumber":
            is_smallestperiod = True
            is_oneperiod = False
            is_antiperiod = False
        else:
            if self.input_data is not None and not self.is_step:
                # Check if symmetries need to be reconstructed to match input_data
                axis_values = axis.get_values(
                    is_smallestperiod=True,
                    operation=self.operation,
                    is_real=is_real,
                )
                if min(self.input_data) >= min(axis_values) and max(
                    self.input_data
                ) <= max(axis_values):
                    is_smallestperiod = True
                    is_oneperiod = False
                    is_antiperiod = False
                else:
                    axis_values = axis.get_values(
                        is_oneperiod=True,
                        operation=self.operation,
                        is_real=is_real,
                    )
                    if min(self.input_data) >= min(axis_values) and max(
                        self.input_data
                    ) <= max(axis_values):
                        is_smallestperiod = False
                        is_oneperiod = True
                        is_antiperiod = False
                        self.extension = "oneperiod"
                    else:
                        is_smallestperiod = False
                        is_oneperiod = False
                        is_antiperiod = False
                        if not self.is_pattern:
                            self.extension = "interval"
            elif self.transform == "ifft":  # Ignore symmetries in ifft case
                is_smallestperiod = True
                is_oneperiod = False
                is_antiperiod = False
            else:
                is_smallestperiod = False
                is_oneperiod = False
                is_antiperiod = False
        # Get original values of the axis including unit and normalizations
        # Store before normalization/operation
        if (
            self.unit != self.corr_unit
            and self.unit != "SI"
            or self.operation is not None
        ):
            self.corr_values = array(
                axis.get_values(
                    is_oneperiod=is_oneperiod,
                    is_antiperiod=is_antiperiod,
                    is_smallestperiod=is_smallestperiod,
                )
            )
        # Prepare unit
        # if self.corr_unit is None:
        #     self.corr_unit = self.unit
        values = axis.get_values(
            is_oneperiod=is_oneperiod,
            is_antiperiod=is_antiperiod,
            is_smallestperiod=is_smallestperiod,
            unit=self.unit,
            operation=self.operation,
            is_real=is_real,
            corr_unit=self.corr_unit,
        )

        # Rebuild symmetries in fft case
        if self.transform == "fft":
            if "period" in axis.symmetries:
                if axis.name != "time":
                    values = values * axis.symmetries["period"]
            elif "antiperiod" in axis.symmetries:
                if axis.name != "time":
                    values = values * axis.symmetries["antiperiod"] / 2
        # Rebuild symmetries in ifft case
        if self.transform == "ifft":
            if self.extension not in [
                "smallestperiod",
                "oneperiod",
                "antiperiod",
                "sum",
                "mean",
                "rms",
                "rss",
                "integrate",
                "integrate_local",
                "derivate",
                "antiderivate",
            ]:
                values = rebuild_symmetries_axis(values, axis.symmetries)
        # Interpolate axis with input data
        if self.input_data is None:
            self.values = values
        else:
            if len(self.input_data) == 2 and self.extension != "axis_data":
                indices = [
                    i
                    for i, x in enumerate(values)
                    if x >= self.input_data[0] and x <= self.input_data[-1]
                ]
                if self.indices is None:
                    self.indices = indices
                else:
                    indices_new = []
                    for i in self.indices:
                        if i in indices:
                            indices_new.append(i)
                    self.indices = indices_new
                self.input_data = None
            else:
                self.values = values
        if self.indices is not None:
            self.values = values[self.indices]
            if self.extension in operation_list:
                self.indices = None
