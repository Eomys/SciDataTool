from SciDataTool.Functions import AxisError


def check_filter(self):
    """Check if filter is correctly defined
    Parameters
    ----------
    self: Data1D
        a Data1D object
    Returns
    -------
    keys: list
        list of filter keys in same order as in values
    """
    keys = []
    for i, value in enumerate(self.values):
        items = value.split(self.delimiter)
        if len(items) != len(self.filter.keys()):
            raise AxisError("Filter is not correctly defined")
        for item in items:
            is_match = False
            for key in self.filter:
                if item in self.filter[key]:
                    is_match = True
                    if i == 0:
                        keys.append(key)
            if not is_match:
                raise AxisError("Missing item in filter: " + item)

    return keys
