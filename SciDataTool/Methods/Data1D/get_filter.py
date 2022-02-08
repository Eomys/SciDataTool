from SciDataTool.Functions import AxisError


def get_filter(self, filter_dict):
    """Get filtering indices
    Parameters
    ----------
    self: Data1D
        a Data1D object
    filter_dict: dict
        a dict of the values to filter (keep values defined in filter_dict)
    Returns
    -------
    indices: list
        list of indices to use to get corresponding filter
    """

    # Check that keys in filter_dict are correctly defined in self.filter
    if len(filter_dict.keys()) != len(self.filter.keys()):
        raise AxisError("Filter key not defined in Data1D.filter")
    for key in filter_dict:
        if key not in self.filter:
            raise AxisError("Filter key not defined in Data1D.filter")

    # Prepare filtering keys in correct order
    keys = self.check_filter()

    indices = []
    for i, value in enumerate(self.values):
        items = value.split(self.delimiter)
        nb_match = 0
        for j, item in enumerate(items):
            if item in filter_dict[keys[j]]:
                nb_match += 1
        if nb_match == len(keys):
            indices.append(i)

    return indices
