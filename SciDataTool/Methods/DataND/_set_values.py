from SciDataTool.Classes._check import check_dimensions, check_var
from numpy import squeeze, array


def _set_values(self, value):
    """setter of values"""
    if type(value) is int and value == -1:
        value = array([])
    elif type(value) is list:
        try:
            value = array(value)
        except:
            pass
    check_var("values", value, "ndarray")

    # Check dimensions
    if value is not None:
        value = squeeze(value)
    value = check_dimensions(value, self.axes)
    self._values = value
