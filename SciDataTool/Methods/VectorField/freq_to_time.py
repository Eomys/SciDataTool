def freq_to_time(self):
    """Performs the Fourier Transform and stores the resulting field in a VectorField of DataTime objects.
    Parameters
    ----------
    self : VectorField
        a VectorField object
    Returns
    -------
    a VectorField object
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.VectorField", fromlist=["VectorField"])
    VectorField = getattr(module, "VectorField")

    comp_dict = dict()
    for key, comp in self.components.items():
        comp_dict[key] = comp.freq_to_time()

    return VectorField(name=self.name, symbol=self.symbol, components=comp_dict)
