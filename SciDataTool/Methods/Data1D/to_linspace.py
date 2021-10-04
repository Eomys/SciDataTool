from numpy import allclose, linspace

from SciDataTool.Functions import AxisError


def to_linspace(self):
    """Tests if values are a linspace and returns a DataLinspace (or Data1D if not possible)
    Parameters
    ----------
    self: Data1D
        a Data1D object
    Returns
    -------
    DataLinspace or Data1D
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataLinspace", fromlist=["DataLinspace"])
    DataLinspace = getattr(module, "DataLinspace")

    values = self.values
    if allclose(
        values,
        linspace(values[0], values[-1], len(values), endpoint=True),
        rtol=1e-5,
        atol=1e-8,
        equal_nan=False,
    ):
        New_axis = DataLinspace(
            initial=values[0],
            final=values[-1],
            number=len(values),
            include_endpoint=True,
            name=self.name,
            unit=self.unit,
            symmetries=self.symmetries,
            normalizations=self.normalizations,
            is_components=self.is_components,
            symbol=self.symbol,
        )
    else:
        New_axis = self.copy()

    return New_axis
